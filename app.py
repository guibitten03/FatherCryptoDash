from library import *
from utils.constants import *
from services.Database import Database
from services.Coinmarketcap import CoinMarketCap
from services.FiatPrice import FiatPrices
import json

import streamlit_card as st_card

st.set_page_config(layout="wide")

# ======= DATABASE IMPORT ======= #
database = Database(worksheets=[
    ("DATA", 10),
    ("COINS", 2),
    ("EXCHANGES", 1)
])

cmc = CoinMarketCap(MARKET_CAP_AP_KEY)

# fp = FiatPrices()
# dolar_price_in_real = fp.get_fiat_price()
# if dolar_price_in_real == 0.0:
#     dolar_price_in_real = 5
dolar_price_in_real = 5

# config = dotenv_values('.env')
# binance = Binance(config.get('KEY'), config.get('SECRET_KEY'))

register_sheet = database.worksheets["DATA"].dropna(how="all")
coin_sheet = database.worksheets["COINS"].dropna(how="all")
exchange_sheet = database.worksheets["EXCHANGES"].dropna(how="all")

# ======= =============== ======= #

# ======= INPUT DATA ======= #
 
st.title("📊 Análise de Transações")

btn_1, btn_2 = st.columns(2, gap="medium")

with btn_1:
    st.link_button("Acesse a planilha de operações", url=SHEET_LINK)

with btn_2:
    update_price_coins = st.button("Atualizar preço das moedas")

if update_price_coins:
    coins_to_update_price = register_sheet['Coin'].drop_duplicates(keep="first").values

    current_prices = []
    for coin_to_up in coins_to_update_price:
        data = cmc.get_coin_price(coin=coin_to_up)
        currrent_coin_price = json.loads(data)['data'][coin_to_up][0]['quote']['USD']['price']
        current_prices.append(currrent_coin_price)

    coins_price = {coins_to_update_price[i]: current_prices[i] for i in range(len(current_prices))}

    coin_price_mapped = [coins_price[coin_to_map] for coin_to_map in register_sheet['Coin'].values]

    register_sheet['Preço Atual (U$)'] = coin_price_mapped
    register_sheet['Preço Atual (R$)'] = [i * DOLAR_PRICE for i in coin_price_mapped]

    database.conn.update(worksheet="DATA", data=register_sheet)

    st.success("Valores das moedas atualizadas com sucesso!")


input_c1, input_c2 = st.columns(2, gap="medium")

with input_c1:
    exchange = st.selectbox("Selecione a Corretora", options=exchange_sheet['Exchange'].values)

with input_c2:
    coin = st.selectbox("Selecione a Moeda", options=coin_sheet['Nickname'].values, index=False)

st.divider()

# ======= =============== ======= #

exchange_filtered = register_sheet[register_sheet['Exchange'] == exchange]

line_filtered_df = exchange_filtered[(exchange_filtered['Coin'] == coin) & (exchange_filtered['Status'] == "Buy")]

# @GUARD-CLAUSE
if len(line_filtered_df) == 0: 
    st.markdown(f"<h1 style='text-align: center;' >🔴 Não existe transações da moeda {coin} na corretora {exchange} 🔴</h1>", unsafe_allow_html=True)
    
else:
    mean_price = line_filtered_df['Valor Investido (R$)'].sum() / line_filtered_df['Qte'].sum()

    line_filtered_df['Mean Price'] = [mean_price for x in range(line_filtered_df.shape[0])]

    card_col_1, card_col_2, card_col_3 = st.columns(3, gap="small")

    card_style = {
        "card":{
            "width": "100%",
            "height": "100px",
            "border-radius": "10px",
            "box-shadow": "0 0 10px rgba(218,165,32,0.5)",
        },
    }


    with card_col_1:
        dollar_mean_price = st_card.card(
            title = "%.10f $" % (line_filtered_df['Mean Price'].iloc[0] / dolar_price_in_real),
            text = "Preço Médio em Dólar",
            styles=card_style
        )

    with card_col_2:
        real_mean_price = st_card.card(
            title = "%.10f R$" % (line_filtered_df['Mean Price'].iloc[0]),
            text = "Preço Médio em Real",
            styles=card_style
        )  

    with card_col_3:
        dolar_price = st_card.card(
            title = f"{dolar_price_in_real} R$",
            text = "Preço Dolar em Real",
            styles=card_style
        )  


    c1, c2 = st.columns(2, gap="small")

    with c1:
        line_purchase = go.Scatter(x=line_filtered_df['Data'], y=line_filtered_df['Preço (R$)'], name='Preços de Compra', mode='lines')
        line_mean = go.Scatter(x=line_filtered_df['Data'], y=line_filtered_df['Mean Price'], name='Preço Médio', mode='lines')

        layout = go.Layout(
            title='Histórico de Compras e Preço Médio de Compra',
            xaxis=dict(title='Data'),
            yaxis=dict(title='Price (R$)'),
            hovermode='closest',
            margin=dict(l=20, r=20, b=20, t=40),
            showlegend=True,
            dragmode='pan',
            uirevision='none',
        )

        fig = go.Figure(data=[line_purchase, line_mean], layout=layout)
        with st.container(border=True):
            st.plotly_chart(fig)

    bar_filtered_df = register_sheet[(register_sheet['Coin'] == coin)]
    bar_filtered_df = bar_filtered_df.groupby(by="Status")['Valor Investido (R$)'].sum().reset_index()

    with c2:
        bar_purchase = go.Bar(x=['Buy'], y=bar_filtered_df[['Valor Investido (R$)']].iloc[0,:], name='Purchase', marker=dict(color='red'))

        try:
            bar_sellof = go.Bar(x=['Sell'], y=bar_filtered_df[['Valor Investido (R$)']].iloc[1,:], name='Sale', marker=dict(color='green'))

            layout = go.Layout(
                title='Valor (R$) Total Comprado e Vendido',
                xaxis=dict(title='Coin'),
                yaxis=dict(title='Values'),
                barmode='group', 
                margin=dict(l=20, r=20, b=20, t=40),
                legend=dict(orientation='h'), 
            )

            fig = go.Figure(data=[bar_purchase, bar_sellof], layout=layout)
        except:
            fig = go.Figure(data=[bar_purchase], layout=layout)

        with st.container(border=True):
            st.plotly_chart(fig)


    
