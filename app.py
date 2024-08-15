import streamlit as st
from page_functions.Dashboard import Dashboard
from page_functions.login import LoginPage

st.set_page_config(layout="wide")

st.session_state['sheet_account'] = st.sidebar.selectbox("Selecione a conta...", options=["Guilherme", "Jader"])

LoginPage().page(page_to_show=Dashboard)