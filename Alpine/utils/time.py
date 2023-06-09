from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import pandas as pd
import os.path as path
import fastf1

fastf1.Cache.set_disabled()


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

def gmtToUser(time):
    gmt_timestamp = datetime(time.year, time.month, time.day, time.hour, time.minute, time.second, tzinfo=pytz.timezone('GMT'))
    paris_timezone = pytz.timezone('Europe/Paris')

    return gmt_timestamp.astimezone(paris_timezone)

def userToGmt():
    utc_now = datetime.now(pytz.utc)
    gmt_timezone = pytz.timezone('GMT')

    return utc_now.astimezone(gmt_timezone)


def get_session_date(date):
    paris_ts = gmtToUser(date)
    day_of_week = paris_ts.strftime('%A')
    date = paris_ts.strftime('%d %B %Y')
    time = paris_ts.strftime('%H:%M')

    return f"The session will take place {day_of_week} {date} at {time} Paris Time"

def get_latest():
    now = datetime.now()
    dt = pd.read_csv("data/dates.csv")
    dt['Date'] = pd.to_datetime(dt['Date'])
    dt = dt.loc[dt.Date <= now].sort_values('Date', ascending=False)
    session = fastf1.get_session(dt.Year.iloc[0], dt.Round.iloc[0], "R")
    td = timedelta(hours=3)
    if (session.date + td) < userToGmt().replace(tzinfo=None):
        return f"/grand-prix/{dt.Year.iloc[0]}/{dt.Round.iloc[0]}/race"
    else:
        return f"/grand-prix/{dt.Year.iloc[1]}/{dt.Round.iloc[1]}/race"
