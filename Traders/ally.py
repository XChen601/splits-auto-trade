from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
load_dotenv()

class AllyTrader:
    def __init__(self, tracker, share_amt, extended_hour, accounts):
        self.tracker = tracker
        self.share_amt = share_amt
        self.accounts = accounts
        self.extended_hour = extended_hour


    def login(self, driver):
        ally_username = os.getenv('ally_username')
        ally_password = os.getenv('ally_password')

        driver.get("https://secure.ally.com/")
        username_input = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.ID, 'username')))
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="login-submit"]')

        username_input.send_keys(ally_username)
        password_input.send_keys(ally_password)
        login_button.click()
        wait = WebDriverWait(driver, 18).until(
            EC.presence_of_element_located((By.ID, 'main')))
        print('ally logged in')
        time.sleep(5)


    def trade(self, driver, symbol_list, limit_price, trade_type):
        self.login(driver)

        for symbol in symbol_list:
            for account_num in range(self.accounts):
                try:
                    driver.get("https://live.invest.ally.com/trading-full/stocks")
                    if account_num == 0:
                        time.sleep(2)
                        try:
                            no_thanks_btn = driver.find_element(By.ID, "noThanks_btn")
                            no_thanks_btn.click()
                        except:
                            pass

                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, 'modal-select-account')))
                    accounts_dropdown = Select(driver.find_element(By.ID, 'modal-select-account'))

                    accounts_dropdown.select_by_index(account_num + 1)
                    time.sleep(.5)

                    continue_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
                    continue_button.click()
                    time.sleep(1)

                    symbol_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        '//*[@id="content"]/div/div[1]/ally-card[1]/section/section-company/div[1]/symbol-search/div[1]/div/div/div[1]/input')))
                    symbol_input.clear()

                    symbol_input = driver.find_element(By.XPATH,
                                                       '//*[@id="content"]/div/div[1]/ally-card[1]/section/section-company/div[1]/symbol-search/div[1]/div/div/div[1]/input')
                    symbol_input.send_keys(symbol)

                    arrow_button = driver.find_element(By.CSS_SELECTOR,
                                                       '[aria-label="Click here to search for a Symbol"]')
                    arrow_button.click()
                    time.sleep(1)

                    quantity_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="stock-quantity"]/div/label/input')))
                    quantity_input.clear()

                    quantity_input = driver.find_element(By.XPATH, '//*[@id="stock-quantity"]/div/label/input')
                    quantity_input.send_keys(self.share_amt)
                    if trade_type.lower() == "sell":
                        sell_btn = driver.find_element(By.ID, "stock-sell")
                        sell_btn.click()
                        time.sleep(.5)
                    if limit_price:
                        limit_button = driver.find_element(By.ID, "stock-limit")
                        limit_button.click()

                        time.sleep(1)
                        limit_input = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="stock-limit-input"]/div/label/input')))
                        limit_input.clear()
                        limit_input.send_keys(limit_price)

                    if self.extended_hour:
                        market_close_button = driver.find_element(By.ID, "stock-market-on-close")
                        market_close_button.click()
                        time.sleep(1)

                    preview_order_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Preview Order')]")
                    preview_order_button.click()

                    place_order_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Place Order')]")))

                    place_order_button.click()
                    time.sleep(2)
                    self.tracker.add_success("ALLY", account_num, symbol, trade_type)
                except Exception as e:
                    print(e)
                    self.tracker.add_error("ALLY", account_num, symbol, trade_type)
                    time.sleep(1)
