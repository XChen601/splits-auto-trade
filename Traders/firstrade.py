from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class FirstradeTrader:
    def __init__(self, tracker, share_amt, extended_hour):
        self.tracker = tracker
        self.share_amt = share_amt
        self.extended_hour = extended_hour


    def login(self, driver):
        load_dotenv()
        firstrade_username = os.getenv("FIRSTRADE_USERNAME")
        firstrade_password = os.getenv("FIRSTRADE_PASSWORD")

        driver.get('https://invest.firstrade.com/cgi-bin/login?ft_locale=en-us')
        username_input = WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.ID, 'username')))
        password_input = driver.find_element(By.ID, 'password')
        login_btn = driver.find_element(By.ID, 'loginButton')
        time.sleep(1)

        username_input.send_keys(firstrade_username)
        password_input.send_keys(firstrade_password)
        login_btn.click()

        # enter pin
        two = WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.ID, 'two')))
        eight = driver.find_element(By.ID, 'eight')
        nine = driver.find_element(By.ID, 'nine')

        two.click()
        time.sleep(.2)
        eight.click()
        time.sleep(.2)
        nine.click()
        time.sleep(.2)
        eight.click()
        driver.find_element(By.ID, 'submit').click()

    def trade(self, driver, symbol_list, limit_price, trade_type):
        self.login(driver)

        driver.get('https://invest.firstrade.com/cgi-bin/main#/cgi-bin/stock_order')

        WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.ID, 'accountId')))
        accounts_dropdown = Select(driver.find_element(By.ID, 'accountId'))
        time.sleep(3)

        # for each symbol
        for symbol in symbol_list:
            # for each account
            for account in range(len(accounts_dropdown.options)):
                try:
                    accounts_dropdown.select_by_index(account)
                    time.sleep(1)
                    buy_btn = WebDriverWait(driver, 12).until(
                        EC.presence_of_element_located((By.ID, 'transactionType_Buy1')))
                    sell_btn = driver.find_element(By.ID, 'transactionType_Sell1')

                    if trade_type == 'buy':
                        buy_btn.click()
                    elif trade_type == 'sell':
                        sell_btn.click()
                    time.sleep(1)
                    shares_input = driver.find_element(By.ID, 'quantity1')
                    shares_input.send_keys(self.share_amt)
                    time.sleep(1)

                    symbol_input = driver.find_element(By.ID, 'symbol1')
                    symbol_input.send_keys(symbol)
                    time.sleep(1)
                    # if no limit price, do market order
                    if limit_price == '':
                        order_types = Select(driver.find_element(By.ID, 'priceType1'))
                        market = order_types.select_by_visible_text('Market')
                    else:
                        limit_price_input = driver.find_element(By.ID, 'limitPrice1')
                        limit_price_input.send_keys(limit_price)
                    time.sleep(1)

                    if self.extended_hour:
                        order_types = Select(driver.find_element(By.ID, 'duration1'))
                        order_types.select_by_visible_text('After Mkt')

                    send_order_btn = driver.find_element(By.ID, 'submitOrder1')
                    send_order_btn.click()

                    self.tracker.add_success("FIRSTRADE", account, symbol, trade_type)
                    time.sleep(1)

                except Exception as e:
                    print(e)
                    print(f"error on account {account}")
                    self.tracker.add_error("FIRSTRADE", account, symbol, trade_type)
