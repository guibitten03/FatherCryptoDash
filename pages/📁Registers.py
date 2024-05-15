from library import *
from services.Database import Database

st.set_page_config(layout="wide")

st.title("📁 Crypto Trades Registed")
st.markdown("You can see all your trades bellow!")

database = Database(worksheets=[
    ("DATA", 9),
    ("COINS", 2),
    ("EXCHANGES", 1)
])

# Teste
data_register = database.worksheets["DATA"].dropna(how="all")
data_coins = database.worksheets["COINS"].dropna(how="all")
data_exchanges = database.worksheets["EXCHANGES"].dropna(how="all")

c1, c2, c3 = st.columns(3, gap="small")

with c1: 
    with st.container(border=True):
        # st.title("Registered Operatios")
        st.markdown("<h1 style='text-align: center; '>Registered Operatios</h1>", unsafe_allow_html=True)

        edit_data_register = st.data_editor(data_register, hide_index=True)
        
        submit_btn_register = st.button(label="Update Register Dataframe")
        
        if submit_btn_register:
            try:
                database.conn.update(worksheet="DATA", data=edit_data_register)
                st.success("Dataset Updated with Success!")

            except:
                st.warning("Dataset not Updated!")
                st.stop()

with c2:
    with st.container(border=True):
        # st.title("Registered Coins")
        st.markdown("<h1 style='text-align: center; '>Registered Coins</h1>", unsafe_allow_html=True)


        edit_data_coins = st.data_editor(data_coins, hide_index=True)

        submit_btn_coins = st.button(label="Update Coins Dataframe")
        
        if submit_btn_coins:
            try:
                database.conn.update(worksheet="COINS", data=edit_data_coins)
                st.success("Dataset Updated with Success!")

            except:
                st.warning("Dataset not Updated!")
                st.stop()

with c3:
    with st.container(border=True):
        # st.title("Registered Coins")
        st.markdown("<h1 style='text-align: center; '>Registered Exchanges</h1>", unsafe_allow_html=True)

        edit_data_exchanges = st.data_editor(data_exchanges, hide_index=True)

        submit_btn_exchanges = st.button(label="Update exchanges Dataframe")
        
        if submit_btn_exchanges:
            try:
                database.conn.update(worksheet="EXCHANGES", data=edit_data_exchanges)
                st.success("Dataset Updated with Success!")

            except:
                st.warning("Dataset not Updated!")
                st.stop()