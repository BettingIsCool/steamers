import base64
import streamlit as st
import db_steamers_remote


def play_notification():

    # Example audio file or URL - thanx Grok!
    audio_file = "bell-ringing-05.wav"
    audio_bytes = open(audio_file, 'rb').read()
    encoded_audio = base64.b64encode(audio_bytes).decode()

    # HTML to embed audio with autoplay and hidden controls
    html_code = f'''
            <audio autoplay style="display:none;">
              <source src="data:audio/wav;base64,{encoded_audio}" type="audio/wav">
            </audio>
            '''
    st.markdown(html_code, unsafe_allow_html=True)


def clear_cache():
    """
    Clears the cached data for Streamlit application.

    :return: None
    """
    st.cache_data.clear()


@st.cache_resource()
def get_active_session(username: str):
    """
    :return: The session ID of the active session for the specified user.
    """
    return st.session_state.session_id


def color_cells(val: float):

    if val >= 0.05:
        color = 'green'
    elif val > 0:
        color = 'yellow'
    else:
        color = 'gray'

    return f'color: {color}'


def get_american_odds(decimal_odds: float):
    """
    :param decimal_odds: The decimal odds value to be converted to American odds format.
    :return: The corresponding American odds value.
    """
    return int((decimal_odds - 1) * 100) if decimal_odds >= 2.00 else int(-100 / (decimal_odds - 1))


def get_decimal_odds(american_odds: int):
    """
    :param american_odds: American odds value for which the decimal odds are to be calculated.
    :type american_odds: int
    :return: Decimal odds corresponding to the given American odds.
    :rtype: float
    """
    return american_odds / 100 + 1 if american_odds >= 0 else - 100 / american_odds + 1


def redirect_button():
    url = 'https://t.me/psp_ultra_bot'

    st.sidebar.markdown(f'''<a href={url}><button style="background-color:Red;">Click here to connect! Link will expire in 1 minute.</button></a>''', unsafe_allow_html=True)
    db_steamers_remote.set_telegram_button_pressed(username=st.session_state.email)
