from library import *
from services.Database import Database

st.set_page_config(layout="wide")

st.title("📁 Operações Registradas")
st.markdown("Você pode ver todos as operações registradas abaixo!")


database = Database(worksheets=[
    ("DATA", 10),
    ("COINS", 2),
    ("EXCHANGES", 1)
])

data_register = database.worksheets["DATA"].dropna(how="all")
data_coins = database.worksheets["COINS"].dropna(how="all")
data_exchanges = database.worksheets["EXCHANGES"].dropna(how="all")

c1, c2 = st.columns(2, gap="small")
 
with st.container(border=True):
        st.markdown("<h1 style='text-align: center; '>Operações Registradas</h1>", unsafe_allow_html=True)

        edit_data_register = st.data_editor(data_register, hide_index=True)
        
        submit_btn_register = st.button(label="Atualizar dados de operações...")
        
        if submit_btn_register:
            try:
                database.conn.update(worksheet="DATA", data=edit_data_register)
                st.success("Tabela atualizada com sucesso!")

            except:
                st.warning("Tabela não atualizada!")
                st.stop()

with c1:
    with st.container(border=True):
        st.markdown("<h1 style='text-align: center; '>Moedas Registradas</h1>", unsafe_allow_html=True)


        edit_data_coins = st.data_editor(data_coins, hide_index=True)

        submit_btn_coins = st.button(label="Atualizar dados de moedas...")
        
        if submit_btn_coins:
            try:
                database.conn.update(worksheet="COINS", data=edit_data_coins)
                st.success("Tabela atualizada com sucesso!")

            except:
                st.warning("Tabela não atualizada!")
                st.stop()

with c2:
    with st.container(border=True):
        st.markdown("<h1 style='text-align: center; '>Corretoras Registradas</h1>", unsafe_allow_html=True)

        edit_data_exchanges = st.data_editor(data_exchanges, hide_index=True)

        submit_btn_exchanges = st.button(label="Atualizar dados de corretoras...")
        
        if submit_btn_exchanges:
            try:
                database.conn.update(worksheet="EXCHANGES", data=edit_data_exchanges)
                st.success("Tabela atualizada com sucesso!")

            except:
                st.warning("Tabela não atualizada!")
                st.stop()