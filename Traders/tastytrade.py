from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time
import os


class TastyTrader:
    def __init__(self, tracker, share_amt, extended_hour):
        self.tracker = tracker
        self.share_amt = share_amt
        self.extended_hour = extended_hour

    def login(self, driver):
        load_dotenv()
        tastyworks_username = os.getenv('TASTYWORKS_USERNAME')
        tastyworks_password = os.getenv('TASTYWORKS_PASSWORD')

        driver.get('https://trade.tastyworks.com/login/index.html')
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ember388')))
        password_input = driver.find_element(By.ID, 'ember391')

        username_input.send_keys(tastyworks_username)
        password_input.send_keys(tastyworks_password)

        login_btn = driver.find_element(By.ID, 'ember394')
        login_btn.click()
        time.sleep(1)

    def trade(self, driver, symbol_list, limit_price, trade_type):
        self.login(driver)
        driver.get('https://trade.tastyworks.com/index.html#/homePage')
        try:
            # Wait until the element is available and locate it
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".wb2-notice-close-button .close-popup"))
            )
            time.sleep(1)
            # Perform an action (e.g., click) on the element
            element.click()
            time.sleep(1)
        except:
            pass
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/header/dl[1]/dd/select')))
        accounts_list = Select(driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/header/dl[1]/dd/select'))

        for symbol in symbol_list:
            symbol = symbol.upper()
            for account in range(len(accounts_list.options)):
                try:
                    # trade
                    driver.get('https://trade.tastyworks.com/index.html#/homePage')

                    try:
                        print('test')
                        # Wait until the element is available and locate it
                        element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".wb2-notice-close-button .close-popup"))
                        )
                        print('test2')
                        time.sleep(1)
                        # Perform an action (e.g., click) on the element
                        element.click()
                        time.sleep(1)
                    except:
                        pass

                    accounts_dropdown = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'account-selector')))
                    accounts_dropdown.click()

                    accounts_list = Select(
                        driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/header/dl[1]/dd/select'))
                    time.sleep(1)
                    accounts_list.select_by_index(account)
                    time.sleep(1)

                    trade_btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[2]/div[1]/nav/a[1]/i')))

                    trade_btn.click()

                    time.sleep(1)
                    symbol_input = driver.find_element(By.XPATH,
                                                       '/html/body/div/div[1]/div[3]/div/div/section/div/header/div[1]/div/div/div/input')
                    symbol_input.click()
                    time.sleep(1)

                    if account == 0:
                        for i in range(6):
                            symbol_input.send_keys(Keys.BACKSPACE)

                        for letter in symbol:
                            symbol_input.send_keys(letter)
                            time.sleep(.1)
                        time.sleep(1)

                        options_list = driver.find_element(By.XPATH,
                                                           '/html/body/div/div[1]/div[3]/div/div/section/div/header/div[1]/div/ul')
                        first_item = options_list.find_elements(By.TAG_NAME, 'li')[0]
                        first_item.click()
                    time.sleep(1)

                    sell_btn = driver.find_element(By.XPATH, value=f"//button[contains(.,'Sell')]")
                    buy_btn = driver.find_element(By.XPATH, value=f"//button[contains(.,'Buy')]")

                    if trade_type.lower() == 'buy':
                        buy_btn.click()
                    elif trade_type.lower() == 'sell':
                        sell_btn.click()
                    time.sleep(.5)

                    quantity_input = driver.find_element(By.XPATH,
                                                         '/html/body/div/div[1]/div[3]/div/div/section/div/section[1]/fieldset[1]/div[2]/div[1]/input')
                    quantity_input.clear()
                    quantity_input.send_keys(self.share_amt)
                    time.sleep(.5)

                    if not self.extended_hour:
                        market_btn = driver.find_element(By.XPATH,
                                                         '/html/body/div/div[1]/div[3]/div/div/section/div/section[1]/fieldset[2]/div[1]/button')
                        market_btn.click()
                    else:
                        # extended hour
                        extended_hour_btn = driver.find_element(By.XPATH,
                                                                "/html/body/div/div[1]/div[3]/div/div/section/div/section[1]/fieldset[3]/div[3]/button")
                        extended_hour_btn.click()
                    time.sleep(.5)

                    review_order_btn = driver.find_element(By.XPATH,
                                                           '/html/body/div/div[1]/div[3]/div/div/section/div/footer/button')
                    review_order_btn.click()
                    time.sleep(1)

                    send_order_btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '/html/body/div/div[1]/div[3]/div/div/section/div/footer/button')))
                    send_order_btn.click()
                    time.sleep(1.5)

                    self.tracker.add_success('TASTYWORKS', account, symbol, trade_type)

                except:
                    self.tracker.add_error('TASTYWORKS', account, symbol, trade_type)