from library import *

class Style:
    def __init__(self, path=""):
        
        with open(path) as f:
            self.css = f.read()

    def _connect(self):
        st.markdown(f"<style>{self.css}</style>", unsafe_allow_html=True)