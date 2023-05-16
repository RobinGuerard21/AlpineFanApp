import joblib
import pandas as pd
import os.path as path
import random
import plotly.express as px
from sklearn.preprocessing import OneHotEncoder
import Alpine.utils as utils
import plotly.io as pio

def predict(event):
    regression = joblib.load(path.join("data", "strat", 'grid_test.pkl'))
    tyres = pd.read_csv(path.join("data", "strat", "tyres.csv"))
    tracks = pd.read_csv(path.join("data", "strat", "track.csv"))
    tyre = tyres.loc[tyres.Name == event]

    if tyre.Circuits.iloc[0] == None:
        return False, ""

    utils.template
    pio.templates.default = 'alpine'
    length = tracks.loc[tracks.Name == event, "Length"]
    laps = []
    for i in range(80):
        j = i * length
        laps.append(j)

    liste = ['Soft', 'Medium', 'Hard']
    encoder = OneHotEncoder()
    valeur_aleatoire = random.choice(liste)
    data = pd.DataFrame({"Distance": laps, "Team": "Alpine", "Compound": tyre[valeur_aleatoire].iloc[0],
                         "Track": tyre["Circuits"].iloc[0]})
    X_test = pd.DataFrame(columns=regression["columns"])
    Xf = data[['Distance']]
    encodedf = encoder.fit_transform(data[['Team', 'Compound', 'Track']])
    Xf = pd.concat([Xf, pd.DataFrame(data=encodedf.toarray(), columns=encoder.get_feature_names_out())], axis=1)
    X_test = pd.concat([X_test, Xf])
    X_test.fillna(0, inplace=True)
    T_pred = regression["model"].predict(X_test)
    X_test = pd.concat([X_test, pd.DataFrame({"Predict": T_pred})], axis=1)
    X_test['LapNb'] = X_test.index
    fig = px.line(X_test, x="LapNb", y="Predict",
                  title=f"{event} Alpine {valeur_aleatoire}({tyre[valeur_aleatoire].iloc[0]}) Prediction")
    fig.update_layout(
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (second)",
    )
    return True, fig