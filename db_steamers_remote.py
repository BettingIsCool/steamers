# The module 'db_steamers_remote.py' uses sqlalchemy as the database connector which is the preferred way for streamlit
# The module 'db_steamers_remote2.py' uses mysql-connector-python

import time
from datetime import datetime

import streamlit as st
from sqlalchemy import text
from config import TABLE_USERS

conn = st.connection('steamers', type='sql')


@st.cache_data()
def get_users():
    """
    Fetches and returns a list of usernames from the specified users table.

    This function retrieves all usernames from the database by executing an SQL
    query on a predefined users table. The returned data is cached using streamlit's
    `st.cache_data()` decorator to optimize performance and avoid redundant database
    queries.

    :return: A list containing usernames fetched from the database.
    :rtype: list
    """
    return conn.query(f"SELECT username FROM {TABLE_USERS}")['username'].tolist()


@st.cache_data()
def append_user(data: dict):
    """
    Append a new user to the database by inserting values into the users table. The data is provided as
    a dictionary containing user-specific details. The values for `sports`, `markets`, and other fields
    are predefined defaults.

    This function is designed to interact with a database session, and commits the new user data
    to the database after successful insertion.

    :param data: A dictionary containing user information. Includes at least a `username` key
        with corresponding data mapped for `username` in the `TABLE_USERS`.
    :type data: dict
    :return: None
    """
    query = f"INSERT INTO {TABLE_USERS} (username, sports, markets, mindrop, minodds, maxodds, lookahead, book1, book2, book3, clear_cache, need_book) VALUES(:username, :sports, :markets, :mindrop, :minodds, :maxodds, :lookahead, :book1, :book2, :book3, :clear_cache, :need_book)"

    with conn.session as session:
        session.execute(text(query), params=dict(username=data['username'], sports='Soccer,Tennis,Basketball,Hockey,Volleyball,Handball,American Football,Mixed Martial Arts,Baseball,E Sports,Cricket', markets='moneyline,spread,totals', mindrop=0.10, minodds=1.01, maxodds=100.00, lookahead=8, book1='No Book', book2='No Book', book3='No Book', clear_cache=5, need_book='no'))
        session.commit()


@st.cache_data()
def get_user_setting(username: str, param: str):
    """
    Retrieve a specific setting for a given username from the user table.

    This function fetches the value of a specific parameter for a given username
    from the database. The result is then cached for optimized performance in repeated
    calls.

    :param username: The username whose setting is to be retrieved.
    :type username: str
    :param param: The specific parameter to fetch from the user table.
    :type param: str
    :return: The value of the requested parameter for the specified username.
    :rtype: str
    """
    return conn.query(f"SELECT {param} FROM {TABLE_USERS} WHERE username = '{username}'")[param].tolist()[0]


@st.cache_data()
def change_sports(username: str):
    """
    Updates the sports preferences for a specified user by modifying the database entry
    for that user. The sports preferences are fetched from the current session state variables.

    :param username: The unique identifier for the user whose sports preferences
                     need to be updated.
    :type username: str
    :return: None
    """
    st.session_state.sports = st.session_state.sports_key
    sports_string = ','.join(st.session_state.sports)

    with conn.session as session:
        session.execute(text(f"UPDATE {TABLE_USERS} SET sports = '{sports_string}' WHERE username = '{username}'"))
        session.commit()


@st.cache_data()
def change_markets(username: str):
    """
    Updates the markets for a user in the database and the current session state.

    This function synchronizes the local session state of the application with the
    persistent database storage. It retrieves the current list of markets from the
    session state and updates the associated record in the database for the provided
    username.

    :param username: The username of the user whose markets need to be updated.
    :type username: str
    :return: None
    """
    st.session_state.markets = st.session_state.markets_key
    markets_string = ','.join(st.session_state.markets)

    with conn.session as session:
        session.execute(text(f"UPDATE {TABLE_USERS} SET markets = '{markets_string}' WHERE username = '{username}'"))
        session.commit()


@st.cache_data()
def change_mindrop(username: str):
    """
    Updates the minimum value associated with the given username in the database.
    Also updates the session state with the new minimum value.

    :param username: The username of the user whose `mindrop` is being updated.
    :type username: str
    :return: None
    """
    st.session_state.mindrop = st.session_state.mindrop_key

    with conn.session as session:
        session.execute(text(f"UPDATE {TABLE_USERS} SET mindrop = {st.session_state.mindrop} WHERE username = '{username}'"))
        session.commit()


@st.cache_data()
def change_minodds(username: str):
    """
    Update the minimum odds value in the session state and persist the update to the database
    for the specified user.

    This function updates the `minodds` value of a user in both the Streamlit session state and
    the database. It retrieves the value from session state, applies the update locally,
    and performs a database query to ensure this change is reflected persistently
    in the user table of the data source.

    :param username: The username of the user whose minimum odds value is being updated.
    :type username: str
    :return: None
    """
    st.session_state.minodds = st.session_state.minodds_key

    with conn.session as session:
        session.execute(text(f"UPDATE {TABLE_USERS} SET minodds = {st.session_state.minodds} WHERE username = '{username}'"))
        session.commit()
        

@st.cache_data()
def change_maxodds(username: str):
    """
    Update the maxodds value for a specific user in the database. The maxodds
    value is fetched from the current session state and updated in the users
    table for the provided username.

    This function utilizes Streamlit's caching mechanism and ensures that
    the database update happens within an active session.

    :param username: The username of the user for whom the maxodds value
        will be updated
    :type username: str
    :return: None
    """
    st.session_state.maxodds = st.session_state.maxodds_key

    with conn.session as session:
        session.execute(text(f"UPDATE {TABLE_USERS} SET maxodds = {st.session_state.maxodds} WHERE username = '{username}'"))
        session.commit()
        

@st.cache_data()
def change_lookahead(username: str):
    """
    Updates the lookahead value for a specific user in the database and
    the session state based on the key `lookahead_key` in `st.session_state`.

    :param username: Username of the user whose lookahead value is to be
                     updated. The username is used to identify the user
                     in the database.
    :type username: str

    :return: None
    """
    st.session_state.lookahead = st.session_state.lookahead_key

    with conn.session as session:
        session.execute(text(f"UPDATE {TABLE_USERS} SET lookahead = {st.session_state.lookahead} WHERE username = '{username}'"))
        session.commit()
        

@st.cache_data()
def change_book1(username: str):
    """
    Updates the `book1` value for the given username in the database. This function modifies
    the `book1` state in the application and updates the corresponding record in the database.

    This function is cached to optimize the performance and reduce redundant executions.
    Caching is especially useful when dealing with session state or database interactions.

    :param username: The username of the user whose `book1` state should be updated.
    :type username: str
    :return: None
    """
    st.session_state.book1 = st.session_state.book1_key

    with conn.session as session:
        session.execute(text(f"UPDATE {TABLE_USERS} SET book1 = '{st.session_state.book1}' WHERE username = '{username}'"))
        session.commit()


@st.cache_data()
def change_book2(username: str):
    """
    Updates the 'book2' field for a given user in the database. The value of 'book2'
    is updated in the database based on the current state of 'st.session_state.book2'.

    Parameters should be carefully passed while using this function to ensure correct
    updates in the database.

    :param username: The username of the user whose 'book2' field is to be updated.
    :type username: str
    :return: None
    """
    st.session_state.book2 = st.session_state.book2_key

    with conn.session as session:
        session.execute(text(f"UPDATE {TABLE_USERS} SET book2 = '{st.session_state.book2}' WHERE username = '{username}'"))
        session.commit()
        

@st.cache_data()
def change_book3(username: str):
    """
    Updates the value of the `book3` attribute for the specified user in the database
    and the session state. The new value of `book3` is fetched from
    `st.session_state.book3_key`.

    :param username: The username whose `book3` attribute needs to be updated.
    :type username: str
    :return: None
    """
    st.session_state.book3 = st.session_state.book3_key

    with conn.session as session:
        session.execute(text(f"UPDATE {TABLE_USERS} SET book3 = '{st.session_state.book3}' WHERE username = '{username}'"))
        session.commit()


def set_telegram_button_pressed(username: str):
    """
    Updates the 'telegram_button_pressed' field in the user record with the current
    timestamp in the database. This function identifies the user by the given username
    and modifies their corresponding record.

    :param username: The identifier of the user whose database record needs to be
        updated with the current timestamp for the 'telegram_button_pressed' field.
    :type username: str
    :return: None
    """
    query = f"UPDATE {TABLE_USERS} SET telegram_button_pressed = '{datetime.now()}' WHERE username = '{username}'"

    with conn.session as session:
        session.execute(text(query))
        session.commit()


@st.cache_data()
def change_clear_cache(username: str):
    """
    Clears and updates the user's cache setting in the database. This function interacts
    with the database to modify the `clear_cache` property for the user with the specified
    username. The modified value is based on the session state's `clear_cache_key`.

    :param username: The username of the user whose cache setting
        is to be changed.
    :type username: str
    :return: None
    """
    st.session_state.clear_cache = st.session_state.clear_cache_key

    with conn.session as session:
        session.execute(text(f"UPDATE {TABLE_USERS} SET clear_cache = {st.session_state.clear_cache} WHERE username = '{username}'"))
        session.commit()


@st.cache_data()
def change_need_book(username: str):
    """
    Updates the `need_book` field for a specific user in the database based on the session state.

    This function modifies the value of `st.session_state.need_book`, then performs an
    SQL `UPDATE` query to set the corresponding `need_book` field in the user record
    where the username matches.

    :param username: The username of the user whose `need_book` field will be updated.
    :type username: str
    :return: None
    """
    st.session_state.need_book = st.session_state.need_book_key

    with conn.session as session:
        session.execute(text(f"UPDATE {TABLE_USERS} SET need_book = '{st.session_state.need_book}' WHERE username = '{username}'"))
        session.commit()

