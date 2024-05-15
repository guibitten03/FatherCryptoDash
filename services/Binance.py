import json
import websocket
from binance import Client

class Binance:
    def __init__(self, api_key: str = "", api_secret: str = ""):
        if not all([api_key, api_secret]):
            raise ValueError("Please, submit your correct api and secret key.")
        
        self.client = Client(api_key, api_secret)


    # def get_balances(self):