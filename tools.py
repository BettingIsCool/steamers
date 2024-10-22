import re
import pytz
import flag
import emoji
import base64
import db_pinnacle
import streamlit as st
from zoneinfo import ZoneInfo
from datetime import datetime

from config_local import SIDES


def extract_selection(market: str, event: dict, index: int):
    """
    Extracts the selection from the given market, event, and index.

    :param market: The market identifier.
    :param event: The event dictionary containing runner information.
    :param index: The index of the runner in the market.
    :return: The uppercase representation of the selected runner.

    """
    if SIDES[market][index] == 'home':
        return event['runner_home']
    elif SIDES[market][index] == 'away':
        return event['runner_away']
    else:
        return SIDES[market][index]


def get_country_code(league_id: int):
    """
    :param league_id: The unique identifier for a sports league.
    :return: The country code associated with the given league_id. Returns an empty string if retrieval fails.
    """
    try:
        cc = flag.flag(countrycode=db_pinnacle.get_country_code(league_id=league_id))
    except Exception as ex:
        print(ex, f"Couldn't get country code for league_id {league_id}")
        cc = ''
    return cc


def epoch_to_local_datetime(epoch_time: int):
    """
    :param epoch_time: The epoch timestamp to be converted, expressed as an integer.
    :return: The local datetime corresponding to the epoch timestamp, adjusted to the "Europe/Vienna" timezone.
    """
    utc_time = datetime.utcfromtimestamp(epoch_time)

    # Get the current local timezone
    try:
        local_tz = ZoneInfo(key="Europe/Vienna")
    except ImportError:
        # Fallback for Python versions that don't have zoneinfo
        local_tz = pytz.utc.localize(utc_time).astimezone().tzinfo

    # Convert UTC datetime to local time
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz)

    return local_time


def extract_pinnacle_event_id(url: str):
    """
    :param url: A string representing the URL which potentially contains a Pinnacle event ID.
    :return: A string containing the 10-digit Pinnacle event ID if found, otherwise None.
    """
    # Regular expression pattern for matching 10 consecutive digits
    pattern = r'\b\d{10}\b'

    # Search for the pattern in the text
    match = re.search(pattern, url)

    # If a match is found, return it; otherwise, return None
    return match.group() if match else None


def compose_alert_message(sport: dict, country_code: str, market: str, selection: str, previous_odds: float, previous_odds_american: int, verified_odds: float, current_odds_american: int, verified_drop_pct: float, true_odds: float, odds_to_beat_american: int, ten_val_american: int, max_win: float, event: dict, line: (float, None)):
    """

    Compose Alert Message

    This method takes in several parameters and returns a formatted alert message string.

    Parameters:
    - sport: A dictionary representing the sport information.
    - country_code: A string representing the country code.
    - selection: A string representing the current selection.
    - previous_odds: A float representing the previous odds.
    - previous_odds_american: An integer representing the previous odds in American format.
    - verified_odds: A float representing the current verified odds.
    - current_odds_american: An integer representing the current verified odds in American format.
    - verified_drop_pct: A float representing the percentage of drop from previous odds to verified odds.
    - true_odds: A float representing the true odds.
    - odds_to_beat_american: An integer representing the odds to beat in American format.
    - ten_val_american: An integer representing the 10%-value in American format.
    - max_win: A float representing the maximum possible win.
    - event: A dictionary representing the event information.

    Returns:
    - A string containing the formatted alert message.

    Example Usage:
    sport = {'emoji': ':soccer:', 'name': 'Football'}
    country_code = 'US'
    selection = 'Real Madrid'
    previous_odds = 2.0
    previous_odds_american = -200
    verified_odds = 1.8
    current_odds_american = -125
    verified_drop_pct = 10.0
    true_odds = 1.5
    odds_to_beat_american = +200
    ten_val_american = +220
    max_win = 1000.0
    event = {'runner_home': 'Real Madrid', 'runner_away': 'Barcelona', 'league_name': 'La Liga', 'starts': datetime.datetime(2021, 10, 10, 12, 0)}

    alert_message = compose_alert_message(sport, country_code, selection, previous_odds, previous_odds_american, verified_odds, current_odds_american, verified_drop_pct, true_odds, odds
    *_to_beat_american, ten_val_american, max_win, event)
    print(alert_message)

    """
    text = f"{emoji.emojize(sport['emoji'])} {emoji.emojize(sport['name'].upper())} ({market.upper()}) {country_code}\n\n"
    if line is not None:
        if market == 'spread':
            if line != 0:
                text += f"*{selection.upper()} {line:+g}*\n"
            else:
                text += f"*{selection.upper()} 0*\n"
        else:
            text += f"*{selection.upper()} {line:g}*\n"
    else:
        text += f"*{selection.upper()}*\n"
    text += f"{previous_odds} ({previous_odds_american:+g}) >>> {verified_odds} ({current_odds_american:+g}) \\[{round(100 * verified_drop_pct, 2)}%]\n"
    text += f"Odds to beat: {round(true_odds, 3)} ({odds_to_beat_american:+g})\n"
    text += f"10%-value: *{round(1.1 * true_odds, 3)} ({ten_val_american:+g})*\n"
    text += f"Limit: USD {int(2 * max_win)}\n\n"
    text += f"{event['runner_home']} v {event['runner_away']}\n"
    text += f"{event['league_name']}\n"
    text += f"{event['starts'].strftime('%a %-d-%b %-H:%M')} GMT+1\n"

    return text


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
