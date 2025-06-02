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

    return conn.query(f"SELECT username FROM {TABLE_USERS}")['username'].tolist()


@st.cache_data()
def append_user(data: dict):

    query = f"INSERT INTO {TABLE_USERS} (username, sports, markets, minval, minodds, maxodds, lookahead, book1, book2, book3) VALUES(:username, :sports, :markets, :minval, :minodds, :maxodds, :lookahead, :book1, :book2, :book3)"

    with conn.session as session:
        session.execute(text(query), params=dict(username=data['username'], sports='Alpine Skiing,Archery,Athletics,Aussie Rules,Badminton,Bandy,Baseball,Basketball,Beach Volleyball,Biathlon,Bobsleigh,Boxing,Chess,Cricket,Cross Country,Crossfit,Curling,Cycling,Darts,Drone Racing,E Sports,Entertainment,Field Hockey,Figure Skating,Floorball,Football,Formula 1,Freestyle Skiing,Futsal,Golf,Handball,Hockey,Horse Racing Specials,Lacrosse,Luge,Mixed Martial Arts,Motorsport,Nordic Combined,Olympics,Other Sports,Padel Tennis,Pickleball,Poker,Politics,Rugby League,Rugby Union,Short Track,Simulated Games,Skeleton,Ski Jumping,Slap Fighting,Snooker,Snow Boarding,Soccer,Softball,Speed Skating,Squash,Sumo,Table Tennis,Tennis,Volleyball,Water Polo', markets='moneyline,spread,totals', minval=0.10, minodds=1.01, maxodds=100.00, lookahead=8, book1='No Book', book2='No Book', book3='No Book'))
        session.commit()


@st.cache_data()
def get_user_setting(username: str, param: str):

    return conn.query(f"SELECT {param} FROM {TABLE_USERS} WHERE username = '{username}'")[param].tolist()[0]


@st.cache_data()
def change_sports(username: str):

    st.session_state.sports = st.session_state.sports_key
    sports_string = ','.join(st.session_state.sports)

    with conn.session as session:
        session.execute(text(f"UPDATE {TABLE_USERS} SET sports = '{sports_string}' WHERE username = '{username}'"))
        session.commit()


@st.cache_data()
def change_markets(username: str):

    st.session_state.markets = st.session_state.markets_key
    markets_string = ','.join(st.session_state.markets)

    with conn.session as session:
        session.execute(text(f"UPDATE {TABLE_USERS} SET markets = '{markets_string}' WHERE username = '{username}'"))
        session.commit()


@st.cache_data()
def change_minval(username: str):

    st.session_state.minval = st.session_state.minval_key

    with conn.session as session:
        session.execute(text(f"UPDATE {TABLE_USERS} SET minval = {st.session_state.minval} WHERE username = '{username}'"))
        session.commit()
