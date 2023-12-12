from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv
import os

class FidelityTrader:
    def __init__(self, tracker, share_amt, extended_hour, fid_accounts):
        self.tracker = tracker
        self.share_amt = share_amt
        self.extended_hour = extended_hour
        self.fid_accounts = fid_accounts

    def login(self, driver):
        load_dotenv()
        fid_username = os.getenv('FID_USERNAME')
        fid_password = os.getenv('FID_PASSWORD')
        driver.get(
            'https://digital.fidelity.com/prgw/digital/login/full-page?AuthRedUrl=https://digital.fidelity.com/ftgw/digital/portfolio/summary')
        time.sleep(1)
        username = WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.ID, 'dom-username-input')))
        password = driver.find_element(By.ID, 'dom-pswd-input')
        login_btn = driver.find_element(By.ID, 'dom-login-button')
        time.sleep(1)
        for char in fid_username:
            username.send_keys(char)
            time.sleep(.1)
        time.sleep(.5)

        for char in fid_password:
            password.send_keys(char)
            time.sleep(.1)
        time.sleep(.5)
        login_btn.click()
        time.sleep(3)

    def trade(self, driver, symbol_list, limit_price, trade_type):
        self.login(driver)
        for symbol in symbol_list:
            counter = 0
            while True:
                try:
                    self.fid_trade_first(driver, symbol, limit_price, trade_type, counter)
                    break
                except:
                    self.tracker.add_error("FIDELITY", counter, symbol, trade_type)
                    counter += 1
            # now loop through each account in dropdown
            for account_num in range(counter + 1, self.fid_accounts):
                try:
                    dropdown_btn = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.ID, 'dest-acct-dropdown')))
                    dropdown_btn.click()

                    account = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.ID, f'account{account_num}')))
                    account.click()
                    time.sleep(1)
                    # if EXTENDED_HOUR == True:
                    #     extended_hour_btn = driver.find_element(By.XPATH,
                    #                                             "/html/body/div[3]/ap122489-ett-component/div/order-entry-base/div/div/div[1]/div/equity-order-selection/div[2]/order-selection/div/div[1]/div/label")
                    #     extended_hour_btn.click()
                    #     time.sleep(.5)

                    preview_btn = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.ID, 'previewOrderBtn')))
                    preview_btn.click()

                    place_order = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.ID, 'placeOrderBtn')))
                    place_order.click()
                    self.tracker.add_success("FIDELITY", account_num, symbol, trade_type)
                    time.sleep(1)

                except:
                    try:
                        close_error = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'use[href="#pvd3-action__close"]')))
                        close_error.click()
                    except Exception as e:
                        close_error = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            '/html/body/div[3]/ap122489-ett-component/div/pvd3-modal[1]/s-root/div/div[2]/div/button')))
                        driver.execute_script("arguments[0].click();", close_error)
                    time.sleep(1)
                    self.tracker.add_error('FIDELITY', account_num, symbol, trade_type)

            time.sleep(3)

    def fid_trade_first(self, driver, symbol, limit_price, trade_type, counter):
        driver.get('https://digital.fidelity.com/ftgw/digital/trade-equity/index/orderEntry')
        time.sleep(.5)

        dropdown_btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'dest-acct-dropdown')))
        dropdown_btn.click()

        # select first account
        account = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, f'account{counter}')))
        account.click()

        if self.extended_hour == True:
            extended_hour_btn = driver.find_element(By.XPATH,
                                                    "/html/body/div[3]/ap122489-ett-component/div/order-entry-base/div/div/div[1]/div/equity-order-selection/div[2]/order-selection/div/div[1]/div/label")
            extended_hour_btn.click()
            time.sleep(.5)
        symbol_input = driver.find_element(By.ID, 'eq-ticket-dest-symbol')
        symbol_input.send_keys(symbol)

        buy_btn = driver.find_element(By.ID, 'action-buy')
        sell_btn = driver.find_element(By.ID, 'action-sell')

        if trade_type == 'buy':
            buy_btn.click()
            time.sleep(.5)
            buy_btn.click()
        else:
            sell_btn.click()
            time.sleep(.5)
            sell_btn.click()

        time.sleep(.5)
        shares_input = driver.find_element(By.ID, 'shareAmount')
        shares_input.click()
        time.sleep(1)
        shareInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="eqt-shared-quantity"]'))
        )
        shareInput.send_keys(self.share_amt)

        limit_btn = driver.find_element(By.ID, 'market-no')
        limit_btn.click()

        if limit_price == '':
            market_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[for="market-yes-segment"]'))
            )
            market_button.click()
        else:
            # limit price input
            limitPriceInputClick = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="limit-price"]'))
            )
            limitPriceInputClick.click()

            limitPriceInput = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="eqt-ordsel-limit-price-field"]'))
            )
            limitPriceInput.send_keys(limit_price)

        time.sleep(.5)
        preview_btn = driver.find_element(By.ID, 'previewOrderBtn')
        preview_btn.click()

        place_order = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'placeOrderBtn')))
        place_order.click()
        time.sleep(1)