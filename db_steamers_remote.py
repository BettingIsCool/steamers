# The module 'db_steamers_remote.py' uses sqlalchemy as the database connector which is the preferred way for streamlit
# The module 'db_steamers_remote2.py' uses mysql-connector-python

import time
from datetime import datetime

import streamlit as st
from sqlalchemy import text
from config import TABLE_USERS

conn = st.connection('steamers', type='sql')


def get_users():
    """
    :return: List of usernames retrieved from the database TABLE_USERS.
    :rtype: list
    """
    return conn.query(f"SELECT username FROM {TABLE_USERS}")['username'].tolist()


def append_user(data: dict):
    """
    :param data: Dictionary containing user data with the key 'username'.
    :return: None
    """
    query = f"INSERT INTO {TABLE_USERS} (username, minval, minodds, maxodds, lookahead, active_books) VALUES(:username, :minval, :minodds, :maxodds, :lookahead, :active_books)"

    with conn.session as session:
        session.execute(text(query), params=dict(username=data['username'], minval=0.10, minodds=1.01, maxodds=100.00, lookahead=8, active_books=0))
        session.commit()


def get_user_setting(username: str, param: str):

    return conn.query(f"SELECT {param} FROM {TABLE_USERS} WHERE username = '{username}'")[param].tolist()[0]


def change_user_setting(username: str, param: str, value: (float, int)):

    query = f"UPDATE {TABLE_USERS} SET {param} = {value} WHERE username = '{username}'" if 'book' not in param else f"UPDATE {TABLE_USERS} SET {param} = '{value}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()




def get_user_dbid(username: str):

    return conn.query(f"SELECT id FROM {TABLE_USERS} WHERE username = '{username}'")['id'].tolist()


def get_telegram_user_id(username: str):

    return conn.query(f"SELECT telegram_id FROM {TABLE_USERS} WHERE username = '{username}'")['telegram_id'].tolist()






def set_telegram_button_pressed(username: str):

    query = f"UPDATE {TABLE_USERS} SET telegram_button_pressed = '{datetime.now()}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()










def change_user_odds_display(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_odds_display = st.session_state.default_odds_display_key

    query = f"UPDATE {TABLE_USERS} SET default_odds_display = '{st.session_state.default_odds_display}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Odds format changed successfully!')
    time.sleep(2)
    placeholder.empty()


def change_user_timezone(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_timezone = st.session_state.default_timezone_key

    query = f"UPDATE {TABLE_USERS} SET default_timezone = '{st.session_state.default_timezone}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Time zone format changed successfully!')
    time.sleep(2)
    placeholder.empty()
    

def change_user_minval(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_minval = st.session_state.default_minval_key

    query = f"UPDATE {TABLE_USERS} SET default_minval = '{st.session_state.default_minval}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Minimum value threshold changed successfully!')
    time.sleep(2)
    placeholder.empty()


def change_user_minodds(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_minodds = st.session_state.default_minodds_key

    query = f"UPDATE {TABLE_USERS} SET default_minodds = '{st.session_state.default_minodds}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Minimum odds changed successfully!')
    time.sleep(2)
    placeholder.empty()


def change_user_maxodds(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_maxodds = st.session_state.default_maxodds_key

    query = f"UPDATE {TABLE_USERS} SET default_maxodds = '{st.session_state.default_maxodds}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Maximum odds changed successfully!')
    time.sleep(2)
    placeholder.empty()
    

def change_user_book1(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_book1 = st.session_state.default_book1_key

    query = f"UPDATE {TABLE_USERS} SET default_book1 = '{st.session_state.default_book1}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Book1 changed successfully!')
    time.sleep(2)
    placeholder.empty()
    

def change_user_book2(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_book2 = st.session_state.default_book2_key

    query = f"UPDATE {TABLE_USERS} SET default_book2 = '{st.session_state.default_book2}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Book2 changed successfully!')
    time.sleep(2)
    placeholder.empty()
    

def change_user_book3(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_book3 = st.session_state.default_book3_key

    query = f"UPDATE {TABLE_USERS} SET default_book3 = '{st.session_state.default_book3}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Book3 changed successfully!')
    time.sleep(2)
    placeholder.empty()
    

def change_user_book4(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_book4 = st.session_state.default_book4_key

    query = f"UPDATE {TABLE_USERS} SET default_book4 = '{st.session_state.default_book4}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Book4 changed successfully!')
    time.sleep(2)
    placeholder.empty()
    

def change_user_book5(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_book5 = st.session_state.default_book5_key

    query = f"UPDATE {TABLE_USERS} SET default_book5 = '{st.session_state.default_book5}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Book5 changed successfully!')
    time.sleep(2)
    placeholder.empty()
    

def change_user_lookahead(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_lookahead = st.session_state.default_lookahead_key

    query = f"UPDATE {TABLE_USERS} SET default_lookahead = '{st.session_state.default_lookahead}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Lookahead changed successfully!')
    time.sleep(2)
    placeholder.empty()
