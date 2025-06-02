import streamlit as st

# set_page_config() can only be called once per app page, and must be called as the first Streamlit command in your script.
st.set_page_config(page_title="ChasingSteamers Personal by BettingIsCool", page_icon="♨️", layout="wide", initial_sidebar_state="expanded")

import time
import pytz
from config import SPORTS, MARKETS, BOOKS, TEXT_LANDING_PAGE


import datetime
import pandas as pd
import db_steamers_remote as db
from streamlit_autorefresh import st_autorefresh

placeholder1 = st.empty()
placeholder2 = st.empty()

if 'display_landing_page_text' not in st.session_state:

    # Display landing page (pre login)
    placeholder1.markdown(TEXT_LANDING_PAGE)
    placeholder2.image('chart.png', use_container_width='auto')
    st.session_state.display_landing_page_text = True

# Add google authentication (only users with a valid stripe subscription can log in)
# Username must match the registered email-address at stripe
# IMPORTANT: st_paywall is a forked library. This fork supports additional verification, i.e. if the user has a valid subscription for the product
# The original st_paywall just looks into the stripe account for ANY valid subscription for that particular user, but doesn't care if this subscription is actually valid for a specific app.
# See also https://github.com/tylerjrichards/st-paywall/issues/75
# Importing this fork can be done with 'git+https://github.com/bettingiscool/st-paywall_fork.git@main' in the requirements.txt file

from st_paywall import add_auth
add_auth(required=True)

# Maybe a short delay helps to avoid "Bad message format - Tried to use SessionInfo before it was initialized"
time.sleep(0.25)
username = st.session_state.email

placeholder1.empty()
placeholder2.empty()

st.cache_data.clear()

# Check if username is in database, otherwise append the user
if 'users_fetched' not in st.session_state:
    if username not in set(db.get_users()):
        db.append_user(data={'username': username})
    st.session_state.users_fetched = True

# Load settings into session state
if 'sports' not in st.session_state:
    st.session_state.sports = db.get_user_setting(username=username, param='sports').split(',')
if 'markets' not in st.session_state:
    st.session_state.markets = db.get_user_setting(username=username, param='markets').split(',')
if 'minval' not in st.session_state:
    st.session_state.minval = db.get_user_setting(username=username, param='minval')
if 'minodds' not in st.session_state:
    st.session_state.minodds = db.get_user_setting(username=username, param='minodds')
if 'maxodds' not in st.session_state:
    st.session_state.maxodds = db.get_user_setting(username=username, param='maxodds')
if 'lookahead' not in st.session_state:
    st.session_state.lookahead = db.get_user_setting(username=username, param='lookahead')
if 'book1' not in st.session_state:
    st.session_state.book1 = db.get_user_setting(username=username, param='book1')
if 'book2' not in st.session_state:
    st.session_state.book2 = db.get_user_setting(username=username, param='book2')
if 'book3' not in st.session_state:
    st.session_state.book3 = db.get_user_setting(username=username, param='book3')
if 'telegram_id' not in st.session_state:
    st.session_state.telegram_id = db.get_user_setting(username=username, param='telegram_id')

# Connect Telegram
if st.session_state.telegram_id is None:
    if st.sidebar.button("Connect Telegram", help="Hit this button to receive telegram alerts.", type="secondary"):
        url = "https://t.me/psp_ultra_bot/"
        st.sidebar.markdown(f'<a href="{url}" target="_blank">Click here to connect! Link will expire in 1 minute.</a>', unsafe_allow_html=True)
        db.set_telegram_button_pressed(username=st.session_state.email)
        st.session_state.telegram_id = db.get_user_setting(username=username, param='telegram_id')

# Welcome message in the sidebar
st.sidebar.subheader(f"Welcome {username}")

st.header(f"Settings")
selected_sports = st.multiselect(label="Sports", options=SPORTS, default=st.session_state.sports, on_change=db.change_sports, args=(username,), key='sports_key', help="Which sports should be included in your alerts?")
selected_markets = st.multiselect(label="Markets", options=MARKETS, default=st.session_state.markets, on_change=db.change_markets, args=(username,), key='markets_key', help="Which markets should be included in your alerts?")
selected_minval = st.slider(label='Minimum Value Threshold', min_value=0.025, max_value=1.00, value=st.session_state.minval, step=0.005, format="%0.3f", key='minval_key', on_change=db.change_minval, args=(username,), help='Enter percentage as decimal number. 5% = 0.05')
selected_minodds = st.slider(label='Minimum Odds', min_value=1.00, max_value=10.00, value=st.session_state.minodds, step=0.05, format="%0.2f", key='minodds_key', on_change=db.change_minodds, args=(username,))
selected_maxodds = st.slider(label='Maximum Odds', min_value=selected_minodds, max_value=100.00, value=st.session_state.maxodds, step=0.05, format="%0.2f", key='maxodds_key', on_change=db.change_maxodds, args=(username,))
selected_lookahead = st.slider(label='Lookahead (in hours)', min_value=1, max_value=500, value=st.session_state.lookahead, step=1, key='lookahead_key', on_change=db.change_lookahead, args=(username,), help='Show only events that start within the next x hours.')

st.subheader(f"Bookmaker Deeplinks")
col_book1, col_book2, col_book3 = st.columns([1, 1, 1])

with col_book1:
    selected_book1 = st.selectbox(label='Bookie 1', options=sorted(list(BOOKS)), index=sorted(list(BOOKS)).index(st.session_state.book1), key='book1_key', on_change=db.change_book1, args=(username,), help='Deeplinks for your preferred bookmaker can be included in every alert. One click will take you to the respective market meaning a highly efficient and hassle-free bet placement.')
with col_book2:
    selected_book2 = st.selectbox(label='Bookie 2', options=sorted(list(BOOKS)), index=sorted(list(BOOKS)).index(st.session_state.book2), key='book2_key', on_change=db.change_book2, args=(username,), help='Deeplinks for your preferred bookmaker can be included in every alert. One click will take you to the respective market meaning a highly efficient and hassle-free bet placement.')
with col_book3:
    selected_book3 = st.selectbox(label='Bookie 3', options=sorted(list(BOOKS)), index=sorted(list(BOOKS)).index(st.session_state.book3), key='book3_key', on_change=db.change_book3, args=(username,), help='Deeplinks for your preferred bookmaker can be included in every alert. One click will take you to the respective market meaning a highly efficient and hassle-free bet placement.')
