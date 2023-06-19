import fastf1
import os.path as path
import os
import pandas as pd

fastf1.Cache.set_disabled()

dates = pd.read_csv(path.join("data", "dates.csv"))

for index, row in dates.iterrows():
    if row["Year"] == 2023 and row["Round"] > 8:
        break
    session = fastf1.get_session(row["Year"], row["Round"], 4)
    session.load(laps=False, telemetry=False, weather=False, messages=False, livedata=False)
    dir = path.join("data", str(row["Year"]) + " " + session.event.EventName)
    if not path.exists(dir):
        os.mkdir(dir)
    session.results.to_csv(path.join("data", str(row["Year"]) + " " + session.event.EventName, "Qualifying-result.csv"))
    print(str(row["Year"]) + " " + session.event.EventName)