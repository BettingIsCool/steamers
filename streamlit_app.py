import pytz
import toolkit
import streamlit as st

from config import BOOKS, TEXT_LANDING_PAGE, USER_DOMAIN_CHANGES

# set_page_config() can only be called once per app page, and must be called as the first Streamlit command in your script.
st.set_page_config(page_title="ChasingSteamers by BettingIsCool", page_icon="♨️", layout="wide", initial_sidebar_state="expanded")

import datetime
import pandas as pd
import db_steamers_remote as db
from streamlit_autorefresh import st_autorefresh

# TODO min_odds, max_odds, time_range filters
# TODO proper database indexing
# TODO default settings (timezone, decimal/american, default books, default min val)
# TODO create detailed stats with overview per book
# TODO retrieve odds from all bookmakers (update list of bookmakers every day)
# TODO add comments below table (bets for last hour, don't hot refresh, advice)
# TODO option to add to Track-A-Bet on the fly
# TODO add media
# TODO major refactoring


placeholder1 = st.empty()

if 'display_landing_page_text' not in st.session_state:

    # Display landing page (pre login)
    placeholder1.markdown(TEXT_LANDING_PAGE)
    st.session_state.display_landing_page_text = True

# Add google authentication (only users with a valid stripe subscription can log in)
# Username must match the registered email-address at stripe
# IMPORTANT: st_paywall is a forked library. This fork supports additional verification, i.e. if the user has a valid subscription for the product
# The original st_paywall just looks into the stripe account for ANY valid subscription for that particular user, but doesn't care if this subscription is actually valid for a specific app.
# See also https://github.com/tylerjrichards/st-paywall/issues/75
# Importing this fork can be done with 'git+https://github.com/bettingiscool/st-paywall_fork.git@main' in the requirements.txt file

from st_paywall import add_auth
add_auth(required=True)

username = st.session_state.email

st.write()

placeholder1.empty()

# Check if username is in database, otherwise append the user
if 'users_fetched' not in st.session_state:
    toolkit.clear_cache()
    if username not in set(db.get_users()):
        db.append_user(data={'username': username})
        st.session_state.user_id = username
        st.session_state.session_id = username + '_' + str(datetime.datetime.now())

    # Create session token
    else:
        st.session_state.user_id = username
        st.session_state.session_id = username + '_' + str(datetime.datetime.now())
        toolkit.get_active_session.clear()
        aux_active_session = toolkit.get_active_session(st.session_state.user_id)

    st.session_state.user_dbid = db.get_user_dbid(username=username)[0]
    st.session_state.users_fetched = True


# Allow only ONE session per user
# See https://discuss.streamlit.io/t/right-way-to-manage-same-user-opening-multiple-sessions/25608

if st.session_state.session_id == toolkit.get_active_session(st.session_state.user_id):

    # Get user preferences
    if 'default_odds_display' not in st.session_state:
        st.session_state.default_odds_display = db.get_user_setting(username=username, param='default_odds_display')
    if 'default_timezone' not in st.session_state:
        st.session_state.default_timezone = db.get_user_setting(username=username, param='default_timezone')
    if 'default_minval' not in st.session_state:
        st.session_state.default_minval = db.get_user_setting(username=username, param='default_minval')
    if 'default_minodds' not in st.session_state:
        st.session_state.default_minodds = db.get_user_setting(username=username, param='default_minodds')
    if 'default_maxodds' not in st.session_state:
        st.session_state.default_maxodds = db.get_user_setting(username=username, param='default_maxodds')
    if 'default_book1' not in st.session_state:
        st.session_state.default_book1 = db.get_user_setting(username=username, param='default_book1')
    if 'default_book2' not in st.session_state:
        st.session_state.default_book2 = db.get_user_setting(username=username, param='default_book2')
    if 'default_book3' not in st.session_state:
        st.session_state.default_book3 = db.get_user_setting(username=username, param='default_book3')
    if 'default_book4' not in st.session_state:
        st.session_state.default_book4 = db.get_user_setting(username=username, param='default_book4')
    if 'default_book5' not in st.session_state:
        st.session_state.default_book5 = db.get_user_setting(username=username, param='default_book5')

    if 'id_max' not in st.session_state:
        st.session_state.id_max = 0

    # Welcome message in the sidebar
    st.sidebar.subheader(f"Welcome {username}")
    st.sidebar.write(f"Default settings")

    # update every 5 seconds
    st_autorefresh(interval=10 * 1000, debounce=True, key="dataframerefresh")

    selected_books = st.multiselect(label='Bookmakers', options=BOOKS.keys(), default=[st.session_state.default_book1, st.session_state.default_book2, st.session_state.default_book3, st.session_state.default_book4, st.session_state.default_book5], format_func=lambda x: BOOKS.get(x), help='Default bookmakers will always show up. You can add more bookmakers here.')
    selected_books = [f"'{s}'" for s in selected_books]
    selected_books = f"({','.join(selected_books)})"

    col_minval, col_minodds, col_maxodds, col_datefrom, col_lookahead = st.columns([1, 1, 1, 1, 1])

    with col_minval:
        selected_minval = st.slider(label='Minimum Value Threshold', min_value=0.025, max_value=1.00, value=st.session_state.default_minval, step=0.005, format="%0.3f")

    with col_minodds:
        selected_minodds = st.slider(label='Minimum Odds', min_value=1.00, max_value=10.00, value=st.session_state.default_minodds, step=0.05, format="%0.2f")

    with col_maxodds:
        selected_maxodds = st.slider(label='Maximum Odds', min_value=selected_minodds, max_value=100.00, value=st.session_state.default_maxodds, step=0.05, format="%0.2f")

    with col_lookahead:
        selected_lookahead = st.slider(label='Lookahead', min_value=1, max_value=1000, value=8, step=1, help='Show only events that start within the next x hours.')

    if selected_books != '()':

        bets = db.get_log(bookmakers=selected_books, minval=selected_minval, minodds=selected_minodds, maxodds=selected_maxodds, lookahead=selected_lookahead)

        if bets:

            bets_df = pd.DataFrame(data=bets)

            # Change bookie domains
            if st.session_state.user_dbid in USER_DOMAIN_CHANGES.keys():
                for domain_original, domain_changed in USER_DOMAIN_CHANGES[st.session_state.user_dbid].items():
                    bets_df['book_url'] = bets_df['book_url'].str.replace(domain_original, domain_changed)

            # Compute time difference for UPDATED column
            for index, row in bets_df.iterrows():
                bets_df.at[index, 'updated_ago'] = f"{int((datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) - row['timestamp_utc']).total_seconds())} s ago"

            # Play notification sound if new bet
            if bets_df['id'].max() > st.session_state.id_max:
                st.session_state.id_max = bets_df['id'].max()
                toolkit.play_notification()

            bets_df = bets_df.rename(columns={'sport_name': 'SPORT', 'league_name': 'LEAGUE', 'runner_home': 'RUNNER_HOME', 'runner_away': 'RUNNER_AWAY', 'selection': 'SELECTION', 'market': 'MARKET', 'line': 'LINE', 'prev_odds': 'PODDS', 'curr_odds': 'CODDS', 'droppct': 'DROPPCT', 'oddstobeat': 'OTB', 'book_odds': 'ODDS', 'book_val': 'VALUE', 'book_name': 'BOOK', 'book_url': 'LINK', 'id': 'ID', 'bet_str': 'BET', 'drop_str': 'DROP', 'timestamp_utc': 'TIMESTAMP', 'starts_utc': 'STARTS', 'updated_ago': 'UPDATED'})
            bets_df = bets_df[['UPDATED', 'BET', 'ODDS', 'BOOK', 'VALUE', 'DROP', 'OTB', 'LINK', 'STARTS', 'SPORT', 'LEAGUE', 'RUNNER_HOME', 'RUNNER_AWAY']]

            styled_df = bets_df.style.set_properties(**{'color': 'gray'}, subset=['UPDATED', 'DROP', 'STARTS', 'SPORT', 'LEAGUE', 'RUNNER_HOME', 'RUNNER_AWAY']).set_properties(**{'color': 'red'}, subset=['OTB']).applymap(toolkit.color_cells, subset=['VALUE']).format({'LINE': '{:g}'.format, 'PODDS': '{:,.3f}'.format, 'CODDS': '{:,.3f}'.format, 'ODDS': '{:,.3f}'.format, 'OTB': '{:,.3f}'.format, 'VALUE': '{:,.2%}'.format})
            st.dataframe(styled_df, column_config={"LINK": st.column_config.LinkColumn("LINK")}, hide_index=True)

    st.cache_data.clear()

    # Create a radio button for Decimal/American odds format
    odds_display_options = ['Decimal', 'American']
    st.session_state.default_odds_display = st.sidebar.radio(label="Select odds format", options=odds_display_options, index=odds_display_options.index(st.session_state.default_odds_display), horizontal=True, on_change=db.change_user_odds_display, args=(username, placeholder1), key='default_odds_display_key')

    # Create selectbox for timezone
    timezone_options = pytz.common_timezones
    st.session_state.default_timezone = st.sidebar.selectbox(label="Select timezone", options=timezone_options, index=timezone_options.index(st.session_state.default_timezone), on_change=db.change_user_timezone, args=(username, placeholder1), key='default_timezone_key')

    # Create number input for default_minval
    st.session_state.default_minval = st.sidebar.number_input("Select default minimum value threshold", min_value=0.025, max_value=1.00, value=st.session_state.default_minval, step=0.005, format="%0.3f", on_change=db.change_user_minval, args=(username, placeholder1), key='default_minval_key', help='Enter percentage as decimal number. 5% = 0.05')

    # Create number input for default_minodds
    st.session_state.default_minodds = st.sidebar.number_input("Select default minimum odds", min_value=1.00, max_value=10.00, value=st.session_state.default_minodds, step=0.05, format="%0.2f", on_change=db.change_user_minodds, args=(username, placeholder1), key='default_minodds_key')

    # Create number input for default_maxodds
    st.session_state.default_maxodds = st.sidebar.number_input("Select default maximum odds", min_value=st.session_state.default_minodds, max_value=100.00, value=st.session_state.default_maxodds, step=0.05, format="%0.2f", on_change=db.change_user_maxodds, args=(username, placeholder1), key='default_maxodds_key')

    # Create text input for default_book1
    st.session_state.default_book1 = st.sidebar.selectbox(label="Select default bookmaker 1", options=BOOKS.keys(), index=list(BOOKS.keys()).index(st.session_state.default_book1), format_func=lambda x: BOOKS.get(x), on_change=db.change_user_book1, args=(username, placeholder1), key='default_book1_key')

    # Create text input for default_book2
    st.session_state.default_book2 = st.sidebar.selectbox(label="Select default bookmaker 2", options=BOOKS.keys(), index=list(BOOKS.keys()).index(st.session_state.default_book2), format_func=lambda x: BOOKS.get(x), on_change=db.change_user_book2, args=(username, placeholder1), key='default_book2_key')

    # Create text input for default_book3
    st.session_state.default_book3 = st.sidebar.selectbox(label="Select default bookmaker 3", options=BOOKS.keys(), index=list(BOOKS.keys()).index(st.session_state.default_book3), format_func=lambda x: BOOKS.get(x), on_change=db.change_user_book3, args=(username, placeholder1), key='default_book3_key')

    # Create text input for default_book4
    st.session_state.default_book4 = st.sidebar.selectbox(label="Select default bookmaker 4", options=BOOKS.keys(), index=list(BOOKS.keys()).index(st.session_state.default_book4), format_func=lambda x: BOOKS.get(x), on_change=db.change_user_book4, args=(username, placeholder1), key='default_book4_key')

    # Create text input for default_book5
    st.session_state.default_book5 = st.sidebar.selectbox(label="Select default bookmaker 5", options=BOOKS.keys(), index=list(BOOKS.keys()).index(st.session_state.default_book5), format_func=lambda x: BOOKS.get(x), on_change=db.change_user_book5, args=(username, placeholder1), key='default_book5_key')

else:
    st.info('Your session has expired')
    for key in st.session_state.keys():
        del st.session_state[key]
