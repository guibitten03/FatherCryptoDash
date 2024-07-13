import streamlit as st

class Style:
    def __init__(self, stylesheet_path: str = "style/style.css") -> None:
        self.stylesheet_path = stylesheet_path

        self._load()


    def _load(self):
        with open(self.stylesheet_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
