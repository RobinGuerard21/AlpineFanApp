import os.path

import fastf1
import fastf1.plotting as plot
import pandas as pd

fastf1.Cache.enable_cache('Cache')

year = 2022

tyres = pd.read_csv("tyres.csv")

track = pd.read_csv("track.csv")

for circuit in tyres.Circuits:
    if circuit != "Monza":
        t_hard = tyres[tyres['Circuits'] == circuit]["Hard"].values[0]
        t_medium = tyres[tyres['Circuits'] == circuit]["Medium"].values[0]
        t_soft = tyres[tyres['Circuits'] == circuit]["Soft"].values[0]

        fp1 = fastf1.get_session(year, circuit, 'FP1')
        fp1.load(laps=True, telemetry=True, weather=False)
        fp2 = fastf1.get_session(year, circuit, 'FP2')
        fp2.load(laps=True, telemetry=True, weather=False)
        fp3 = fastf1.get_session(year, circuit, tyres[tyres['Circuits'] == circuit]["Sprint"].values[0])
        fp3.load(laps=True, telemetry=True, weather=False)
        race = fastf1.get_session(year, circuit, 'R')
        race.load(laps=True, telemetry=True, weather=False)

        length = track[track['Circuits'] == circuit]['Length'].values[0]

        dt = pd.concat([fp1.laps.pick_accurate().pick_quicklaps(),
                        fp2.laps.pick_accurate().pick_quicklaps(),
                        fp3.laps.pick_accurate().pick_quicklaps(),
                        race.laps.pick_accurate()])

        dt.replace("SOFT", t_soft, inplace=True)
        dt.replace("MEDIUM", t_medium, inplace=True)
        dt.replace("HARD", t_hard, inplace=True)

        dt["Second"] = dt.LapTime.dt.total_seconds()
        dt["TyreDistance"] = dt["TyreLife"] * length

        tyresLife = pd.DataFrame({"Distance": dt['TyreDistance'].reset_index(drop=True),
                                  "Time": dt['Second'].reset_index(drop=True),
                                  "Team": dt['Team'].reset_index(drop=True),
                                  "Compound": dt['Compound'].reset_index(drop=True),
                                  "Track": circuit})

        if os.path.exists("Data/tyrelife.csv"):
            print(tyresLife)
            tyresLife = pd.concat([tyresLife, pd.read_csv(f"Data/tyrelife.csv")]).sort_values(by="Distance")

        tyresLife.to_csv(f"Data/tyrelife.csv", index=False)