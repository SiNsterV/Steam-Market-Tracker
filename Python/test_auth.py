import streamlit as st
import hashlib
import sqlite3
from SteamtrackerV3 import program
import database as data



st.set_page_config(layout="wide")

def main():

    if 'user' not in st.session_state:
        # User is not logged in
        menu = ["Login", "SignUp"]
        choice = st.sidebar.selectbox("Menu", menu)
    else:
        # User is logged in
        menu = ["Home", "Update Steam API Key", "Logout"]
        choice = st.sidebar.selectbox("Menu", menu)
        st.sidebar.write(f"Logged in as {st.session_state['user']}")

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login" and 'user' not in st.session_state:
        st.sidebar.subheader("Login Section")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        steam_api_key = "0"
        if st.sidebar.button("Login"):
            data.create_usertable()
            hashed_pswd = data.make_hashes(password)
            result = data.login_user(username, hashed_pswd)
            if result:
                st.rerun()
                st.session_state['user'] = result['username']
                st.success(f"Logged In as {username}")
                choice = "Update Steam API Key"

    elif choice == "SignUp" and 'user' not in st.session_state:
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        steam_api_key = "0"
        if st.button("Signup"):
            data.create_usertable()
            data.add_userdata(new_user, data.make_hashes(new_password), steam_api_key)
            st.success("You have successfully created an account")
            st.info("Go to Login Menu to login")

    elif choice == "Update Steam API Key":
        st.subheader("Update your Steam API Key")
        new_api_key = st.text_input("Steam API Key", value="")
        if st.button("Update API Key"):
            data.update_steam_api_key(st.session_state['user'], new_api_key)
            st.success("Steam API Key Updated Successfully")

    elif choice == "Logout":
        st.session_state.pop('user', None)  # Remove user from session
        st.info("You have been logged out.")

    if 'user' in st.session_state:
        if data.is_steam_api_key_zero(st.session_state['user']):
            st.warning("Your Steam API key is not set. Please update your Steam API Key.")
        else:
            st.sidebar.write("Your Steam API key is set.")
            program()

if __name__ == '__main__':
    main()
