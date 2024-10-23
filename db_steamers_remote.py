# The module 'db_steamers_remote.py' uses sqlalchemy as the database connector which is the preferred way for streamlit
# The module 'db_steamers_remote2.py' uses mysql-connector-python

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
    return conn.query(f"SELECT starts, sport_name, league_name, runner_home, runner_away, selection, market, line, prev_odds, curr_odds, droppct, oddstobeat, book_odds, book_val, book_name, book_url, timestamp, id, bet_str FROM {TABLE_LOG} WHERE book_slug IN {bookmakers} ORDER BY timestamp DESC").to_dict('records')


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
    query = f"INSERT INTO {TABLE_USERS} (username, odds_display, timezone, default_minval, default_book1, default_book2, default_book3, default_book4, default_book5) VALUES(:username, :odds_display, :timezone, :default_minval, :default_book1, :default_book2, :default_book3, :default_book4, :default_book5)"

    with conn.session as session:
        session.execute(text(query), params=dict(username=data['username'], odds_display='Decimal', timezone='Europe/London', default_minval=0.05, default_book1='', default_book2='', default_book3='', default_book4='', default_book5=''))
        session.commit()