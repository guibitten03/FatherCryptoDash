import streamlit as st
import json
import plotly.graph_objects as go
import pandas as pd

from utils.functions import get_amount_coins
from utils.constants import *


def home_page():
    st.title("📊 Análise de Transações")

    with st.sidebar:

        st.divider()

        input_c1, input_c2 = st.columns(2, gap="medium")

        with input_c1:
            exchange = st.selectbox("Selecione a Corretora", options=st.session_state['exchange_sheet']['Exchange'].values, index=False)

        with input_c2:
            coin = st.selectbox("Selecione a Moeda", options=st.session_state['coin_sheet']['Nickname'].values, index=False)

        st.divider()

        st.markdown("Utilize o botão abaixo para atualizar o preço atual de todas as moedas 👇")

        update_price_coins = st.button("Atualizar preço das moedas")

        if update_price_coins:
            coins_to_update_price = st.session_state['register_sheet']['Coin'].drop_duplicates(keep="first").values

            current_prices = []
            for coin_to_up in coins_to_update_price:

                data = st.session_state['cmc'].get_coin_price(coin=coin_to_up)
                currrent_coin_price = json.loads(data)['data'][coin_to_up][0]['quote']['USD']['price']
                current_prices.append(currrent_coin_price)

                # try:
                #     data = st.session_state['cmc'].get_coin_price(coin=coin_to_up)
                #     currrent_coin_price = json.loads(data)['data'][coin_to_up][0]['quote']['USD']['price']
                #     current_prices.append(currrent_coin_price)
                # except Exception as e:
                #     current_prices.append(1)

            coins_price = {coins_to_update_price[i]: current_prices[i] for i in range(len(current_prices))}

            coin_price_mapped = [coins_price[coin_to_map] for coin_to_map in st.session_state['register_sheet']['Coin'].values]

            st.session_state['register_sheet']['Preço Atual (U$)'] = coin_price_mapped
            st.session_state['register_sheet']['Preço Atual (R$)'] = [i * st.session_state['dolar_price'] for i in coin_price_mapped]

            st.session_state['database'].conn.update(worksheet="DATA", data=st.session_state['register_sheet'])

            st.success("Valores das moedas atualizadas com sucesso!")

    tab1, tab2 = st.tabs(["Análise de Preço", "Análise de Performante"])

    # ======= =============== ======= #

    exchange_filtered = st.session_state['register_sheet'][st.session_state['register_sheet']['Exchange'] == exchange]

    coin_filtered = st.session_state['register_sheet'][(st.session_state['register_sheet']['Coin'] == coin)]

    line_filtered_df = exchange_filtered[(exchange_filtered['Coin'] == coin) & ((exchange_filtered['Status'] == "Buy") | (exchange_filtered['Status'] == "Rebuy"))]

    with tab1:
        # @GUARD-CLAUSE
        if len(line_filtered_df) == 0: 
            st.markdown(f"<h1 style='text-align: center;' >🔴 Não existe transações da moeda {coin} na corretora {exchange} 🔴</h1>", unsafe_allow_html=True)
            
        else:

            mean_price = line_filtered_df['Valor Investido (R$)'].sum() / line_filtered_df['Qte'].sum()

            mean_price_col = [mean_price] * line_filtered_df.shape[0]

            line_filtered_df.insert(0, "Mean Price", mean_price_col)

            card_col_1, card_col_2, card_col_3 = st.columns(3, gap="small")

            with card_col_1:
                with st.container(border=True):
                    title = st.markdown("### %.10f $" % (line_filtered_df['Mean Price'].iloc[0] / st.session_state['dolar_price']))
                    text = st.text("Preço Médio em Dólar")

            with card_col_2:
                with st.container(border=True):
                    title = st.markdown("### %.10f R$" % (line_filtered_df['Mean Price'].iloc[0]))
                    text = st.text("Preço Médio em Real")

            with card_col_3:
                with st.container(border=True):
                    title = st.markdown(f"### {st.session_state['dolar_price']} R$")
                    text = st.text("Preço Dolar em Real")


            c1, c2 = st.columns(2, gap="small")

            with c1:

                # line_chat_tab1, line_chat_tab2 = st.tabs(['Preço Médio de Compra', 'Preço Médio de Venda']) 

                # with line_chat_tab1:
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
                    fig.update_layout(autosize=True)

                    with st.container(border=True):
                        st.plotly_chart(fig)

                # with line_chat_tab2:

                #     try:
                #         line_sell_filtered = coin_filtered[coin_filtered['Status'] == "Sell"]
                #         st.dataframe(line_sell_filtered)
                #         # mean_price_sell = line_sell_filtered['Valor Investido (R$)'].sum() / line_sell_filtered['Qte'].sum()

                #         # line_filtered_df['Mean Price'] = [mean_price for x in range(line_sell_filtered.shape[0])]

                #         # line_selling = go.Scatter(x=line_sell_filtered['Data'], y=line_sell_filtered['Preço (R$)'], name='Preços de Venda', mode='lines')
                #         # line_sell_mean = go.Scatter(x=line_sell_filtered['Data'], y=line_sell_filtered['Mean Price'], name='Preço Médio', mode='lines')

                #         # layout = go.Layout(
                #         #     title='Histórico de Vendas e Preço Médio de Venda',
                #         #     xaxis=dict(title='Data'),
                #         #     yaxis=dict(title='Price (R$)'),
                #         #     hovermode='closest',
                #         #     margin=dict(l=20, r=20, b=20, t=40),
                #         #     showlegend=True,
                #         #     dragmode='pan',
                #         #     uirevision='none',
                #         # )

                #         # fig = go.Figure(data=[line_selling, line_sell_mean], layout=layout)
                #         # fig.update_layout(autosize=True)

                #         # with st.container(border=True):
                #         #     st.plotly_chart(fig)
                        
                #     except:
                #         st.markdown("## Não existe vendas nessa moeda.")


            bar_filtered_df = coin_filtered.groupby(by="Status")['Valor Investido (R$)'].sum().reset_index()

            with c2:
                bar_plots = []
                bar_purchase = go.Bar(x=['Comprado'], y=bar_filtered_df[['Valor Investido (R$)']].iloc[0,:], name='Comprado', marker=dict(color='green'))
                bar_plots.append(bar_purchase)
            
                try:
                    bar_sellof = go.Bar(x=['Vendido'], y=bar_filtered_df[['Valor Investido (R$)']].iloc[1,:], name='Vendido', marker=dict(color='red'))

                    bar_plots.append(bar_sellof)
                except:
                    pass
                
                try:
                    
                    total_amount = get_amount_coins(coin_filtered)

                    total_amount = total_amount * coin_filtered['Preço Atual (R$)'].values[0]

                    bar_non_realized = go.Bar(x=['Em Carteira'], y=[total_amount], name="Em Carteira", marker=dict(color='blue'))

                    bar_plots.append(bar_non_realized)
                except:
                    pass

                layout = go.Layout(
                        title='Valor (R$) Total Comprado e Vendido',
                        xaxis=dict(title='Operação'),
                        yaxis=dict(title='Quantidade (R$)'),
                        barmode='group', 
                        margin=dict(l=20, r=20, b=20, t=40),
                        legend=dict(orientation='h'), 
                    )
                fig = go.Figure(data=bar_plots, layout=layout)

                fig.update_layout(autosize=True)

                with st.container(border=True):
                    st.plotly_chart(fig)


            st.divider()

            st.markdown("## Análise On-Chain")

            total_amount = get_amount_coins(coin_filtered)

            c1, c2, c3 = st.columns(3, gap='medium')

            with c1:
                with st.container(border=True):
                    st.markdown(f"### {total_amount}")
                    st.text("Quantidade de moedas em carteira")

            with c2:
                with st.container(border=True):
                    st.markdown(f"###  {mean_price:.02f} R$")
                    st.text(f"Preço Pago por Moeda: ")
                                
            with c3:
                with st.container(border=True):
                    st.markdown(f"### {coin_filtered['Preço Atual (R$)'].values[0]:.02f} R$")
                    st.text(f"Preço Atual da Moeda:")



    with tab2:

        st.markdown("## Análise de Carteira")

        coin_current_price = st.session_state['register_sheet'][['Coin', 'Preço Atual (R$)']].drop_duplicates('Coin', keep='first')
        coin_current_price = {coin:price for coin, price in zip(coin_current_price['Coin'], coin_current_price['Preço Atual (R$)'])}

        buy_df = st.session_state['register_sheet'][st.session_state['register_sheet']['Status'] == 'Buy']
        buy_df = buy_df.groupby('Coin')['Qte'].sum().reset_index()

        sell_df = st.session_state['register_sheet'][st.session_state['register_sheet']['Status'] == 'Sell']
        sell_df = sell_df.groupby('Coin')['Qte'].sum().reset_index()

        coin_current_amout = {}

        for coin in coin_current_price.keys():
            qte = 0.0
            if coin in buy_df['Coin'].values:
                qte_buy = buy_df.loc[buy_df['Coin'] == coin]['Qte'].values[0]
                qte += qte_buy
            
            if coin in sell_df['Coin'].values:
                qte_sell = sell_df.loc[sell_df['Coin'] == coin]['Qte'].values[0]
                qte -= qte_sell

            coin_current_amout[coin] = coin_current_price[coin] * qte

        # # box = INITIAL_WALLET_CASH + rebuy_historical_df[rebuy_historical_df['Status'] == 'Sell']['Valor Investido (R$)'].sum() - rebuy_historical_df[rebuy_historical_df['Status'] == 'Buy']['Valor Investido (R$)'].sum()

        # box = INITIAL_INCOME + st.session_state['register_sheet'].loc[st.session_state['register_sheet']['Status'] == 'Sell']['Valor Investido (R$)'] - st.session_state['register_sheet'].loc[st.session_state['register_sheet']['Status'] == 'Buy']['Valor Investido (R$)']

        # coin_current_amout['Caixa'] = box

        fig = go.Figure(data=[go.Pie(labels=list(coin_current_amout.keys()), values=list(coin_current_amout.values()))])

        # Customize the layout (optional)
        fig.update_layout(
            title='Porcentagem por Moeda',
            xaxis_title='Moeda',
            yaxis_title='Porcentagem'
        )

        total_capital = sum(coin_current_amout.values())

        with st.container(border=True):
            wallet_value_1, wallet_value_2, wallet_value_3 = st.columns(3, gap='medium')

            revenue_total = st.session_state['revenue_sheet']['Amount'].sum()

            with wallet_value_1:
                with st.container(border=True):
                    st.text("Valor Total de Aportes")
                    st.markdown(f"### {revenue_total} R$")

            with wallet_value_2:
                with st.container(border=True):
                    st.text("Valor Atual da Carteira")
                    st.markdown(f"### {total_capital:.2f} R$")

            with wallet_value_3:
                with st.container(border=True):
                    st.text("Valorização Média da Carteira")
                    valuation = total_capital / revenue_total
                    if valuation > 1.00:
                        st.markdown(f"### % {valuation:.2f} 🟢")
                    else:
                        st.markdown(f"### {valuation:.2f} 🔴")




        c1_wallet, c2_wallet = st.columns(2, gap='medium')

        with c1_wallet:
            with st.container(border=True):
                st.plotly_chart(fig)


        with c2_wallet:
            with st.container(border=True):
                fiat_amount = st.session_state['register_sheet'][st.session_state['register_sheet']['Coin'].isin([
                    'USDT', 'USDC', 'BRL'
                ])]

                fiat_amount = round((fiat_amount['Qte'] * fiat_amount['Preço Atual (R$)']).sum(), 2)

                wallet_amount = st.session_state['register_sheet'][~st.session_state['register_sheet']['Coin'].isin([
                    'USDT', 'USDC', 'BRL'
                ])]

                wallet_amount = round((wallet_amount['Qte'] * wallet_amount['Preço Atual (R$)']).sum(), 2)

                box_bar = go.Figure(data=[go.Bar(x=["Caixa", "Carteira"], y=[fiat_amount, wallet_amount])])

                box_bar.add_trace(go.Scatter(
                    x=["Caixa", "Carteira"], 
                    y=[fiat_amount, wallet_amount],
                    text=[fiat_amount, wallet_amount],
                    mode='text',
                    textposition='top center',
                    textfont=dict(
                        size=18,
                    ),
                    showlegend=False
                ))

                box_bar.update_layout(
                    title='Caixa x Carteira',
                    xaxis_title='Investido em',
                    yaxis_title='Valor Total (R$)'
                )

                st.plotly_chart(box_bar)

        with st.container(border=True):
            revenue_fig = go.Figure()

            revenue_fig.add_trace(go.Bar(x=st.session_state['revenue_sheet'].tail(12)['Data'], y=st.session_state['revenue_sheet'].tail(12)['Amount']))
            revenue_fig.add_trace(go.Scatter(x=st.session_state['revenue_sheet'].tail(12)['Data'], y=st.session_state['revenue_sheet'].tail(12)['Amount']))

            revenue_fig.update_layout(
                    title='Aportes ao longo do tempo',
                    xaxis_title='Data',
                    yaxis_title='Valor Total (R$)'
                )

            st.plotly_chart(revenue_fig)



        