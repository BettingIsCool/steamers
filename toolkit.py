import base64
import streamlit as st
import db_steamers_remote


def redirect_button():
    url = 'https://t.me/psp_ultra_bot'

    #st.sidebar.markdown(f'''<a href={url}><button style="background-color:Red;">Click here to connect! Link will expire in 1 minute.</button></a>''', unsafe_allow_html=True)
    st.sidebar.markdown(f'<script>window.open("{url}", "_blank");</script>', unsafe_allow_html=True)
    db_steamers_remote.set_telegram_button_pressed(username=st.session_state.email)
