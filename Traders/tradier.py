import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TradierTrader:
    def __init__(self, tracker, share_amt):
        self.tracker = tracker
        self.share_amt = share_amt
        self.token = os.getenv("tradier_token")
        self.accounts = os.getenv("tradier_accounts")

    def trade(self, symbol_list, trade_type):
        accounts_list = self.accounts.split(',')
        for symbol in symbol_list:
            for account in accounts_list:
                response = requests.post(f'https://api.tradier.com/v1/accounts/{account}/orders',
                                         data={'class': 'equity', 'symbol': symbol, 'side': trade_type, 'quantity': 1,
                                               'type': 'market', 'duration': 'day'},
                                         headers={'Authorization': f'Bearer {self.token}', 'Accept': 'application/json'}
                                         )
                json_response = response.json()
                print(f"{response.status_code} - {account}")
                #print(json_response)
                if response.status_code == 200:
                    self.tracker.add_success('TRADIER', account, symbol, trade_type)
                else:
                    self.tracker.add_error('TRADIER', account, symbol, trade_type)