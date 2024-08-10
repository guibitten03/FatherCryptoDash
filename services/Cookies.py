import streamlit as st
from dotenv import dotenv_values

from services.Database import Database
from services.Coinmarketcap import CoinMarketCap
from services.FiatPrice import FiatPrices


class Cookies:
    def __init__(self) -> None:
        if 'config' not in st.session_state:
            st.session_state['config'] = dotenv_values(".env")


    def database_cookie(self):
        if 'database' not in st.session_state:
            try:
                st.session_state['database'] = Database(worksheets=[
                    ("DATA", 10),
                    ("COINS", 2),
                    ("EXCHANGES", 1),
                    ("REVENUE", 3)
                ])
                st.session_state['register_sheet'] = st.session_state['database'].worksheets["DATA"].dropna(how="all")
                st.session_state['coin_sheet'] = st.session_state['database'].worksheets["COINS"].dropna(how="all")
                st.session_state['exchange_sheet'] = st.session_state['database'].worksheets["EXCHANGES"].dropna(how="all")
                st.session_state['revenue_sheet'] = st.session_state['database'].worksheets["REVENUE"].dropna(how="all")

                print("Database connected!")

            except Exception as e:
                print(f"There is no possible connect with database. ERROR: {e}")

            
    def coinmarketcap_cookie(self):
        if 'cmc' not in st.session_state:
            try:
                st.session_state['cmc'] = CoinMarketCap(st.session_state['config'].get("MARKET_CAP_AP_KEY"))

                print("CoinMarketCap connected!")

            except Exception as e:
                print(f"There is no possible connect with CoinMarketCap. ERROR: {e}")
                

    def fiatprices_cookie(self):
        if 'fiat_price' not in st.session_state:
            try:
                st.session_state['fiat_price'] = FiatPrices()
                st.session_state['dolar_price'] = st.session_state['fiat_price'].get_fiat_price()

                print("Fiat Price connected!")

            except Exception as e:
                print(f"There is no possible connect with FiatPrice. ERROR: {e}")
