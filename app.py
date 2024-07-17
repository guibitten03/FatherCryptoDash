import streamlit as st

from utils.constants import *

st.set_page_config(layout="wide")

from services.Cookies import Cookies
cookies = Cookies()
cookies.database_cookie()
cookies.coinmarketcap_cookie()
cookies.fiatprices_cookie()

st.sidebar.image("assets/BUSINESS_LOGOTYPE.png")

from navigation.pages import sideBar

sideBar()

from style.Style import Style
Style()