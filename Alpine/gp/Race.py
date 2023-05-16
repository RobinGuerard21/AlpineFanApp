import warnings
import fastf1
import joblib
import os.path as path
import os
from datetime import datetime, timedelta
import numpy as np
import Alpine.utils as utils
import pandas as pd
import plotly.express as px

utils.template

fastf1.Cache.disabled()

class Race:
    def __init__(self, year, event):
        session = fastf1.get_session(year, event, "R")
        dir = path.join("data", str(year) + " " + session.event.EventName)
        if not path.exists(dir):
            os.mkdir(dir)
        self.name = session.name
        self.event_name = session.event.EventName
        self.event_date = session.event.EventDate
        file = path.join("data", str(year) + " " + session.event.EventName, f"{session.name}.z")
        if not path.exists(file):
            td = timedelta(hours=3)
            if (session.date + td) < utils.time.get_time(session.event.Country, session.event.Location).replace(
                    tzinfo=None):
                session.load()
                # Setting up laps DataFrame
                session.laps['LapTime (s)'] = session.laps.LapTime.dt.total_seconds()
                session.laps['AltTime'] = session.laps.Time.dt.total_seconds() - 3600
                self._laps = session.laps
                # Setting up tel DataFrame
                drivers = np.unique(session.laps.Driver)
                tel = pd.DataFrame()
                for driver in drivers:
                    laps = list(session.laps.pick_driver(driver)['LapNumber'])
                    for lap_nb in laps:
                        lap = session.laps.pick_driver(driver).loc[session.laps['LapNumber'] == lap_nb].iloc[0]
                        dtel = session.laps.pick_driver(driver).get_car_data().add_distance().slice_by_lap(lap)
                        dtel['LapNumber'] = lap_nb
                        dtel['Driver'] = driver
                        tel = pd.concat([tel, dtel], ignore_index=True)
                self._tel = tel
                # Live telemetry
                driver = session.results.loc[session.results.Position == 1, "Abbreviation"].iloc[0]
                for i in self._laps['LapNumber'].unique():
                    lap_data = self._laps[self._laps['LapNumber'] == i]
                    self._laps.loc[self._laps['LapNumber'] == i, 'DeltaToFirst'] = lap_data['AltTime'] - lap_data.loc[
                        lap_data['Driver'] == driver, 'AltTime'].iloc[0]
                # weather DataFrame
                session.weather_data['AltTime'] = session.weather_data.Time.dt.total_seconds() - 3600
                session.weather_data['AltTime'].loc[session.weather_data['AltTime'] < 0] = np.nan
                session.weather_data.dropna(axis=0, inplace=True)
                self._weather = session.weather_data
                self._results = session.results
                self.race_Date = utils.time.get_session_date(session)
                self.race = True
                joblib.dump(self, file)
            else:
                self.race = False
                self.race_Date = utils.time.get_session_date(session)
                warnings.warn("The session is not done, the data is available 1h after the end of the session.",
                              Warning, stacklevel=2)
                return
        else:
            race = joblib.load(file)
            self._laps = race._laps
            self._tel = race._tel
            self.race_Date = utils.time.get_session_date(session)
            self._weather = race._weather
            self._results = race._results
            self.race = True
        return

    @property
    def laps(self):
        return self._laps

    @property
    def tel(self):
        return self._tel

    @property
    def weather(self):
        return self._weather

    @property
    def results(self):
        return self._results

    @property
    def get_load(self):
        return self.race, self.race_Date

    def delta_to_first(self):
        laps = self._laps[self._laps['FastF1Generated'] != True]
        drivers = pd.unique(laps.Driver).tolist()
        driver_colors = utils.driver_color(drivers)
        fig = px.line(laps, x="LapNumber", y="DeltaToFirst", color="Driver", color_discrete_sequence=driver_colors, title=f"{self.event_name} Race Gap to Winner")
        fig = utils.logo(fig)
        fig.update_layout(
            yaxis=dict(
                autorange="reversed"
            )
        )
        return fig

    def lap_times(self):
        laps = self._laps
        drivers = pd.unique(laps.Driver).tolist()
        colors = utils.driver_color(drivers)
        x = [0, 600, 1200, 1800, 2400, 3000, 3600]
        fig = px.line(laps, x="LapNumber", y="LapTime (s)", color="Driver", color_discrete_sequence=colors,
                      markers=True, title=f"{self.event_name} Race Lap Time")
        fig = utils.logo(fig)
        return fig

    def violin_st(self):
        laps = self._laps
        teams = pd.unique(laps.Team).tolist()
        teams_colors = utils.team_color(teams)
        fig = px.violin(laps, x="Team", y="SpeedST", color="Team", color_discrete_sequence=teams_colors, box=True,
                        title=f"{self.event_name} Race Teams Speed Trap")
        fig = utils.logo(fig)
        return fig

    def violin_lap(self):
        laps = self._laps
        teams = pd.unique(laps.Team).tolist()
        teams_colors = utils.team_color(teams)
        fig = px.violin(laps, x="Team", y="LapTime (s)", color="Team", color_discrete_sequence=teams_colors,
                        box=True, title=f"{self.event_name} Race Teams Laps Time")
        fig = utils.logo(fig)
        return fig

    def top_speed(self):
        laps = self._laps
        top_speeds = laps.groupby("Team")["SpeedST"].max()
        teams = pd.unique(top_speeds.index).tolist()
        teams_colors = utils.team_color(teams)
        fig = px.scatter(top_speeds, x=top_speeds.index, y="SpeedST", color=top_speeds.index,
                         color_discrete_sequence=teams_colors, title=f"{self.event_name} Race Teams Top Speed")
        fig = utils.logo(fig)
        return fig