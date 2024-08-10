import streamlit as st
import pandas as pd

from utils.constants import *

def register_page():
    st.title("🖋️ Cadastrar operações, moedas ou corretoras novas")
    st.markdown("Insira as informações nos formulários abaixo...")

    operation_r, coins_r, exchange_r, revenue_r = st.tabs(["Registrar Operação", "Registrar Moeda", "Registrar Corretora", "Registrar Aporte"])

    with operation_r:
        data = st.date_input("Trade date")
        coin = st.selectbox("Select coin", options=st.session_state['coin_sheet']['Nickname'].values, index=False)
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
                price = price * st.session_state['dolar_price']
            else:
                dolar_price = price / st.session_state['dolar_price']

        amount = 0.0
        if price != None and income != None:
            if income_fund:
                income = income * st.session_state['dolar_price']
            amount = income / price

        exchange = st.selectbox("Select Exchange", options=st.session_state['exchange_sheet']['Exchange'].values)

        register = st.button("Register")

        if register:
            if not data or not coin or not price or not income or not status:
                st.warning("Report All Data.")
            else:   
                register_data = pd.DataFrame([{
                    "Data": data.strftime("%d-%m-%Y"),
                    "Coin": coin,
                    "Preço (R$)": price,
                    "Preço (U$)": dolar_price,
                    "Preço Atual (R$)": 0,
                    "Preço Atual (U$)": 0,
                    "Valor Investido (R$)": income,
                    "Qte": amount,
                    "Status": status,
                    "Exchange": exchange
                }])

                updated_df = pd.concat([st.session_state['register_sheet'], register_data], ignore_index=True)

                st.session_state['database'].conn.update(worksheet="DATA", data=updated_df)

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

                updated_df_coin = pd.concat([st.session_state['coin_sheet'], register_data_coin], ignore_index=True)

                st.session_state['database'].conn.update(worksheet="COINS", data=updated_df_coin)

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

                updated_df_exchange = pd.concat([st.session_state['exchange_sheet'], register_data_exchange], ignore_index=True)

                st.session_state['database'].conn.update(worksheet="EXCHANGES", data=updated_df_exchange)

                st.success("Exchange Registed with Success")

    with revenue_r:
        revenue_data = st.date_input("Revenue date")

        revenue_amout = st.number_input("Revenue Amount")

        revenue_exchange = st.selectbox("Revenue Exchange", options=st.session_state['exchange_sheet']['Exchange'].values)

        revenue_ex = st.button("Submit New Revenue")

        if revenue_ex:
            if not revenue_data or not revenue_amout or not revenue_exchange:
                st.warning("Please, insert all values required.")
            else:
                revenue_data_exchange = pd.DataFrame([{
                    "Data": revenue_data,
                    "Amount": revenue_amout,
                    "Exchange": revenue_exchange
                }])

                updated_df_revenue = pd.concat([st.session_state['revenue_sheet'], revenue_data_exchange], ignore_index=True)

                st.session_state['database'].conn.update(worksheet="REVENUE", data=updated_df_revenue)

                st.success("revenue Registed with Success")