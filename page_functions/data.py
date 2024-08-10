import streamlit as st

def data_page():
    st.title("📁 Operações Registradas")
    st.markdown("Você pode ver todos as operações registradas abaixo!")

    f_c1, f_c2 = st.columns([3, 1], gap="small")
    
    with f_c1:
        with st.container(border=True):
            st.markdown("<h1 style='text-align: center; '>Operações Registradas</h1>", unsafe_allow_html=True)

            st.divider()

            edit_data_register = st.data_editor(st.session_state['register_sheet'], hide_index=True)
            
            submit_btn_register = st.button(label="Atualizar dados de operações...")
            
            if submit_btn_register:
                try:
                    st.session_state['database'].conn.update(worksheet="DATA", data=edit_data_register)
                    st.success("Tabela atualizada com sucesso!")

                except:
                    st.warning("Tabela não atualizada!")
                    st.stop()

    with f_c2:
        with st.container(border=True):
            st.markdown("<h1 style='text-align: center; '>Aportes Registrados</h1>", unsafe_allow_html=True)

            st.divider()

            edit_data_revenue = st.data_editor(st.session_state['revenue_sheet'], hide_index=True)
            
            submit_btn_revenue = st.button(label="Atualizar dados de aportes...")
            
            if submit_btn_revenue:
                try:
                    st.session_state['database'].conn.update(worksheet="REVENUE", data=edit_data_revenue)
                    st.success("Tabela atualizada com sucesso!")

                except:
                    st.warning("Tabela não atualizada!")
                    st.stop()

    c1, c2 = st.columns(2, gap="small")

    with c1:
        with st.container(border=True):
            st.markdown("<h1 style='text-align: center; '>Moedas Registradas</h1>", unsafe_allow_html=True)

            st.divider()

            edit_data_coins = st.data_editor(st.session_state['coin_sheet'], hide_index=True)

            submit_btn_coins = st.button(label="Atualizar dados de moedas...")
            
            if submit_btn_coins:
                try:
                    st.session_state['database'].conn.update(worksheet="COINS", data=edit_data_coins)
                    st.success("Tabela atualizada com sucesso!")

                except:
                    st.warning("Tabela não atualizada!")
                    st.stop()

    with c2:
        with st.container(border=True):
            st.markdown("<h1 style='text-align: center; '>Corretoras Registradas</h1>", unsafe_allow_html=True)

            st.divider()

            edit_data_exchanges = st.data_editor(st.session_state['exchange_sheet'], hide_index=True)

            submit_btn_exchanges = st.button(label="Atualizar dados de corretoras...")
            
            if submit_btn_exchanges:
                try:
                    st.session_state['database'].conn.update(worksheet="EXCHANGES", data=edit_data_exchanges)
                    st.success("Tabela atualizada com sucesso!")

                except:
                    st.warning("Tabela não atualizada!")
                    st.stop()