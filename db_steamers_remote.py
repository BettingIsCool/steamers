# The module 'db_steamers_remote.py' uses sqlalchemy as the database connector which is the preferred way for streamlit
# The module 'db_steamers_remote2.py' uses mysql-connector-python

import time
import streamlit as st
from sqlalchemy import text
from config import TABLE_LOG, TABLE_USERS

conn = st.connection('steamers', type='sql')


@st.cache_data()
def get_log(bookmakers: str):
    """
    :param username: The username of the individual placing the bets.
    :param sports: A string specifying which sports to include in the query.
    :param bookmakers: A string specifying which bookmakers to include in the query.
    :param tags: A string specifying which tags to include in the query.
    :param date_from: The start date for filtering bets.
    :param date_to: The end date for filtering bets.
    :return: A list of dictionaries containing bet details filtered by the given criteria.
    """
    return conn.query(f"SELECT starts, sport_name, league_name, runner_home, runner_away, selection, market, line, prev_odds, curr_odds, droppct, oddstobeat, book_odds, book_val, book_name, book_url, timestamp, id, bet_str, timestamp_utc, starts_utc, updated_ago, drop_str FROM {TABLE_LOG} WHERE book_slug IN {bookmakers} AND TIMESTAMPDIFF(SECOND, timestamp_utc, NOW()) < 3600 ORDER BY timestamp_utc DESC").to_dict('records')


def get_users():
    """
    :return: List of usernames retrieved from the database TABLE_USERS.
    :rtype: list
    """
    return conn.query(f"SELECT username FROM {TABLE_USERS}")['username'].tolist()


def get_user_dbid(username: str):

    return conn.query(f"SELECT id FROM {TABLE_USERS} WHERE username = '{username}'")['id'].tolist()


def append_user(data: dict):
    """
    :param data: Dictionary containing user data with the key 'username'.
    :return: None
    """
    query = f"INSERT INTO {TABLE_USERS} (username, odds_display, timezone, default_minval, default_minodds, default_maxodds, default_book1, default_book2, default_book3, default_book4, default_book5) VALUES(:username, :odds_display, :timezone, :default_minval, :default_minodds, :default_maxodds, :default_book1, :default_book2, :default_book3, :default_book4, :default_book5)"

    with conn.session as session:
        session.execute(text(query), params=dict(username=data['username'], odds_display='Decimal', timezone='Europe/London', default_minval=0.025, default_minodds=1, default_maxodds=1000, default_book1='', default_book2='', default_book3='', default_book4='', default_book5=''))
        session.commit()


def get_user_setting(username: str, param: str):

    return conn.query(f"SELECT {param} FROM {TABLE_USERS} WHERE username = '{username}'")[param].tolist()[0]


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

    placeholder.success('Odds format changed successfully!')
    time.sleep(2)
    placeholder.empty()


def change_user_maxodds(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_maxodds = st.session_state.default_maxodds_key

    query = f"UPDATE {TABLE_USERS} SET default_maxodds = '{st.session_state.default_maxodds}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Odds format changed successfully!')
    time.sleep(2)
    placeholder.empty()
    

def change_user_book1(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_book1 = st.session_state.default_book1_key

    query = f"UPDATE {TABLE_USERS} SET default_book1 = '{st.session_state.default_book1}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Odds format changed successfully!')
    time.sleep(2)
    placeholder.empty()
    

def change_user_book2(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_book2 = st.session_state.default_book2_key

    query = f"UPDATE {TABLE_USERS} SET default_book2 = '{st.session_state.default_book2}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Odds format changed successfully!')
    time.sleep(2)
    placeholder.empty()
    

def change_user_book3(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_book3 = st.session_state.default_book3_key

    query = f"UPDATE {TABLE_USERS} SET default_book3 = '{st.session_state.default_book3}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Odds format changed successfully!')
    time.sleep(2)
    placeholder.empty()
    

def change_user_book4(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_book4 = st.session_state.default_book4_key

    query = f"UPDATE {TABLE_USERS} SET default_book4 = '{st.session_state.default_book4}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Odds format changed successfully!')
    time.sleep(2)
    placeholder.empty()
    

def change_user_book5(username: str, placeholder: st.delta_generator.DeltaGenerator):

    st.session_state.default_book5 = st.session_state.default_book5_key

    query = f"UPDATE {TABLE_USERS} SET default_book5 = '{st.session_state.default_book5}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()

    placeholder.success('Odds format changed successfully!')
    time.sleep(2)
    placeholder.empty()
