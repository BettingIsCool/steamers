import time
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

# TODO Remove user from database if sub cancelled (check subscription via strip api)
# TODO Fitzdares/bet600/fafabet/betgoodwin, Smarkets and SBK, ladbrokes AU
# TODO retrieve odds from all bookmakers (update list of bookmakers every day)
# TODO add media
# TODO major refactoring
# TODO Bad message format - Tried to use SessionInfo before it was initialized, see: https://www.restack.io/docs/streamlit-knowledge-streamlit-bad-message-format-fix
# TODO replace url with 'Link': https://discuss.streamlit.io/t/st-data-editor-linkcolumn-with-different-label-and-url/45757

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

# Maybe a short delay helps to avoid "Bad message format - Tried to use SessionInfo before it was initialized"
time.sleep(0.25)
username = st.session_state.email

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
    st.session_state.telegram_user_id = db.get_telegram_user_id(username=username)[0]
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
    if 'default_lookahead' not in st.session_state:
        st.session_state.default_lookahead = db.get_user_setting(username=username, param='default_lookahead')
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

    if st.session_state.telegram_user_id is None:

        #st.sidebar.link_button(label='Connect Telegram', url='https://t.me/psp_ultra_bot', on_click=toolkit.open_page(url='https://t.me/psp_ultra_bot'), help='Hit this button to receive telegram alerts.', type='primary')
        st.sidebar.button('Connect Telegram', help='Hit this button to receive telegram alerts.', type='primary', on_click=toolkit.redirect_button)
        st.session_state.telegram_user_id = db.get_telegram_user_id(username=username)[0]

    st.sidebar.subheader(f"Default settings", help='Your standard settings every time you log in. These are also the settings applied to your telegram alerts.')
    # update every 5 seconds
    st_autorefresh(interval=10 * 1000, debounce=True, key="dataframerefresh")

    selected_books = st.multiselect(label='Bookmakers', options=BOOKS.keys(), default=[st.session_state.default_book1, st.session_state.default_book2, st.session_state.default_book3, st.session_state.default_book4, st.session_state.default_book5], format_func=lambda x: BOOKS.get(x), help='Default bookmakers will always show up. You can add more bookmakers here.')
    selected_books = [f"'{s}'" for s in selected_books]
    selected_books = f"({','.join(selected_books)})"

    col_minval, col_minodds, col_maxodds, col_lookahead = st.columns([1, 1, 1, 1])

    with col_minval:
        selected_minval = st.slider(label='Minimum Value Threshold', min_value=0.025, max_value=1.00, value=st.session_state.default_minval, step=0.005, format="%0.3f", help='Enter percentage as decimal number. 5% = 0.05')

    with col_minodds:
        if st.session_state.default_odds_display == 'American':
            selected_minodds_american = st.slider(label='Minimum Odds', min_value=-10000.00, max_value=10000.00, value=st.session_state.default_minodds, step=1.00)
            selected_minodds = toolkit.get_decimal_odds(american_odds=selected_minodds_american)
        else:
            selected_minodds = st.slider(label='Minimum Odds', min_value=1.00, max_value=10.00, value=st.session_state.default_minodds, step=0.05, format="%0.2f")

    with col_maxodds:
        if st.session_state.default_odds_display == 'American':
            selected_maxodds_american = st.slider(label='Maximum Odds', min_value=selected_minodds_american, max_value=10000.00, value=st.session_state.default_maxodds, step=1.00)
            selected_maxodds = toolkit.get_decimal_odds(american_odds=selected_maxodds_american)
        else:
            selected_maxodds = st.slider(label='Maximum Odds', min_value=selected_minodds, max_value=100.00, value=st.session_state.default_maxodds, step=0.05, format="%0.2f")

    with col_lookahead:
        selected_lookahead = st.slider(label='Lookahead (in hours)', min_value=1, max_value=500, value=st.session_state.default_lookahead, step=1, help='Show only events that start within the next x hours.')

    if selected_books != '()':
        bets = db.get_log(bookmakers=selected_books, minval=selected_minval, minodds=selected_minodds, maxodds=selected_maxodds, lookahead=selected_lookahead)

        if bets:

            bets_df = pd.DataFrame(data=bets)

             # Convert datetimes to user timezone
            # There is a possibility that the conversion fails if the timestamp falls into a time change
            # See https://github.com/streamlit/streamlit/issues/1288
            try:
                #bets_df.starts_utc = bets_df.starts_utc.dt.tz_localize('Europe/London').dt.tz_convert(st.session_state.default_timezone).dt.tz_localize(None)
                bets_df['starts_utc'] = bets_df['starts_utc'].dt.tz_localize('utc').dt.tz_convert(st.session_state.default_timezone).dt.tz_localize(None)
            except Exception as ex:
                pass

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

            if st.session_state.default_odds_display == 'American':
                bets_df = bets_df.rename(columns={'sport_name': 'SPORT', 'league_name': 'LEAGUE', 'runner_home': 'RUNNER_HOME', 'runner_away': 'RUNNER_AWAY', 'selection': 'SELECTION', 'market': 'MARKET', 'line': 'LINE', 'prev_odds': 'PODDS', 'curr_odds': 'CODDS', 'droppct': 'DROPPCT', 'oddstobeat': 'OTB', 'book_odds': 'ODDS', 'book_val': 'VALUE', 'book_name': 'BOOK', 'book_url': 'LINK', 'id': 'ID', 'bet_str': 'BET', 'drop_str_american': 'DROP', 'timestamp_utc': 'TIMESTAMP', 'starts_utc': 'STARTS', 'updated_ago': 'ALERT'})
            else:
                bets_df = bets_df.rename(columns={'sport_name': 'SPORT', 'league_name': 'LEAGUE', 'runner_home': 'RUNNER_HOME', 'runner_away': 'RUNNER_AWAY', 'selection': 'SELECTION', 'market': 'MARKET', 'line': 'LINE', 'prev_odds': 'PODDS', 'curr_odds': 'CODDS', 'droppct': 'DROPPCT', 'oddstobeat': 'OTB', 'book_odds': 'ODDS', 'book_val': 'VALUE', 'book_name': 'BOOK', 'book_url': 'LINK', 'id': 'ID', 'bet_str': 'BET', 'drop_str': 'DROP', 'timestamp_utc': 'TIMESTAMP', 'starts_utc': 'STARTS', 'updated_ago': 'ALERT'})
            bets_df = bets_df[['ALERT', 'BET', 'ODDS', 'BOOK', 'VALUE', 'DROP', 'OTB', 'LINK', 'STARTS', 'SPORT', 'LEAGUE', 'RUNNER_HOME', 'RUNNER_AWAY']]

            if st.session_state.default_odds_display == 'American':
                bets_df.ODDS = bets_df.ODDS.apply(toolkit.get_american_odds)
                bets_df.OTB = bets_df.OTB.apply(toolkit.get_american_odds)
                styled_df = bets_df.style.set_properties(**{'color': 'gray'}, subset=['ALERT', 'DROP', 'STARTS', 'SPORT', 'LEAGUE', 'RUNNER_HOME', 'RUNNER_AWAY']).set_properties(**{'color': 'red'}, subset=['OTB']).applymap(toolkit.color_cells, subset=['VALUE']).format({'LINE': '{:g}'.format, 'PODDS': '{:,.3f}'.format, 'CODDS': '{:,.3f}'.format, 'ODDS': '{0:g}'.format, 'OTB': '{0:g}'.format, 'VALUE': '{:,.2%}'.format})
            else:
                styled_df = bets_df.style.set_properties(**{'color': 'gray'}, subset=['ALERT', 'DROP', 'STARTS', 'SPORT', 'LEAGUE', 'RUNNER_HOME', 'RUNNER_AWAY']).set_properties(**{'color': 'red'}, subset=['OTB']).applymap(toolkit.color_cells, subset=['VALUE']).format({'LINE': '{:g}'.format, 'PODDS': '{:,.3f}'.format, 'CODDS': '{:,.3f}'.format, 'ODDS': '{:,.3f}'.format, 'OTB': '{:,.3f}'.format, 'VALUE': '{:,.2%}'.format})

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
    if st.session_state.default_odds_display == 'American':
        st.session_state.default_minodds = st.sidebar.number_input("Select default minimum odds", min_value=-10000.00, max_value=10000.00, value=st.session_state.default_minodds, step=1.00, on_change=db.change_user_minodds, args=(username, placeholder1), key='default_minodds_key')
    else:
        st.session_state.default_minodds = 1.00 if st.session_state.default_minodds < 1.00 else st.session_state.default_minodds
        st.session_state.default_minodds = st.sidebar.number_input("Select default minimum odds", min_value=1.00, max_value=10.00, value=st.session_state.default_minodds, step=0.05, format="%0.2f", on_change=db.change_user_minodds, args=(username, placeholder1), key='default_minodds_key')

    # Create number input for default_maxodds
    if st.session_state.default_odds_display == 'American':
        st.session_state.default_maxodds = st.sidebar.number_input("Select default maximum odds", min_value=st.session_state.default_minodds, max_value=10000.00, value=st.session_state.default_maxodds, step=1.00, on_change=db.change_user_maxodds, args=(username, placeholder1), key='default_maxodds_key')
    else:
        st.session_state.default_minodds = 1.00 if st.session_state.default_minodds < 1.00 else st.session_state.default_minodds
        st.session_state.default_maxodds = 100.00 if st.session_state.default_maxodds > 100.00 else st.session_state.default_maxodds
        st.session_state.default_maxodds = st.sidebar.number_input("Select default maximum odds", min_value=st.session_state.default_minodds, max_value=100.00, value=st.session_state.default_maxodds, step=0.05, format="%0.2f", on_change=db.change_user_maxodds, args=(username, placeholder1), key='default_maxodds_key')

    # Create number input for default_lookahead
    st.session_state.default_lookahead = st.sidebar.number_input("Select default lookahead (in hours)", min_value=1, max_value=500, value=st.session_state.default_lookahead, step=1, on_change=db.change_user_lookahead, args=(username, placeholder1), key='default_lookahead_key', help='Show only events that start within the next x hours.')

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

    st.write("⚠️️The bot will send instant alerts for significant price drops at sharp bookmakers. Such drops will yield opportunities at (soft) bookmakers who are too slow adjusting their prices. Once the alert hits the app/telegram place the bet immediately using the included bookmaker links. Each alert has a minimum price included (= otb). Don't bet below this price! If the odds have fallen below otb, skip the bet and move on.")

    st.write("⚠️ ATTENTION TELEGRAM USERS! Default settings (left sidebar) will be applied to your telegram alerts. The above filters won't have an effect on your telegram alerts.")

    st.write("️⚠️ The app updates automatically. DO NOT REFRESH YOUR BROWSER! Every refresh results in a log out.")

    st.write("👉 OTB (odds to beat) represents the fair odds and is the theoretical break-even point. In other words: In order to make money long-term you need to get a price higher than the 'odds to beat' price.")

    st.write("👉 Don’t judge your bet record too early! Variance plays a huge role in sportsbetting and even samples over a few hundred bets are often meaningless if you consider the actual profits only.")

    st.write("👉 The way to judge your bets is via clv (closing line value). This is an important concept to understand! There is a 2-part video series on this subject: Part I: https://youtube.com/watch?v=-uLJUhbFD_U, Part II: https://youtube.com/watch?v=MZCeHiywKvs")

    st.write("👉 Annual membership available if paid with crypto. Please get in touch at contact@bettingiscool.com")

    st.write("💰 Good luck with your betting!")

else:
    st.info('Your session has expired')
    for key in st.session_state.keys():
        del st.session_state[key]
