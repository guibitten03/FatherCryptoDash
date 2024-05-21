import requests

class FiatPrices:
    def __init__(self):
        self.url = 'https://economia.awesomeapi.com.br/json/last/{}'


    def get_fiat_price(self, fiat_coin_pair_1:str = "USD", fiat_coin_pair_2:str = "BRL"):
        fiat_coin_pair_1 = fiat_coin_pair_1.upper()
        fiat_coin_pair_2 = fiat_coin_pair_2.upper()

        response = requests.get(url=self.url.format(fiat_coin_pair_1 + "-" + fiat_coin_pair_2))
        data = response.json()

        price = 0.0
        if data[fiat_coin_pair_1+fiat_coin_pair_2]:
            price = data[fiat_coin_pair_1+fiat_coin_pair_2]['high']
            
    
        return float(price)