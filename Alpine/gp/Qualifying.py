import fastf1
import numpy as np
import os
import os.path as path
from datetime import datetime, timedelta
import logging
import pandas as pd
import Alpine.utils as utils
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


fastf1.Cache.set_disabled()

# applying the template
utils.template


class Qualifying:
    def __init__(self, year, event):
        # Creates the Free Practice object
        session = fastf1.get_session(year, event, "Q")
        dir = path.join("data", str(year) + " " + session.event.EventName)
        if not path.exists(dir):
            os.mkdir(dir)
        self.name = session.name
        self.event_name = session.event.EventName
        self.event_date = session.event.EventDate
        laps_file = path.join("data", str(year) + " " + session.event.EventName, f"{session.name}-laps.csv")
        if not path.exists(laps_file):

            # Verifying if the session is done. We add 2h to the beginning of the session to be sure that the data is up
            # They are usually up 30min after the session (1h for fp)
            td = timedelta(hours=2)
            if (session.date + td) < utils.time.userToGmt().replace(tzinfo=None):
                session.load()
                # create the dataframe to be saved with custom cols for easier plots def.
                laps = session.laps
                laps['LapTime (s)'] = laps.LapTime.dt.total_seconds()
                laps['AltTime'] = laps.Time.dt.total_seconds() - 1100
                threshold = 1.1
                threshold_lap_time = laps.pick_fastest()['LapTime (s)'] * threshold
                laps.loc[laps['LapTime (s)'] >= threshold_lap_time, 'LapTime (s)'] = np.nan
                laps.to_csv(laps_file, index=False)
                # create the tel DataFrame with telemetry from the fastest lap of each driver in the session.
                drivers = np.unique(laps.Driver)
                tel = pd.DataFrame()
                for i in drivers:
                    try:
                        d_tel = laps.pick_driver(i).pick_fastest().get_car_data().add_distance()
                        d_tel['Driver'] = i
                        tel = pd.concat([tel, d_tel], ignore_index=True)
                    except:
                        utils.error(
                            f"Could not get telemetry for driver {i} at {session.name} event {session.event.EventName} {year}")
                tel_file = path.join("data", str(year) + " " + session.event.EventName, f"{session.name}-tel.csv")
                tel.to_csv(tel_file, index=False)
                # results
                results = session.results
                results_file = path.join("data", str(year) + " " + session.event.EventName, f"{session.name}-results.csv")
                results.to_csv(results_file, index=False)
                # weather DataFrame
                weather = session.weather_data
                weather['AltTime'] = weather.Time.dt.total_seconds() - 900
                weather['AltTime'].loc[weather['AltTime'] < 0] = np.nan
                weather.dropna(axis=0, inplace=True)
                weather_file = path.join("data", str(year) + " " + session.event.EventName, f"{session.name}-weather.csv")
                weather.to_csv(weather_file, index=False)
            else:
                self.Qualif = False
                self.Qualif_Date = utils.time.get_session_date(session.date)
                logging.info('The session is not done, the data is available 1h after the end of the session.')
                return
        self.Qualif = True
        self.Qualif_Date = utils.time.get_session_date(session.date)
        self._laps = pd.read_csv(laps_file)
        tel_file = path.join("data", str(year) + " " + session.event.EventName, f"{session.name}-tel.csv")
        self._tel = pd.read_csv(tel_file)
        results_file = path.join("data", str(year) + " " + session.event.EventName, f"{session.name}-results.csv")
        self._results = pd.read_csv(results_file)
        weather_file = path.join("data", str(year) + " " + session.event.EventName, f"{session.name}-weather.csv")
        self._weather = pd.read_csv(weather_file)

    @property
    def laps(self):
        return self._laps

    @property
    def tel(self):
        return self._tel

    @property
    def results(self):
        return self._results

    @property
    def weather(self):
        return self._weather

    @property
    def get_load(self):
        return self.Qualif, self.Qualif_Date

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

    def lap_times(self):
        laps = self._laps
        drivers = pd.unique(laps.Driver).tolist()
        colors = utils.driver_color(drivers)
        x = [0, 600, 1200, 1800, 2400, 3000, 3600]
        fig = px.line(laps, x="AltTime", y="LapTime (s)", color="Driver", color_discrete_sequence=colors,
                      markers=True, title=f"{self.event_name} {self.name} Lap Time")
        fig.update_xaxes(
            tickvals=x,
            ticktext=[str(timedelta(seconds=t)) for t in x],
            title="Time"
        )
        fig = utils.logo(fig)
        return fig

    def violin_st(self):
        laps = self._laps
        teams = pd.unique(laps.Team).tolist()
        teams_colors = utils.team_color(teams)
        fig = px.violin(laps, x="Team", y="SpeedST", color="Team", color_discrete_sequence=teams_colors, box=True,
                        title=f"{self.event_name} {self.name} Teams Speed Trap")
        fig = utils.logo(fig)
        return fig

    def violin_lap(self):
        laps = self._laps
        teams = pd.unique(laps.Team).tolist()
        teams_colors = utils.team_color(teams)
        fig = px.violin(laps, x="Team", y="LapTime (s)", color="Team", color_discrete_sequence=teams_colors,
                        box=True, title=f"{self.event_name} {self.name} Teams Laps Time")
        fig = utils.logo(fig)
        return fig

    def top_speed(self):
        laps = self._laps
        top_speeds = laps.groupby("Team")["SpeedST"].max()
        teams = pd.unique(top_speeds.index).tolist()
        teams_colors = utils.team_color(teams)
        fig = px.scatter(top_speeds, x=top_speeds.index, y="SpeedST", color=top_speeds.index,
                         color_discrete_sequence=teams_colors, title=f"{self.event_name} {self.name} Team Top Speed")
        fig = utils.logo(fig)
        return fig

    def lap_comp(self, comp_driver=None):
        tel = self._tel
        if not comp_driver:
            laps = self._laps
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
        fig.update_layout(height=1200, title=f"{self.event_name} {self.name} Fastest Lap Comparison")
        fig = utils.logo(fig, 7)
        return fig