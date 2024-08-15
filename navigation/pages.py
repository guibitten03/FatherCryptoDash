import streamlit as st
from streamlit_option_menu import option_menu

from page_functions.data import data_page
from page_functions.home import home_page
from page_functions.register import register_page


def sideBar():
    with st.sidebar:
        selected = option_menu(menu_title="", 
                               options=["Início",
                                        "Registrar",
                                        "Dados"],
                               icons=["camera"],
                               menu_icon="cast",
                               default_index=0)
        
    if selected == "Início":
        home_page()
    if selected == "Registrar":
        register_page()
    if selected == "Dados":
        data_page()