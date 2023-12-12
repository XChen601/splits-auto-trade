import undetected_chromedriver.v2 as uc

from SplitsUpdated.Traders.tracker import Tracker
from SplitsUpdated.Traders.schwab import SchwabTrader
from SplitsUpdated.Traders.fidelity import FidelityTrader
from SplitsUpdated.Traders.vanguard import VanguardTrader
from SplitsUpdated.Traders.firstrade import FirstradeTrader
from SplitsUpdated.Traders.tastytrade import TastyTrader
from SplitsUpdated.Traders.tradier import TradierTrader
from SplitsUpdated.Traders.stocktwits import StocktwitsTrader
from SplitsUpdated.Traders.chase import ChaseTrader
from SplitsUpdated.Traders.ally import AllyTrader
from SplitsUpdated.Traders.wells import WellsTrader

PATH = "/ReverseSplits/chromedriver.exe"
SHARE_AMT = 1
EXTENDED_HOUR = False

schwab_accounts = 24
fid_accounts = 46
vanguard_accounts = 33
chase_accounts = ["7104", "5761", "8327", "6540"]
ally_accounts = 15
mom_accounts = 13

def new_driver(driver):
    driver.quit()
    options = uc.ChromeOptions()
    driver = uc.Chrome(driver_executable_path=PATH, use_subprocess=True, options=options)
    return driver

def sell_day_ones(driver, symbol_list, limit_price, trade_type="sell"):
    schwab_trader.trade(driver, symbol_list, limit_price, trade_type, schwab_accounts)
    fidelity_trader.trade(driver, symbol_list, limit_price, trade_type)
    vanguard_trader.trade(driver, symbol_list, limit_price, trade_type)
    firstrade_trader.trade(driver, symbol_list, limit_price, trade_type)
    tasty_trader.trade(driver, symbol_list, limit_price, trade_type)
    tradier_trader.trade(symbol_list, trade_type)
    wells_trader.trade(driver, symbol_list, limit_price, trade_type)
    # total accounts = 23 + 10 + 9 + 13 + 10 = 65


if __name__ == "__main__":
    tracker = Tracker()

    print('-------------- ALL --------------')
    symbols = input("Ticker symbol: ")
    limit_price = input('Limit price: ')
    trade_type = input('"buy" or "sell": ')

    symbol_list = symbols.replace(" ", "").split(',')

    options = uc.ChromeOptions()
    driver = uc.Chrome(driver_executable_path=PATH, use_subprocess=True, options=options)

    schwab_trader = SchwabTrader(tracker, SHARE_AMT, EXTENDED_HOUR)
    fidelity_trader = FidelityTrader(tracker, SHARE_AMT, EXTENDED_HOUR, fid_accounts)
    vanguard_trader = VanguardTrader(tracker, SHARE_AMT, EXTENDED_HOUR, vanguard_accounts)
    firstrade_trader = FirstradeTrader(tracker, SHARE_AMT, EXTENDED_HOUR)
    tasty_trader = TastyTrader(tracker, SHARE_AMT, EXTENDED_HOUR)
    tradier_trader = TradierTrader(tracker, SHARE_AMT)
    stocktwits_trader = StocktwitsTrader(tracker)
    chase_trader = ChaseTrader(tracker, SHARE_AMT, EXTENDED_HOUR, chase_accounts)
    ally_trader = AllyTrader(tracker, SHARE_AMT, EXTENDED_HOUR, ally_accounts)
    wells_trader = WellsTrader(tracker, SHARE_AMT)

    #fidelity_trader.trade(driver, symbol_list, limit_price, trade_type)
    vanguard_trader.trade(driver, symbol_list, limit_price, trade_type)
    schwab_trader.trade(driver, symbol_list, limit_price, trade_type, schwab_accounts)
    firstrade_trader.trade(driver, symbol_list, limit_price, trade_type)
    tasty_trader.trade(driver, symbol_list, limit_price, trade_type)
    tradier_trader.trade(symbol_list, trade_type)
    driver = new_driver(driver)
    schwab_trader.trade(driver, symbol_list, limit_price, trade_type, mom_accounts, mom=True)
    chase_trader.trade(driver, symbol_list, limit_price, trade_type)
    ally_trader.trade(driver, symbol_list, limit_price, trade_type)
    wells_trader.trade(driver, symbol_list, limit_price, trade_type)

    #sell_day_ones(driver, symbol_list, limit_price, trade_type)



    print(f"Total Successes: {tracker.get_successes()}")
    print(f"Error List: {tracker.get_errors()}")

