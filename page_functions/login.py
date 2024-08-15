import streamlit as st
import streamlit_authenticator as stauth

class LoginPage:
    def __init__(self):
        self.credentials = st.secrets.to_dict()['credentials']
        self.cookie = st.secrets.to_dict()['cookie']
        self.authenticator = stauth.Authenticate(
            self.credentials,
            self.cookie['name'],
            self.cookie['key'],
        )

    def authenticate(self):
        name, authentication_status, username = self.authenticator.login('main', fields={'Form name': 'Login'})
        return name, authentication_status

    def logout(self):
        self.authenticator.logout('Logout', 'sidebar')

    def page(self, page_to_show):
        name, authentication_status = self.authenticate()

        if authentication_status:
            self.logout()
            page_to_show()
        elif authentication_status == False:
            st.error('Username/password is incorrect')
        elif authentication_status == None:
            st.warning('Please enter your username and password')