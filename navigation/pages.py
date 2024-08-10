import streamlit as st
from streamlit_option_menu import option_menu

<<<<<<< HEAD
from page_functions.data import register_page
from page_functions.home import home_page
from page_functions.registers import data_page
=======
from page_functions.home import home_page
from page_functions.register import register_page
from page_functions.data import data_page
>>>>>>> fc0356778cc07962ff885e20a0c1d7ec133372f1


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