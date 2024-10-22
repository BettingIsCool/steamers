import streamlit as st

# set_page_config() can only be called once per app page, and must be called as the first Streamlit command in your script.
st.set_page_config(page_title="ChasingSteamers (Ultra Feed) by BettingIsCool", page_icon="♨️", layout="wide", initial_sidebar_state="expanded")

import pandas as pd
import db_steamers_remote as db
from streamlit_autorefresh import st_autorefresh

# update every 5 seconds
st_autorefresh(interval=5 * 1000, debounce=True, key="dataframerefresh")

bets = db.get_log()
bets_df = pd.DataFrame(data=bets)
st.write(bets_df)
