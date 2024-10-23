import base64
import streamlit as st


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
