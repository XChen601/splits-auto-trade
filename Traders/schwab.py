from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

class SchwabTrader:
    def __init__(self, tracker, share_amt, extended_hour):
        self.tracker = tracker
        self.share_amt = share_amt
        self.extended_hour = extended_hour

    def login(self, driver, mom):
        load_dotenv()
        schwab_user = os.getenv('SCHWAB_USER')
        schwab_password = os.getenv('SCHWAB_PASSWORD')

        mom_user = os.getenv('mom_user')
        mom_password = os.getenv('mom_password')

        print('=============  SCHWAB  =============')
        driver.get('https://client.schwab.com/login/signon/customercenterlogin.aspx')
        # switch to login iframe
        iframe = driver.find_element(By.XPATH, '//*[@id="lmsSecondaryLogin"]')
        driver.switch_to.frame(iframe)

        login_input = driver.find_element(By.XPATH, '//*[@id="loginIdInput"]')
        pw_input = driver.find_element(By.XPATH, '//*[@id="passwordInput"]')
        login_btn = driver.find_element(By.XPATH, '//*[@id="btnLogin"]')

        username = schwab_user
        password = schwab_password

        if mom:
            username = mom_user
            password = mom_password

        login_input.send_keys(username)
        pw_input.send_keys(password)
        login_btn.click()

        # main_page_wait = WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located((By.ID, "skiptarget"))
        # )
        time.sleep(20)
    def trade(self, driver, symbol_list, limit_price, trade_type, schwab_accounts, mom=False):
        self.login(driver, mom)

        for symbol in symbol_list:
            for i in range(schwab_accounts):
                try:
                    driver.get('https://client.schwab.com/app/trade/tom/#/trade')
                    driver.refresh()
                    time.sleep(1)

                    try:
                        account_dropdown = WebDriverWait(driver, 8).until(
                            EC.presence_of_element_located((By.ID, 'basic-example-small')))
                        account_dropdown.click()
                        time.sleep(1)
                        account = WebDriverWait(driver, 8).until(
                            EC.presence_of_element_located((By.ID, f'basic-example-small-header-0-account-{i}')))
                        account.click()
                        time.sleep(1.5)
                        enter_symbol = driver.find_element(By.ID, '_txtSymbol')
                    except:
                        account_dropdown = WebDriverWait(driver, 8).until(
                            EC.presence_of_element_located((By.ID, 'basic-example-small')))
                        account_dropdown.click()
                        time.sleep(1)
                        account = WebDriverWait(driver, 8).until(
                            EC.presence_of_element_located((By.ID, f'brokerage-acc-{i}')))
                        account.click()
                        time.sleep(1.5)
                        enter_symbol = driver.find_element(By.ID, '_txtSymbol')
                    for letter in symbol:
                        enter_symbol.send_keys(letter)
                        time.sleep(.2)

                    # click_out = driver.find_element(By.XPATH, '//*[@id="aiott-strategy"]')

                    time.sleep(1.5)
                    symbol_from_list = driver.find_element(By.CSS_SELECTOR, f'li[onclick*="{symbol.upper()}"]')
                    symbol_from_list.click()
                    # first_symbol = driver.find_element(By.ID, 'sym-row0')
                    # first_symbol.click()
                    time.sleep(1)

                    action_wait = WebDriverWait(driver, 8).until(
                        EC.visibility_of_element_located((By.ID, '_action')))
                    actions = Select(driver.find_element(By.ID, '_action'))
                    if trade_type.lower() == 'buy':
                        actions.select_by_visible_text('Buy')
                    elif trade_type.lower() == 'sell':
                        try:
                            sell_all_btn = driver.find_element(By.ID, 'mcaio-sellAllHandle')
                        except:
                            continue
                        actions.select_by_visible_text('Sell')

                    time.sleep(.5)

                    if not self.extended_hour:
                        order_type = Select(driver.find_element(By.CLASS_NAME, 'order-type'))
                        order_type.select_by_visible_text('Market')
                    else:
                        limit_price_input = driver.find_element(By.CSS_SELECTOR, '[name="limitPrice"]')
                        limit_price_input.send_keys(limit_price)
                        timing = Select(driver.find_element(By.ID, '_timing'))
                        timing.select_by_visible_text('Day + extended hours')

                    time.sleep(.5)

                    if self.share_amt != 1:
                        shares_input = driver.find_element(By.ID, "ordernumber01inputqty-stepper-input")
                        shares_input.clear()
                        shares_input.send_keys(self.share_amt)
                        time.sleep(.5)

                    # review order
                    review_order_btn = WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="mcaio-footer"]/div/div[2]/button[2]')))
                    driver.execute_script("arguments[0].click();", review_order_btn)

                    time.sleep(.5)

                    place_order_btn = WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((By.ID, 'mtt-place-button')))
                    driver.execute_script("arguments[0].click();", place_order_btn)

                    account_num = WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'sdps-text-l-bold-body')))
                    print(f"{trade_type}:{i} - {account_num.text}")
                    self.tracker.add_success('SCHWAB', str(i), symbol, trade_type)
                    time.sleep(1.5)
                except Exception as e:
                    print(e)
                    self.tracker.add_error('SCHWAB', str(i), symbol, trade_type)