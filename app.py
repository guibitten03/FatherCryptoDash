from library import *
from utils.constants import *
from services.Database import Database
# from services.Binance import Binance

import streamlit_card as st_card

st.set_page_config(layout="wide")

# ======= DATABASE IMPORT ======= #
database = Database(worksheets=[
    ("DATA", 9),
    ("COINS", 2),
    ("EXCHANGES", 1)
])

register_sheet = database.worksheets["DATA"].dropna(how="all")
coin_sheet = database.worksheets["COINS"].dropna(how="all")
exchange_sheet = database.worksheets["EXCHANGES"].dropna(how="all")

# ======= =============== ======= #

# ======= INPUT DATA ======= #
 
st.title("📊 Transactions Analysis")

input_c1, input_c2 = st.columns(2, gap="medium")

with input_c1:
    exchange = st.selectbox("Select Exchange", options=exchange_sheet['Exchange'].values)

with input_c2:
    coin = st.selectbox("Select Coin", options=coin_sheet['Nickname'].values, index=False)

st.divider()

# ======= =============== ======= #

exchange_filtered = register_sheet[register_sheet['Exchange'] == exchange]

line_filtered_df = exchange_filtered[(exchange_filtered['Coin'] == coin) & (exchange_filtered['Status'] == "Buy")]

# @GUARD-CLAUSE
if len(line_filtered_df) == 0: 
    st.markdown(f"<h1 style='text-align: center;' >🔴 There is not transactions of coin {coin} in exchange {exchange} 🔴</h1>", unsafe_allow_html=True)
    
else:
    mean_price = line_filtered_df['Income'].sum() / line_filtered_df['Amount'].sum()

    line_filtered_df['Mean Price'] = [mean_price for x in range(line_filtered_df.shape[0])]

    card_col_1, card_col_2 = st.columns(2, gap="small")

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
            title = "%.10f $" % (line_filtered_df['Mean Price'].iloc[0] / 5),
            text = "Dollar Mean Price",
            styles=card_style
        )

    with card_col_2:
        real_mean_price = st_card.card(
            title = "%.10f R$" % (line_filtered_df['Mean Price'].iloc[0]),
            text = "Real Mean Price",
            styles=card_style
        )

    c1, c2 = st.columns(2, gap="small")

    with c1:
        line_purchase = go.Scatter(x=line_filtered_df['Data'], y=line_filtered_df['Price (R$)'], name='Purchase Price', mode='lines')
        line_mean = go.Scatter(x=line_filtered_df['Data'], y=line_filtered_df['Mean Price'], name='Mean Price', mode='lines')

        layout = go.Layout(
            title='Purchase History and Mean Price',
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
    bar_filtered_df = bar_filtered_df.groupby(by="Status")['Income'].sum().reset_index()

    with c2:
        bar_purchase = go.Bar(x=['Buy'], y=bar_filtered_df[['Income']].iloc[0,:], name='Purchase', marker=dict(color='red'))

        try:
            bar_sellof = go.Bar(x=['Sell'], y=bar_filtered_df[['Income']].iloc[1,:], name='Sale', marker=dict(color='green'))

            layout = go.Layout(
                title='Purchase and Sale Volum',
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

