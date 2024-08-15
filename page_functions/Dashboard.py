import streamlit as st
from services.Cookies import Cookies

from services.Cookies import Cookies


def Dashboard():
    cookies = Cookies()
    cookies.database_cookie(connection_key=st.session_state['sheet_account'])
    cookies.coinmarketcap_cookie()
    cookies.fiatprices_cookie()

    st.sidebar.image("assets/BUSINESS_LOGOTYPE.png")

    from navigation.pages import sideBar

    sideBar()

    from style.Style import Style
    Style()