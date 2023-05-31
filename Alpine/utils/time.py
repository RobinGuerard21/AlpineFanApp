from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import pandas as pd
import os.path as path


def get_timezone_old(country, loc):
    geolocator = Nominatim(user_agent="Alpine")

    location = geolocator.geocode(f"{loc}, {country}")

    tf = TimezoneFinder()
    latitude, longitude = location.latitude, location.longitude
    return pytz.timezone(tf.timezone_at(lng=longitude, lat=latitude))

def get_timezone(event, year):
    gp_data = pd.read_csv(path.join("data", "dates.csv"))
    chosen_gp = gp_data.loc[(gp_data['Year'] == year) & (gp_data["Round"] == event)]
    tf = TimezoneFinder()
    latitude, longitude = float(chosen_gp.Lat), float(chosen_gp.Long)
    return pytz.timezone(tf.timezone_at(lng=longitude, lat=latitude))


def get_time(event, year):
    return datetime.now(get_timezone(event, year))


def get_session_date(session, event, year):
    ts = pd.Timestamp(session.date, tz=get_timezone(event, year))
    user_tz = pytz.timezone('Europe/Paris')
    local_ts = ts.tz_convert(user_tz)
    day_of_week = local_ts.strftime('%A')
    date = local_ts.strftime('%d %B %Y')
    time = local_ts.strftime('%H:%M')

    return f"The session will take place {day_of_week} {date} at {time} Paris Time"