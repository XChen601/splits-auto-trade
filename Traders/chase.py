from dotenv import load_dotenv
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import winsound

class ChaseTrader:
    def __init__(self, tracker, share_amt, extended_hour, chase_accounts):
        self.tracker = tracker
        self.share_amt = share_amt
        self.extended_hour = extended_hour
        self.chase_accounts = chase_accounts

    def login(self, driver):
        load_dotenv()
        chase_username = os.getenv('CHASE_USER')
        chase_password = os.getenv('CHASE_PASSWORD')

        print('=============  CHASE  =============')
        driver.get('https://secure09ea.chase.com/web/auth/#/logon/logon/chaseOnline?navKey=reviewOffers&lang=en')

        time.sleep(3)
        username_input = WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.ID, 'userId-text-input-field')))
        pw_input = driver.find_element(By.ID, 'password-text-input-field')
        login_btn = driver.find_element(By.ID, 'signin-button')

        username_input.send_keys(chase_username)
        time.sleep(.5)
        pw_input.send_keys(chase_password)
        time.sleep(.5)
        login_btn.click()

        notif_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'label-sec-auth-options-0')))
        notif_button.click()
        next_button = driver.find_element(By.ID, "requestIdentificationCode-sm")
        next_button.click()

        winsound.Beep(400, 800)

        # wait for user to finish phone prompt and the page to load
        wait = WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'investment-disclosures-headbar')))
        time.sleep(2)

    def trade(self, driver, symbol_list, limit_price, trade_type):
        self.login(driver)

        for symbol in symbol_list:
            for account_num in self.chase_accounts:
                try:
                    driver.get(
                        'https://secure06ea.chase.com/web/auth/dashboard#/dashboard/trade/equity/entry;ai=select-account;sym=')
                    time.sleep(2.5)

                    dropdown = WebDriverWait(driver, 12).until(
                        EC.presence_of_element_located((By.ID, 'header-accountDropDown')))
                    dropdown.click()
                    time.sleep(1)

                    account = driver.find_element(By.XPATH, f"//*[contains(text(), '...{account_num}')]")
                    account.click()
                    time.sleep(2)

                    symbol_input = WebDriverWait(driver, 12).until(
                        EC.element_to_be_clickable(
                            (By.ID, 'equitySymbolLookup-block-autocomplete-validate-input-field')))
                    symbol_input.send_keys(symbol)
                    symbol_input.send_keys(Keys.RETURN)
                    time.sleep(2)

                    if trade_type.lower() == 'sell':
                        sell_btn = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="tradeActions-container"]/span[2]/label')))
                        sell_btn.click()
                    elif trade_type.lower() == 'buy':
                        buy_btn = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="tradeActions-container"]/span[1]/label')))
                        buy_btn.click()

                    try:
                        market_btn = driver.find_element(By.XPATH,
                                                         '//*[@id="tradeOrderTypeOptions-container"]/span[1]/label')
                        market_btn.click()
                    except:
                        time.sleep(2)
                        market_btn = driver.find_element(By.XPATH,
                                                         '//*[@id="tradeOrderTypeOptions-container"]/span[1]/label')
                        market_btn.click()

                    if trade_type.lower() == 'sell':
                        sell_btn = driver.find_element(By.XPATH, '//*[@id="tradeActions-container"]/span[2]/label')
                        sell_btn.click()
                    elif trade_type.lower() == 'buy':
                        buy_btn = driver.find_element(By.XPATH, '//*[@id="tradeActions-container"]/span[1]/label')
                        buy_btn.click()

                    quantity_input = driver.find_element(By.ID, 'tradeQuantity-text-input-field')
                    quantity_input.send_keys(self.share_amt)

                    day_btn = driver.find_element(By.XPATH, '//*[@id="tradeExecutionOptions-container"]/span[1]/label')
                    day_btn.click()
                    time.sleep(1)

                    preview_btn = driver.find_element(By.ID, 'previewOrder')
                    preview_btn.click()
                    time.sleep(1)

                    # if accept btn appears when market closed
                    try:
                        accept_btn = WebDriverWait(driver, 1).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="acceptWarnings"]//button')))
                        accept_btn.click()
                    except:
                        pass

                    place_order_btn = WebDriverWait(driver, 4).until(
                        EC.presence_of_element_located((By.ID, 'submitOrder')))
                    place_order_btn.click()

                    try:
                        order_confirm = WebDriverWait(driver, 2).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="accessible-text-title"]')))
                        print(order_confirm.text)
                    except:
                        pass
                    time.sleep(1)
                    # print(f"{symbol} - {trade_type}: on account {account_num}")
                    # if market closed, queue order for next business day
                    # yes_btn = WebDriverWait(driver, 4).until(
                    #                    EC.presence_of_element_located((By.XPATH, '//*[@id="confirmAfterHoursOrder"]//button')))
                    # yes_btn.click()
                    order_status_btn = WebDriverWait(driver, 4).until(
                        EC.presence_of_element_located((By.ID, 'orderStatusButton')))
                    order_status_btn.click()
                    time.sleep(1)
                    self.tracker.add_success("CHASE", account_num, symbol, trade_type)
                except Exception as e:
                    self.tracker.add_error("CHASE", account_num, symbol, trade_type)
