# The module 'db_steamers_remote.py' uses sqlalchemy as the database connector which is the preferred way for streamlit
# The module 'db_steamers_remote2.py' uses mysql-connector-python

import time
import streamlit as st
from sqlalchemy import text
from datetime import datetime
from config import TABLE_LEAGUES, TABLE_FIXTURES, TABLE_ODDS, TABLE_RESULTS, TABLE_BETS, TABLE_USERS

conn = st.connection('steamers', type='sql')


@st.cache_data()
def get_log():
    """
    :param username: The username of the individual placing the bets.
    :param sports: A string specifying which sports to include in the query.
    :param bookmakers: A string specifying which bookmakers to include in the query.
    :param tags: A string specifying which tags to include in the query.
    :param date_from: The start date for filtering bets.
    :param date_to: The end date for filtering bets.
    :return: A list of dictionaries containing bet details filtered by the given criteria.
    """
    return conn.query(f"SELECT starts, sport_name, league_name, runner_home, runner_away, selection, market, line FROM {TABLE_LOG} ORDER BY starts").to_dict('records')