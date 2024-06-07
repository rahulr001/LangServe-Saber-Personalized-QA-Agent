import streamlit as st


def register():
    st.title("Register")

    with st.form("register_form"):
        st.subheader("Create a new account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        email = st.text_input("Email")
        full_name = st.text_input("Full Name")
        agree = st.checkbox("I agree to the terms and conditions")
        submitted = st.form_submit_button("Register")

    if submitted:
        if not agree:
            st.error("You must agree to the terms and conditions to register.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        elif not username or not password or not email or not full_name:
            st.error("Please fill out all required fields.")
        else:
            st.session_state.is_registered = True
            st.switch_page("main.py")


register()
