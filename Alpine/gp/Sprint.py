import warnings
import fastf1
import joblib
import os.path as path
import os
from datetime import datetime, timedelta
import numpy as np
import Alpine.utils as utils
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px


fastf1.Cache.disabled()

# applying the template
utils.template
pio.templates.default = 'alpine'


def sprint_race(session):
    name = session.name
    td = timedelta(hours=3)
    if (session.date + td) < utils.time.get_time(session.event.Country, session.event.Location).replace(
            tzinfo=None):
        session.load()
        # Setting up laps DataFrame
        session.laps['LapTime (s)'] = session.laps.LapTime.dt.total_seconds()
        session.laps['AltTime'] = session.laps.Time.dt.total_seconds() - 3600
        _laps = session.laps
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
        _tel = tel
        # Live telemetry
        driver = session.results.loc[session.results.Position == 1, "Abbreviation"].iloc[0]
        for i in _laps['LapNumber'].unique():
            lap_data = _laps[_laps['LapNumber'] == i]
            _laps.loc[_laps['LapNumber'] == i, 'DeltaToFirst'] = lap_data['AltTime'] - lap_data.loc[
                lap_data['Driver'] == driver, 'AltTime'].iloc[0]
        # weather DataFrame
        session.weather_data['AltTime'] = session.weather_data.Time.dt.total_seconds() - 3600
        session.weather_data['AltTime'].loc[session.weather_data['AltTime'] < 0] = np.nan
        session.weather_data.dropna(axis=0, inplace=True)
        _weather = session.weather_data
        _results = session.results
        race_Date = utils.time.get_session_date(session)
        race = True
        return race, race_Date, name, _laps, _tel, _weather, _results
    else:
        race = False
        race_Date = utils.time.get_session_date(session)
        warnings.warn("The session is not done, the data is available 1h after the end of the session.",
                      Warning, stacklevel=2)
        return race, race_Date, name, "", "", "", "", ""



class Sprint:
    def __init__(self, year, event, format):
        sprint = fastf1.get_session(year, event, 4)
        dir = path.join("data", str(year) + " " + sprint.event.EventName)
        if not path.exists(dir):
            os.mkdir(dir)
        self.event_name = sprint.event.EventName
        self.event_date = sprint.event.EventDate
        file = path.join("data", str(year) + " " + sprint.event.EventName, f"{sprint.name}.z")
        if not path.exists(file):
            if format == "sprint_shootout":
                session = fastf1.get_session(year, event, 3)
                self.Q_name = session.name
                # Verifying if the session is done. We add 2h to the beginning of the session to be sure that the data is up
                # They are usually up 30min after the session (1h for fp)
                td = timedelta(hours=2)
                if (session.date + td) < utils.time.get_time(session.event.Country, session.event.Location).replace(
                        tzinfo=None):
                    session.load()
                    # create the dataframe to be saved with custom cols for easier plots def.
                    laps = session.laps
                    laps['LapTime (s)'] = laps.LapTime.dt.total_seconds()
                    laps['AltTime'] = laps.Time.dt.total_seconds() - 1100
                    threshold = 1.1
                    threshold_lap_time = laps.pick_fastest()['LapTime (s)'] * threshold
                    laps.loc[laps['LapTime (s)'] >= threshold_lap_time, 'LapTime (s)'] = np.nan
                    self._Q_laps = laps
                    # create the tel DataFrame with telemetry from the fastest lap of each driver in the session.
                    drivers = np.unique(laps.Driver)
                    tel = pd.DataFrame()
                    for i in drivers:
                        d_tel = laps.pick_driver(i).pick_fastest().get_car_data().add_distance()
                        d_tel['Driver'] = i
                        tel = pd.concat([tel, d_tel], ignore_index=True)
                    self._Q_tel = tel
                    # weather DataFrame
                    weather = session.weather_data
                    weather['AltTime'] = weather.Time.dt.total_seconds() - 1100
                    weather['AltTime'].loc[weather['AltTime'] < 0] = np.nan
                    weather.dropna(axis=0, inplace=True)
                    self._Q_weather = weather
                    self.Qualif = True
                    self.Qualif_Date = utils.time.get_session_date(session)
                else:
                    self.Qualif = False
                    self.Qualif_Date = utils.time.get_session_date(session)
                    warnings.warn("The session is not done, the data is available 1h after the end of the session.",
                                  Warning, stacklevel=2)
                    return
            else:
                self.Qualif = False
                self.Qualif_Date = "Never"
            # Sprint part
            self.race, self.race_Date, self.name, self._laps, self._tel, self._weather, self._results = sprint_race(sprint)
            if format == "sprint_shootout" or self.race:
                joblib.dump(self, file)
        else:
            sprint = joblib.load(file)
            if format == "sprint_shootout":
                self.Q_name = sprint.Q_name
                self._Q_laps = sprint._Q_laps
                self._Q_tel = sprint._Q_tel
                self._Q_weather = sprint._Q_weather
                self.Qualif = True
                self.Qualif_Date = sprint.Qualif_Date
            else:
                self.Qualif = False
                self.Qualif_Date = "Never"
            if not sprint.race and sprint.race_Date + timedelta(hours=3) < datetime.now():
                self.race, self.race_Date, self.name, self._laps, self._tel, self._weather, self._results = sprint_race(sprint)
                joblib.dump(self, file)
            elif not sprint.race:
                self.race, self.race_Date = sprint.race, sprint.race_Date
                warnings.warn("The session is not done, the data is available 1h after the end of the session.",
                              Warning, stacklevel=2)
            else:
                self.race = sprint.race
                self.race_Date = sprint.race_Date
                self.name = sprint.name
                self._laps = sprint._laps
                self._tel = sprint._tel
                self._weather = sprint._weather
                self._results = sprint._results

    @property
    def Q_laps(self):
        return self._Q_laps

    @property
    def Q_tel(self):
        return self._Q_tel

    @property
    def Q_weather(self):
        return self._Q_weather

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
        return self.Qualif, self.race, self.Qualif_Date, self.race_Date

    def delta_time(self, tel, ref_driver, comp_driver):
        def mini_pro(stream):
            # Ensure that all samples are interpolated
            dstream_start = stream[1] - stream[0]
            dstream_end = stream[-1] - stream[-2]
            return np.concatenate([[stream[0] - dstream_start], stream, [stream[-1] + dstream_end]])

        def make_delta(ref, comp):
            ltime = mini_pro(comp['Time'].dt.total_seconds().to_numpy())
            ldistance = mini_pro(comp['Distance'].to_numpy())
            lap_time = np.interp(ref['Distance'], ldistance, ltime)
            delta = lap_time - ref['Time'].dt.total_seconds()
            delta = pd.DataFrame(
                {"Delta": delta.reset_index(drop=True), "Distance": ref['Distance'].reset_index(drop=True),
                 "Driver": pd.unique(comp["Driver"])[0]})
            return delta

        ref = tel.loc[tel.Driver == ref_driver]
        if type(comp_driver) is str:
            comp = tel.loc[tel.Driver == comp_driver]
            return make_delta(ref, comp)
        elif type(comp_driver) is list:
            delta = pd.DataFrame()
            for i in comp_driver:
                comp = tel.loc[tel.Driver == i]
                delta = pd.concat([delta, make_delta(ref, comp)]).reset_index(drop=True)
            return delta

    def Q_lap_times(self):
        laps = self._Q_laps
        drivers = pd.unique(laps.Driver).tolist()
        colors = utils.driver_color(drivers)
        x = [0, 600, 1200, 1800, 2400, 3000, 3600]
        fig = px.line(laps, x="AltTime", y="LapTime (s)", color="Driver", color_discrete_sequence=colors,
                      markers=True, title=f"{self.event_name} {self.Q_name} Lap Time")
        fig.update_xaxes(
            tickvals=x,
            ticktext=[str(timedelta(seconds=t)) for t in x],
            title="Time"
        )
        fig = utils.logo(fig)
        return fig

    def Q_violin_st(self):
        laps = self._Q_laps
        teams = pd.unique(laps.Team).tolist()
        teams_colors = utils.team_color(teams)
        fig = px.violin(laps, x="Team", y="SpeedST", color="Team", color_discrete_sequence=teams_colors, box=True,
                        title=f"{self.event_name} {self.Q_name} Teams Speed Trap")
        fig = utils.logo(fig)
        return fig

    def Q_violin_lap(self):
        laps = self._Q_laps
        teams = pd.unique(laps.Team).tolist()
        teams_colors = utils.team_color(teams)
        fig = px.violin(laps, x="Team", y="LapTime (s)", color="Team", color_discrete_sequence=teams_colors,
                        box=True, title=f"{self.event_name} {self.Q_name} Teams Laps Time")
        fig = utils.logo(fig)
        return fig

    def Q_top_speed(self):
        laps = self._Q_laps
        top_speeds = laps.groupby("Team")["SpeedST"].max()
        teams = pd.unique(top_speeds.index).tolist()
        teams_colors = utils.team_color(teams)
        fig = px.scatter(top_speeds, x=top_speeds.index, y="SpeedST", color=top_speeds.index,
                         color_discrete_sequence=teams_colors, title=f"{self.event_name} {self.Q_name} Team Top Speed")
        fig = utils.logo(fig)
        return fig

    def Q_lap_comp(self, comp_driver=None):
        tel = self._Q_tel
        if not comp_driver:
            laps = self._Q_laps
            lap = laps.loc[laps['LapTime (s)'].idxmin()]
            if isinstance(lap, pd.DataFrame):
                # More laps, same time
                lap = lap.iloc[0]
            comp_driver = lap.Driver
        tel['Time'] = pd.to_timedelta(tel['Time'])
        sel_drivers = []
        if len(sel_drivers) == 0:
            sel_drivers = pd.unique(tel.Driver).tolist()
        dt = tel[tel['Driver'].isin(sel_drivers)]
        delta = self.delta_time(tel, comp_driver, sel_drivers)
        drivers = pd.unique(delta.Driver).tolist()
        colors = utils.driver_color(drivers)
        fig = make_subplots(rows=7, cols=1, shared_xaxes=True)
        # TODO : ajouter les titres au plot et aux axes y
        for i, driver in enumerate(drivers):
            delta_driver = delta[delta['Driver'] == driver]
            dt_driver = dt[dt['Driver'] == driver]
            fig.add_trace(
                go.Scatter(x=delta_driver["Distance"], y=delta_driver["Delta"], legendgroup=driver, name=driver,
                           mode="lines", line=dict(color=colors[i])), row=1, col=1)
            fig.add_trace(
                go.Scatter(x=dt_driver["Distance"], y=dt_driver["Speed"], legendgroup=driver, name=driver, mode="lines",
                           line=dict(color=colors[i]), showlegend=False), row=2, col=1)
            fig.add_trace(
                go.Scatter(x=dt_driver["Distance"], y=dt_driver["Brake"], legendgroup=driver, name=driver, mode="lines",
                           line=dict(color=colors[i]), showlegend=False), row=3, col=1)
            fig.add_trace(
                go.Scatter(x=dt_driver["Distance"], y=dt_driver["DRS"], legendgroup=driver, name=driver, mode="lines",
                           line=dict(color=colors[i]), showlegend=False), row=4, col=1)
            fig.add_trace(
                go.Scatter(x=dt_driver["Distance"], y=dt_driver["nGear"], legendgroup=driver, name=driver, mode="lines",
                           line=dict(color=colors[i]), showlegend=False), row=5, col=1)
            fig.add_trace(go.Scatter(x=dt_driver["Distance"], y=dt_driver["Throttle"], legendgroup=driver, name=driver,
                                     mode="lines", line=dict(color=colors[i]), showlegend=False), row=6, col=1)
            fig.add_trace(
                go.Scatter(x=dt_driver["Distance"], y=dt_driver["RPM"], legendgroup=driver, name=driver, mode="lines",
                           line=dict(color=colors[i]), showlegend=False), row=7, col=1)
        fig.update_yaxes(title_text=f"Delta to {comp_driver}", row=1, col=1)
        fig.update_yaxes(title_text="Speed (km/h)", row=2, col=1)
        fig.update_yaxes(title_text="Brake", row=3, col=1)
        fig.update_yaxes(title_text="DRS", row=4, col=1)
        fig.update_yaxes(title_text="Gear", row=5, col=1)
        fig.update_yaxes(title_text="Throttle", row=6, col=1)
        fig.update_yaxes(title_text="RPM", row=7, col=1)
        fig.update_xaxes(title_text="Distance (km)", row=7, col=1)
        fig.update_layout(height=1200, title=f"{self.event_name} {self.Q_name} Fastest Lap Comparison")
        fig = utils.logo(fig, 7)
        return fig

    def delta_to_first(self):
        laps = self._laps[self._laps['FastF1Generated'] != True]
        drivers = pd.unique(laps.Driver).tolist()
        driver_colors = utils.driver_color(drivers)
        fig = px.line(laps, x="LapNumber", y="DeltaToFirst", color="Driver", color_discrete_sequence=driver_colors, title=f"{self.event_name} Sprint Gap to Winner")
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
                      markers=True, title=f"{self.event_name} Sprint Lap Time")
        fig = utils.logo(fig)
        return fig

    def violin_st(self):
        laps = self._laps
        teams = pd.unique(laps.Team).tolist()
        teams_colors = utils.team_color(teams)
        fig = px.violin(laps, x="Team", y="SpeedST", color="Team", color_discrete_sequence=teams_colors, box=True,
                        title=f"{self.event_name} Sprint Teams Speed Trap")
        fig = utils.logo(fig)
        return fig

    def violin_lap(self):
        laps = self._laps
        teams = pd.unique(laps.Team).tolist()
        teams_colors = utils.team_color(teams)
        fig = px.violin(laps, x="Team", y="LapTime (s)", color="Team", color_discrete_sequence=teams_colors,
                        box=True, title=f"{self.event_name} Sprint Teams Laps Time")
        fig = utils.logo(fig)
        return fig

    def top_speed(self):
        laps = self._laps
        top_speeds = laps.groupby("Team")["SpeedST"].max()
        teams = pd.unique(top_speeds.index).tolist()
        teams_colors = utils.team_color(teams)
        fig = px.scatter(top_speeds, x=top_speeds.index, y="SpeedST", color=top_speeds.index,
                         color_discrete_sequence=teams_colors, title=f"{self.event_name} Sprint Teams Top Speed")
        fig = utils.logo(fig)
        return fig