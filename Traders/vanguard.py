from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import time
from selenium.webdriver.common.keys import Keys

class VanguardTrader:
    def __init__(self, tracker, share_amt, extended_hour, vanguard_accounts):
        self.tracker = tracker
        self.share_amt = share_amt
        self.extended_hour = extended_hour
        self.vanguard_accounts = vanguard_accounts

    def login(self, driver):
        print('=============  VANGUARD  =============')
        driver.get('https://logon.vanguard.com/logon?site=pi')
        time.sleep(1)
        username_box = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, 'USER')))

        passwordBox = driver.find_element(By.ID, 'PASSWORD-blocked')
        loginBtn = driver.find_element(By.ID, 'username-password-submit-btn-1')

        username_box.send_keys('xchen601')
        time.sleep(2)
        passwordBox.send_keys('Abc26539001qq!')
        time.sleep(2)
        loginBtn.click()
        wait = WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.CLASS_NAME,
                                            'main-content')))
        try:
            loginBtn.click()
            WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.CLASS_NAME,
                                                'main-content')))
            print('logged in to Vanguard')
        except:
            pass
        time.sleep(3)

    def trade(self, driver, symbol_list, limit_price, trade_type):
        self.login(driver)
        if self.extended_hour:
            self.vanguard_trade_extended(driver, symbol_list, limit_price, trade_type)
            return

        if trade_type.lower() == "sell":
            self.vanguard_sell(driver, symbol_list, limit_price)
            return

        for symbol in symbol_list:
            for i in range(self.vanguard_accounts):
                try:
                    # go to trade
                    driver.get(
                        'https://personal.vanguard.com/web/sc1/trade-web/trade/ticket?investmentType=EQUITY&nonRetirementMode=true')

                    # select account
                    accounts_dropdown = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME,
                                                        'account-select-trigger__content'))
                    )
                    accounts_dropdown.click()
                    time.sleep(.5)

                    # click account
                    accounts_list = driver.find_elements(By.TAG_NAME, 'tds-list-option')
                    accounts_list[i].click()

                    #
                    sellBtn = driver.find_element(By.XPATH, f"//label[contains(.,'Sell')]")
                    buyBtn = driver.find_element(By.XPATH, f"//label[contains(.,'Buy')]")

                    if trade_type == 'buy':
                        buyBtn.click()
                    elif trade_type == 'sell':
                        sellBtn.click()

                    symbolInput = driver.find_element(By.ID, "symbol")
                    symbolInput.send_keys(symbol)

                    sharesInput = driver.find_element(By.ID, "amountTypeIsShares")
                    sharesInput.send_keys(self.share_amt)

                    market_btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        f"//label[contains(.,'Market')]"))
                    )
                    market_btn.click()

                    try:
                        costBasis = WebDriverWait(driver, 1).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            '/html/body/twe-root/twe-trade/main/form/div/div[3]/div[1]/fieldset/tds-button-group/div[1]/label[1]'))
                        )
                        costBasis.click()
                    except:
                        pass
                    try:
                        continueBtn = WebDriverWait(driver, .5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR,
                                                            '[data-testid="editCostBasisContinueButton"]'))
                        )
                        continueBtn.click()
                    except:
                        pass
                    try:
                        ok_button = WebDriverWait(driver, .5).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f"//span[contains(.,'OK')]"))
                        )
                        ok_button.click()
                    except:
                        pass
                    # preview order
                    previewBtn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    f"//button[contains(.,'Preview')]"))
                    )

                    previewBtn.click()
                    time.sleep(.1)

                    # Continue if market is closed
                    try:
                        closedContinue = WebDriverWait(driver, 1).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            '/html/body/twe-root/main/twe-trade/twe-alert-error-modal/tds-modal[1]/div[1]/div/div[2]/tds-modal-footer/div/button[2]'))
                        )
                        closedContinue.click()
                    except:
                        pass

                    # submit order
                    submitBtn = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        '/html/body/twe-root/main/twe-preview/div/div/div[2]/tds-card/div/tds-card-body/div/button[2]'))
                    )

                    submitBtn.click()

                    # confirm order
                    orderReceived = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '/html/body/twe-root/main/twe-confirm/div/div/div[2]/h2'))
                    )

                    print(orderReceived.text)
                    if "Received" in orderReceived.text:
                        self.tracker.add_success('VANGUARD', str(i), symbol, trade_type)
                    else:
                        self.tracker.add_error('VANGUARD', str(i), symbol, trade_type)
                except Exception as e:
                    self.tracker.add_error('VANGUARD', str(i), symbol, trade_type)
                    try:
                        print(e)
                        time.sleep(1)
                    except:
                        pass

    def vanguard_trade_extended(self, driver, symbol_list, limit_price, trade_type):
        for symbol in symbol_list:
            for i in range(self.vanguard_accounts):
                try:
                    # go to trade
                    driver.get(
                        'https://personal.vanguard.com/us/TradeTicket?accountId=971425103021846&investmentType=EQUITY&extendedHours=true')

                    # select account
                    accounts_dropdown = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID,
                                                        'baseForm:accountSelectOne_text'))
                    )
                    accounts_dropdown.click()
                    time.sleep(.5)

                    account = driver.find_element(By.ID, f"baseForm:accountSelectOne:{i + 1}")
                    account.click()

                    if trade_type.lower() == "buy":
                        buy_button = driver.find_element(By.ID, "baseForm:transactionTypeSelectOne:1")
                        buy_button.click()
                    else:
                        sell_button = driver.find_element(By.ID, "baseForm:transactionTypeSelectOne:2")
                        sell_button.click()

                    symbol_input = driver.find_element(By.ID, "baseForm:investmentTextField")
                    symbol_input.send_keys(symbol)

                    shares_input = driver.find_element(By.ID, "baseForm:shareQuantityTextField")
                    shares_input.send_keys(self.share_amt)

                    limit_button = driver.find_element(By.ID, "baseForm:orderTypeSelectOne:2")
                    limit_button.click()

                    limit_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID,
                                                        'baseForm:limitPriceTextField'))
                    )
                    limit_input.send_keys(limit_price)

                    day_duration_button = driver.find_element(By.ID, "baseForm:durationTypeSelectOne:1")
                    day_duration_button.click()

                    continue_button = driver.find_element(By.ID, "baseForm:reviewButtonInput")
                    continue_button.click()

                    submit_order = driver.find_element(By.ID, "baseForm:submitButtonInput")
                    # submit_order.click()



                except Exception as e:
                    print(e)

    def vanguard_sell(self, driver, symbol_list, limit_price):
        for symbol in symbol_list:
            for i in range(self.vanguard_accounts):
                try:
                    # go to trade
                    driver.get(
                        'https://personal.vanguard.com/us/TradeTicket?investmentType=EQUITY')

                    try:
                        ok_btn = WebDriverWait(driver, 2).until(
                            EC.presence_of_element_located((By.ID,
                                                            'okButtonInput'))
                        )
                        ok_btn.click()
                    except:
                        pass

                    # select account
                    accounts_dropdown = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID,
                                                    'baseForm:accountSelectOne_main'))
                    )
                    accounts_dropdown.click()
                    time.sleep(1)

                    account = driver.find_element(By.ID, f"baseForm:accountSelectOne:{i + 1}")
                    account.click()

                    time.sleep(1.5)
                    transactionType = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID,
                                                    'baseForm:transactionTypeSelectOne_textCont'))
                    )
                    transactionType.click()
                    time.sleep(.5)
                    sell_button = driver.find_element(By.ID, "baseForm:transactionTypeSelectOne:2")
                    sell_button.click()
                    time.sleep(.5)

                    symbol_input = driver.find_element(By.ID, "baseForm:investmentTextField")
                    symbol_input.send_keys(symbol)
                    symbol_input.send_keys(Keys.ENTER)
                    time.sleep(1)

                    shares_input = driver.find_element(By.ID, "baseForm:shareQuantityTextField")
                    shares_input.send_keys(self.share_amt)
                    time.sleep(1)

                    order_type_btn = driver.find_element(By.ID, "baseForm:orderTypeSelectOne_text")
                    order_type_btn.click()
                    time.sleep(.5)

                    market_button = driver.find_element(By.ID, "baseForm:orderTypeSelectOne:1")
                    market_button.click()
                    time.sleep(1.5)

                    try:
                        cost_basis = driver.find_element(By.ID, "baseForm:costBasisMethodSelectOne_main")
                        cost_basis.click()
                        time.sleep(1)

                        FIFO_btn = driver.find_element(By.ID, "baseForm:costBasisMethodSelectOne:2")
                        FIFO_btn.click()
                        time.sleep(1)
                    except:
                        pass

                    continue_button = driver.find_element(By.ID, "baseForm:reviewButton")
                    continue_button.click()
                    time.sleep(1)

                    submit_order = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID,
                                                    "baseForm:submitButtonInput"))
                    )
                    submit_order.click()
                    time.sleep(2)
                    self.tracker.add_error("VANGUARD", str(i), symbol, "sell")



                except Exception as e:
                    try:
                        ok_btn = driver.find_element(By.ID, "yui_3_4_0_1_1685120738850_383")
                        ok_btn.click()
                    except:
                        try:
                            Alert(driver).accept()
                        except:
                            print("Failed to handle the alert")
                    driver.get("https://personal.vanguard.com/us/TradeTicket?investmentType=EQUITY")
                    time.sleep(2)
                    self.tracker.add_error('VANGUARD', str(i), symbol, "sell")
