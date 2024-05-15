from library import *
from utils.constants import *
from services.Database import Database
from services.Style import Style

import datetime

st.set_page_config(layout="wide")

st.title("🖋️ Crypto Currency Formulary")
st.markdown("Insert Trade Information Bellow...")

style = Style("assets/style.css")
style._connect()

database = Database(worksheets=[
    ("DATA", 9),
    ("COINS", 2),
    ("EXCHANGES", 1)
])



register_sheet = database.worksheets["DATA"].dropna(how="all")
coin_sheet = database.worksheets["COINS"].dropna(how="all")
exchange_sheet = database.worksheets["EXCHANGES"].dropna(how="all")

operation_r, coins_r, exchange_r = st.tabs(["Register Operation", "Register Coin", "Register Exchange"])

with operation_r:
    data = st.date_input("Trade date")
    time = st.time_input("Trade time", step=60)
    coin = st.selectbox("Select coin", options=coin_sheet['Nickname'].values, index=False)
    price = st.number_input("Coin Price", step=0.01, format="%.10f", value=None)
    income = st.number_input("Value Invested", step=0.01, value=None)

    c1, c2 = st.columns(2, gap="small")

    with c1:
        status = st.selectbox("Operation", options=OPS, index=False)

    with c2:
        price_fund = st.toggle("Price in Dollar?")
        income_fund = st.toggle("Income in Dollar?")

    dolar_price = 0.0
    if price != None:
        if price_fund:
            dolar_price = price
            price = price * 5
        else:
            dolar_price = price / 5

    amount = 0.0
    if price != None and income != None:
        amount = income / price
        if income_fund:
            income = income * 5

    exchange = st.selectbox("Select Exchange", options=EXCHANGES)

    register = st.button("Register")

    if register:
        if not data or not time or not coin or not price or not income or not status:
            st.warning("Report All Data.")
        else:   
            register_data = pd.DataFrame([{
                "Data": data.strftime("%d-%m-%Y"),
                "Time": time,
                "Coin": coin,
                "Price (R$)": price,
                "Price ($)": dolar_price,
                "Income": income,
                "Amount": amount,
                "Status": status,
                "Exchange": exchange
            }])

            updated_df = pd.concat([register_sheet, register_data], ignore_index=True)

            database.conn.update(worksheet="DATA", data=updated_df)

            st.success("Trade Registed with Success!")

with coins_r:
    coin_r = st.text_input("Insert a New Coin")
    coin_nickname = st.text_input("Insert Coin Nickname")

    register_coin = st.button("Submit New Coin")

    if register_coin:
        if not coin_r:
            st.warning("Report All Data.")
        else:
            register_data_coin = pd.DataFrame([{
                "Coin": coin_r,
                "Nickname": coin_nickname
            }])

            updated_df_coin = pd.concat([coin_sheet, register_data_coin], ignore_index=True)

            database.conn.update(worksheet="COINS", data=updated_df_coin)

            st.success("Coin Registed with Success")

with exchange_r:
    ex_r = st.text_input("Insert New Exchange")

    register_ex = st.button("Submit New Exchange")

    if register_ex:
        if not ex_r:
            st.warning("Insert Some Exchange.")
        else:
            register_data_exchange = pd.DataFrame([{
                "Exchange": ex_r
            }])

            updated_df_exchange = pd.concat([exchange_sheet, register_data_exchange], ignore_index=True)

            database.conn.update(worksheet="EXCHANGES", data=updated_df_exchange)

            st.success("Exchange Registed with Success")