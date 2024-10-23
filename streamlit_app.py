import toolkit
import streamlit as st

from config import BOOKS, TEXT_LANDING_PAGE, USER_DOMAIN_CHANGES

# set_page_config() can only be called once per app page, and must be called as the first Streamlit command in your script.
st.set_page_config(page_title="ChasingSteamers by BettingIsCool", page_icon="♨️", layout="wide", initial_sidebar_state="expanded")

import pandas as pd
import datetime
import db_steamers_remote as db
from streamlit_autorefresh import st_autorefresh

# TODO min_odds, max_odds, time_range filters
# TODO proper database indexing
# TODO default settings (timezone, decimal/american, default books, default min val)
# TODO create detailed stats with overview per book
# TODO add images/media to dataframe
# TODO 1 secs ago, 3 min ago in FIRST column (running counter streamlit)
# TODO retrieve odds from all bookmakers (update list of bookmakers every day)
# TODO possibility to change domain .de to .at (or com interwetten) with USER_DOMAIN_CHANGES
# TODO list bets for last hour
# TODO add comments below table (bets for last hour, don't hot refresh, advice)
# TODO overview of different plans (grid) -> advanced algorithm for ultra (logarithmic), supported sports,
# TODO option to add to Track-A-Bet on the fly
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

    # update every 5 seconds
    st_autorefresh(interval=10 * 1000, debounce=True, key="dataframerefresh")

    if 'id_max' not in st.session_state:
        st.session_state.id_max = 0

    selected_books = st.multiselect(label='Bookmakers', options=BOOKS.keys(), format_func=lambda x: BOOKS.get(x), help='Select book(s) you wish to get bets for.')
    selected_books = [f"'{s}'" for s in selected_books]
    selected_books = f"({','.join(selected_books)})"

    if selected_books != '()':

        bets = db.get_log(bookmakers=selected_books)

        if bets:

            bets_df = pd.DataFrame(data=bets)
            bets_df['book_url'].replace('.de', '.com', inplace=True)

            # Change bookie domains
            #if st.session_state.user_dbid in USER_DOMAIN_CHANGES.keys():
            #    for domain_original, domain_changed in USER_DOMAIN_CHANGES[st.session_state.user_dbid].items():
            #        bets_df['book_url'].replace(domain_original, domain_changed, inplace=True)
            #        st.write(domain_original, domain_changed)
                    #for index, row in bets_df.iterrows():
                    #    if domain_original in row['book_url']:
                    #        st.write('yes')


            bets_df = bets_df.rename(columns={'starts': 'STARTS', 'sport_name': 'SPORT', 'league_name': 'LEAGUE', 'runner_home': 'RUNNER_HOME', 'runner_away': 'RUNNER_AWAY', 'selection': 'SELECTION', 'market': 'MARKET', 'line': 'LINE', 'prev_odds': 'PODDS', 'curr_odds': 'CODDS', 'droppct': 'DROP', 'oddstobeat': 'OTB', 'book_odds': 'BODDS', 'book_val': 'BVAL', 'book_name': 'BNAME', 'book_url': 'BURL', 'timestamp': 'TIMESTAMP', 'id': 'ID'})
            bets_df = bets_df[['TIMESTAMP', 'STARTS', 'SPORT', 'LEAGUE', 'RUNNER_HOME', 'RUNNER_AWAY', 'MARKET', 'SELECTION', 'LINE', 'BODDS', 'BVAL', 'BNAME', 'BURL', 'ID']]

            styled_df = bets_df.style.format({'LINE': '{:g}'.format, 'PODDS': '{:,.3f}'.format, 'CODDS': '{:,.3f}'.format, 'BODDS': '{:,.3f}'.format, 'OTB': '{:,.3f}'.format, 'BVAL': '{:,.2%}'.format})
            st.dataframe(styled_df, column_config={"BURL": st.column_config.LinkColumn("BURL")}, hide_index=True)

            # Play notification sound if new bet
            if bets_df['ID'].max() > st.session_state.id_max:
                st.session_state.id_max = bets_df['ID'].max()
                toolkit.play_notification()

    st.cache_data.clear()

else:
    st.info('Your session has expired')
    for key in st.session_state.keys():
        del st.session_state[key]
