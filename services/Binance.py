from binance import Client
import pandas as pd
from datetime import datetime, timedelta

class Binance:
    def __init__(self, api_key: str = "", api_secret: str = ""):
        if not all([api_key, api_secret]):
            raise ValueError("Please, submit your correct api and secret key.")
        
        self.client = Client(api_key, api_secret)
        self.account = self.client.get_account()

    def get_price(self, coin_pair_1: str = "BTC", coin_pair_2: str = "USDT"):
        coin_pair_1 = coin_pair_1.upper()
        coin_pair_2 = coin_pair_2.upper()

        coin_pair = coin_pair_1 + coin_pair_2

        avg_price = self.client.get_avg_price(symbol=coin_pair)
        return avg_price

    def get_balance(self, coin: str = "BTC"):
        coin = coin.upper()

        balance = self.client.get_asset_balance(asset=coin)
        return balance
    
    def get_fees(self, coin_pair_1: str = "BTC", coin_pair_2: str = "USDT"):
        coin_pair_1 = coin_pair_1.upper()
        coin_pair_2 = coin_pair_2.upper()

        coin_pair = coin_pair_1 + coin_pair_2

        fee = self.client.get_trade_fee(symbol=coin_pair)
        return fee
    
    def get_trades(self, coin_pair_1: str = "BTC", coin_pair_2: str = "USDT"):
        coin_pair_1 = coin_pair_1.upper()
        coin_pair_2 = coin_pair_2.upper()

        coin_pair = coin_pair_1 + coin_pair_2

        history_trades = self.client.get_my_trades(symbol=coin_pair)
        return history_trades
    
    def get_historical_stocks(self, 
                              coin_pair_1: str = "BTC", 
                              coin_pair_2: str = "USDT", 
                              interval:str = "day", 
                              range_in_days:int = 360):
        interval_map = {
            "day": self.client.KLINE_INTERVAL_1DAY,
        }

        coin_pair_1 = coin_pair_1.upper()
        coin_pair_2 = coin_pair_2.upper()

        coin_pair = coin_pair_1 + coin_pair_2

        end = datetime.now()
        end = end - timedelta(days=0)
        start = end - timedelta(days=range_in_days)
        start = start.strftime('%d %b, %Y')
        end = end.strftime('%d %b, %Y')

        klines = self.client.get_historical_klines(
            'BTCUSDT', interval_map[interval], start
        )

        data = pd.DataFrame(
            data=[row[1:7] for row in klines],
            columns=['open', 'high', 'low', 'close', 'volume', 'time']
        ).set_index('time')

        data.index = pd.to_datetime(data.index + 1, unit='ms')

        data = data.sort_index()
        data = data.apply(pd.to_numeric, axis=1)

        return data