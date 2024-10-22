import toolkit
import streamlit as st

from config import BOOKS

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
# TODO add images/media to dataframe
# TODO retrieve odds from all bookmakers (update list of bookmakers every day)
# TODO line = -line if spread_away

# update every 5 seconds
st_autorefresh(interval=10 * 1000, debounce=True, key="dataframerefresh")

if 'id_max' not in st.session_state:
    st.session_state.id_max = 0

selected_books = st.multiselect(label='Bookmakers', options=BOOKS.keys(), format_func=lambda x: BOOKS.get(x), help='Select book(s) you wish to get bets for.')
selected_books = [f"'{s}'" for s in selected_books]
selected_books = f"({','.join(selected_books)})"

if selected_books:
    bets = db.get_log(bookmakers=selected_books)

    bets_df = pd.DataFrame(data=bets)
    bets_df = bets_df.rename(columns={'starts': 'STARTS', 'sport_name': 'SPORT', 'league_name': 'LEAGUE', 'runner_home': 'RUNNER_HOME', 'runner_away': 'RUNNER_AWAY', 'selection': 'SELECTION', 'market': 'MARKET', 'line': 'LINE', 'prev_odds': 'PODDS', 'curr_odds': 'CODDS', 'droppct': 'DROP', 'oddstobeat': 'OTB', 'book_odds': 'BODDS', 'book_val': 'BVAL', 'book_name': 'BNAME', 'book_url': 'BURL', 'timestamp': 'TIMESTAMP', 'id': 'ID'})
    styled_df = bets_df.style.format({'LINE': '{:g}'.format, 'PODDS': '{:,.3f}'.format, 'CODDS': '{:,.3f}'.format, 'BODDS': '{:,.3f}'.format, 'OTB': '{:,.3f}'.format, 'BVAL': '{:,.2%}'.format})
    st.dataframe(styled_df, column_config={"BURL": st.column_config.LinkColumn("BURL")})

    # Play notification sound if new bet
    if bets_df['ID'].max() > st.session_state.id_max:
        st.session_state.id_max = bets_df['ID'].max()
        toolkit.play_notification()

st.cache_data.clear()


