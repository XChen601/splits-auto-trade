from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time
import os

class WellsTrader:
    def __init__(self, tracker, share_amt):
        self.tracker = tracker
        self.share_amt = share_amt



    def login(self, driver):

        def handleLoginError(driver):
            user_input = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID, 'j_username')))
            user_input.send_keys(os.getenv('wells_user'))

            password_input = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID, 'j_password')))
            password_input.send_keys(os.getenv('wells_password'))

        driver.get('https://www.wellsfargoadvisors.com/online-access/signon.htm')
        user_input = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID, 'j_username')))
        user_input.send_keys(os.getenv('wells_user'))

        password_input = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID, 'j_password')))
        password_input.send_keys(os.getenv('wells_password'))

        login_button = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[value="Sign On"]')))
        login_button.click()
        print('Logged into Wells Fargo')
        time.sleep(2)
        if driver.find_elements(By.ID, 'verbose-label-wrapper'):
            input('enter to enter info')
            handleLoginError(driver)

    def trade(self, driver, symbol_list, limit_price, trade_type):
        self.login(driver)
        # go to tradings page
        trade_btn = WebDriverWait(driver, 360).until(EC.presence_of_element_located(
            (By.XPATH,
             '//span[@class="wfanav-full-text d-none d-lg-inline" and @aria-hidden="true" and text()="Trade"]')))
        trade_btn.click()
        time.sleep(2)

        stocks_trade = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID, 'linktradestocks')))
        stocks_trade.click()
        time.sleep(2)

        accounts_dropdown = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID, 'dropdown2')))
        accounts_dropdown.click()
        accounts_dropdown_list = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.ID, 'dropdownlist2')))
        account_count = len(accounts_dropdown_list.find_elements(By.TAG_NAME, "li"))
        time.sleep(2)
        accounts_dropdown.click()
        time.sleep(1)
        for symbol in symbol_list:
            for account_num in range(account_count):
                try:
                    accounts_dropdown = WebDriverWait(driver, 6).until(
                        EC.presence_of_element_located((By.ID, 'dropdown2')))
                    accounts_dropdown.click()
                    accounts_dropdown_list = WebDriverWait(driver, 6).until(
                        EC.presence_of_element_located((By.ID, 'dropdownlist2')))
                    time.sleep(1)

                    selected_account = accounts_dropdown_list.find_elements(By.TAG_NAME, "li")[account_num]
                    selected_account.click()
                    time.sleep(1)

                    try:
                        yes_button = WebDriverWait(driver, 6).until(
                            EC.presence_of_element_located((By.ID, 'btn-continue')))
                        yes_button.click()
                    except:
                        pass
                    print("yesd")
                    time.sleep(1.5)

                    action_btn = WebDriverWait(driver, 6).until(
                        EC.presence_of_element_located((By.ID, 'BuySellBtnText')))
                    action_btn.click()

                    if trade_type.lower() == "buy":
                        buy_btn = WebDriverWait(driver, 6).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-val="Buy"]')))
                        buy_btn.click()
                    elif trade_type.lower() == "sell":
                        sell_btn = WebDriverWait(driver, 6).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-val="Sell"]')))
                        sell_btn.click()

                    symbol_input = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID, 'Symbol')))
                    symbol_input.send_keys(symbol)
                    time.sleep(2)
                    print("symbol inputted")

                    shares_input = WebDriverWait(driver, 6).until(
                        EC.presence_of_element_located((By.ID, 'OrderQuantity')))
                    shares_input.send_keys(self.share_amt)

                    order_type_dropdown = WebDriverWait(driver, 6).until(
                        EC.presence_of_element_located((By.ID, 'OrderTypeBtnText')))
                    order_type_dropdown.click()

                    limit_btn = WebDriverWait(driver, 6).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-val="Limit"]')))
                    limit_btn.click()

                    limit_price_input = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID, 'Price')))
                    # if sell, auto get price
                    if trade_type.lower() == "sell":
                        # get the bid price
                        time.sleep(1)
                        print('test123')
                        bid_price = driver.find_elements(By.CLASS_NAME, "qeval")[1]
                        limit_price_input.send_keys(bid_price.text)
                    else:
                        limit_price_input.send_keys(limit_price)

                    timing_dropdown = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID, 'TIFBtn')))
                    timing_dropdown.click()

                    day_btn = WebDriverWait(driver, 6).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-val="Day"]')))
                    day_btn.click()

                    preview_btn = WebDriverWait(driver, 6).until(
                        EC.presence_of_element_located((By.ID, 'actionbtnContinue')))
                    preview_btn.click()
                    time.sleep(1)

                    submit_btn = WebDriverWait(driver, 6).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'btn-wfa-submit')))
                    submit_btn.click()
                    time.sleep(1)

                    place_another_btn = WebDriverWait(driver, 6).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'btn-wfa-primary')))
                    place_another_btn.click()

                    time.sleep(3)
                except Exception as e:
                    print(e)
                    time.sleep(2)