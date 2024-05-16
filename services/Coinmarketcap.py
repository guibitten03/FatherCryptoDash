from requests import Request, Session
import json

class CoinMarketCap:
    def __init__(self, api_key:str=""):
        
        self.api_key = api_key

    
    def get_coin_price(self, url="https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest", coin="BTC", convert="USD"):
        parameters = {
            'symbol': coin,
            'convert': convert
        }

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            return response.text
        except Exception as e:
            print(e)
            return 
