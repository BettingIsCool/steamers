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
