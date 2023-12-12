import requests
import json

class StocktwitsTrader:
    def __init__(self, tracker):
        self.tracker = tracker
    def singleTradeStocktwits(self, symbol, trade_type):
        trade_type = trade_type.lower()
        symbol = symbol.upper()
        url = "https://trade-api.stinvest.co/api/v1/trading/orders"

        payload = json.dumps({
            "asset_class": "equities",
            "is_notional": True,
            "limit_price": "",
            "notional": None,
            "order_expire_time": None,
            "order_type": "market",
            "quantity": "1",
            "stop_price": "",
            "symbol": symbol,
            "time_in_force": "DAY",
            "transaction_type": trade_type
        })
        headers = {
            'authority': 'trade-api.stinvest.co',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'authorization': 'Bearer 8f76425a57fed16b8c820390ee942adbf1fb8ac5',
            'content-type': 'application/json',
            'origin': 'https://stocktwits.com',
            'referer': 'https://stocktwits.com/',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'x-order-tag-origin': 'web',
            'x-order-tag-widget': 'trade-ticket'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            self.tracker.add_success('Stocktwits', symbol, trade_type)
        else:
            self.tracker.add_error('Stocktwits', symbol, trade_type)

    def stocktwits_trade(self, symbols, trade_type):
        symbols = symbols.split(',')
        for symbol in symbols:
            self.singleTradeStocktwits(symbol, trade_type)