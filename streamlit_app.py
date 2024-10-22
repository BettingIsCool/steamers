from filecmp import clear_cache

import streamlit as st

# set_page_config() can only be called once per app page, and must be called as the first Streamlit command in your script.
st.set_page_config(page_title="ChasingSteamers (Ultra Feed) by BettingIsCool", page_icon="♨️", layout="wide", initial_sidebar_state="expanded")

import pandas as pd
import db_steamers_remote as db
from streamlit_autorefresh import st_autorefresh

# TODO add multiple product ids in st.secrets
# TODO create slogans with grok
# TODO sound_alert if id > id_max
# TODO create detailed stats with overview per book
# TODO deposit tipico/interwetten from bank account (check which accounts worthwhile from log)
# TODO Your one-click app for profits
# TODO add images/media to datafram

# update every 5 seconds
st_autorefresh(interval=10 * 1000, debounce=True, key="dataframerefresh")

bets = db.get_log()
bets_df = pd.DataFrame(data=bets)
bets_df = bets_df.rename(columns={'start_time': 'STARTS', 'sport_name': 'SPORT', 'league_name': 'LEAGUE', 'runner_home': 'RUNNER_HOME', 'runner_away': 'RUNNER_AWAY', 'selection': 'SELECTION', 'market': 'MARKET', 'line': 'LINE', 'prev_odds': 'PODDS', 'curr_odds': 'CODDS', 'droppct': 'DROP', 'oddstobeat': 'OTB', 'book_odds': 'BODDS', 'book_val': 'BVAL', 'book_name': 'BNAME', 'book_url': 'BURL', 'timestamp': 'TIMESTAMP', 'id': 'ID'})
styled_df = bets_df.style.format({'LINE': '{:g}'.format, 'PODDS': '{:,.3f}'.format, 'CODDS': '{:,.3f}'.format, 'BODDS': '{:,.3f}'.format, 'OTB': '{:,.3f}'.format, 'BVAL': '{:,.2%}'.format})
st.dataframe(styled_df, column_config={"BURL": st.column_config.LinkColumn("BURL")})
st.cache_data.clear()

