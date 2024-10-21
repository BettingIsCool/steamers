import streamlit as st

# set_page_config() can only be called once per app page, and must be called as the first Streamlit command in your script.
st.set_page_config(page_title="ChasingSteamers (Ultra Feed) by BettingIsCool", page_icon="♨️", layout="wide", initial_sidebar_state="expanded")

import time
import pytz
import math
import tools
import datetime
import pandas as pd
import db_pinnacle_remote as db


bets = db.get_bets()
bets_df = pd.DataFrame(data=bets)
st.write(bets_df)
