import streamlit as st

from utils.constants import *

st.set_page_config(layout="wide")

from services.Cookies import Cookies
Cookies().database_cookie()
Cookies().coinmarketcap_cookie()
Cookies().fiatprices_cookie()

st.sidebar.image("assets/BUSINESS_LOGOTYPE.png")

from navigation.pages import sideBar

sideBar()

from style.Style import Style
Style()