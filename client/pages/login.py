import streamlit as st

st.set_option("client.showSidebarNavigation", False)


def login():
    if st.session_state.get('is_registered'):
        st.success("Registration successfully.")

    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        st.success("Logged in successfully.")
