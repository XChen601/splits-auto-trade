import winsound

class Tracker:
    def __init__(self):
        self.successes = 0
        self.error_list = {}

    def add_success(self, broker_name, account_num, symbol, trade_type):
        print(f"{broker_name} | {trade_type} {symbol} on account {account_num}")
        self.successes += 1

    def add_error(self, broker_name, account_num, symbol, trade_type):
        print(f"{broker_name} | [{trade_type}] ERROR on account {account_num} for {symbol}")
        if broker_name not in self.error_list:
            self.error_list[broker_name] = [account_num]
        else:
            self.error_list[broker_name].append(account_num)
        winsound.Beep(1000, 1000)

    def get_successes(self):
        return self.successes

    def get_errors(self):
        return self.error_list
