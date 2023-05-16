from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import pandas as pd


def get_timezone(country, loc):
    geolocator = Nominatim(user_agent="Alpine")

    location = geolocator.geocode(f"{loc}, {country}")

    tf = TimezoneFinder()
    latitude, longitude = location.latitude, location.longitude
    return pytz.timezone(tf.timezone_at(lng=longitude, lat=latitude))


def get_time(country, loc):
    return datetime.now(get_timezone(country, loc))


def get_session_date(session):
    ts = pd.Timestamp(session.date, tz=get_timezone(session.event.Country, session.event.Location))
    user_tz = pytz.timezone('Europe/Paris')
    local_ts = ts.tz_convert(user_tz)
    day_of_week = local_ts.strftime('%A')
    date = local_ts.strftime('%d %B %Y')
    time = local_ts.strftime('%H:%M')

    return f"The session will take place {day_of_week} {date} at {time} Paris Time"