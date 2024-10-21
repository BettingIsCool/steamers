import streamlit as st

# set_page_config() can only be called once per app page, and must be called as the first Streamlit command in your script.
st.set_page_config(page_title="ChasingSteamers (Ultra Feed) by BettingIsCool", page_icon="♨️", layout="wide", initial_sidebar_state="expanded")

import pandas as pd
from datetime import datetime
import db_steamers_remote as db

while True:

    bets = db.get_log()
    bets_df = pd.DataFrame(data=bets)
    st.write(bets_df)

    if datetime.now().second % 5 == 0:
        st.rerun()


