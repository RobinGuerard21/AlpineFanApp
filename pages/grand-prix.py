import dash
from dash import html, dcc
import pandas as pd
from datetime import datetime
import Alpine.gp as f1
import os.path as path
import plotly.express as px
import numpy as np
import Alpine.strat as strat
import Alpine.utils as utils
import json

dash.register_page(__name__, path="/grand-prix", path_template="/grand-prix/<year>/<event>/<session>",
                   title="Alpine Fan F1 Dashboard | Grand Prix",
                   description="Get all Formula 1's data on any Grand Prix since 2018. Choose your year, your event and the session then have Fun !",
                   image_url="https://alpinefan.robcorp.net/assets/images/logo.png")


# Setting up the dataframe
def get_dataframe():
    gp_data = pd.read_csv(path.join("data", "dates.csv"))
    gp_data['Date'] = pd.to_datetime(gp_data['Date'])
    today = datetime.today()
    gp_data['Race_Status'] = np.where(gp_data['Date'] < today, 'Past', 'Future')
    color_map = {'Past': '#2ecc71', 'Future': '#e74c3c'}
    gp_data['Color'] = gp_data['Race_Status'].map(color_map)
    return gp_data


def make_map(filtered_data):
    map_fig = px.scatter_geo(filtered_data, lat='Lat', lon='Long', hover_name='Name', hover_data=["Year", "Round"],
                             color="Color", color_discrete_sequence=list(pd.unique(filtered_data['Color'])))
    map_fig.update_geos(bgcolor="#2c3e50", showcountries=True, countrycolor="#ecf0f1",
                        showcoastlines=True, coastlinecolor="#ecf0f1", showframe=False)
    map_fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        dragmode=False
    )
    map_fig.update_traces(marker_size=10)
    return map_fig


def race_result(content, results):
    classement = []
    d_color = html.Div(className="color")
    change = html.Div(className="evolution")
    d_pos = html.Div(className="pos", children="Pos")
    d_num = html.Div(className="num", children="N°")
    d_name = html.Div(className="name", children="Driver")
    d_team = html.Div(className="team", children="Team")
    d_time = html.Div(className="time", children=f"Time")
    d_pts = html.Div(className="pts", children="Pts")
    classement.append(
        html.Div(className="driver row",
                 children=[html.Div(className="flex", children=[d_color, change, d_pos]), d_num, d_name, d_team, d_time,
                           d_pts])
    )
    for index, row in results.iterrows():
        d_color = html.Div(className="color", style={"background-color": f"#{row['TeamColor']}"})
        if (row['Position'] - row['GridPosition']) < 0:
            change = html.Img(className="evolution", src="/assets/images/grow.svg")
        elif (row['Position'] - row['GridPosition']) == 0:
            change = html.Img(className="evolution", src="/assets/images/stable.svg")
        elif (row['Position'] - row['GridPosition']) > 0:
            change = html.Img(className="evolution", src="/assets/images/decrease.svg")
        d_pos = html.Div(className="pos", children=row['ClassifiedPosition'])
        d_num = html.Div(className="num", children=row['DriverNumber'])
        d_name = html.Div(className="name", children=row['FullName'])
        d_team = html.Div(className="team", children=row['TeamName'])
        if row['Position'] == 1:
            d_time = html.Div(className="time",
                              children=f"{row['Time'].seconds // 3600:02d}:{(row['Time'].seconds // 60) % 60:02d}:{row['Time'].seconds % 60:02d}.{int(row['Time'].total_seconds() * 1000) % 1000:03d}")
        elif pd.isnull(row.Time):
            d_time = html.Div(className="time", children=row['Status'])
        else:
            d_time = html.Div(className="time",
                              children=f"{row['Time'].total_seconds():.3f}s")
        d_pts = html.Div(className="pts", children=row['Points'])
        if row['Position'] < 4:
            cl = "driver"
        else:
            cl = "driver full"
        classement.append(
            html.Div(className=cl,
                     children=[html.Div(className="flex", children=[d_color, change, d_pos]), d_num, d_name, d_team,
                               d_time,
                               d_pts])
        )
    more = html.Img(id="more-race", src="/assets/images/more.svg")
    content.append(html.Div(className="race", children=[html.Div(className="title", children="Race Results"),
                                                        html.Div(id="race-results", children=classement), more]))
    return content


def qualy_result(content, results):
    classement = []
    d_color = html.Div(className="color")
    d_pos = html.Div(className="pos", children="Pos")
    d_num = html.Div(className="num", children="N°")
    d_name = html.Div(className="name", children="Driver")
    d_team = html.Div(className="team", children="Team")
    d_time = html.Div(className="time", children="Q1")
    d_time2 = html.Div(className="time", children="Q2")
    d_time3 = html.Div(className="time", children="Q3")
    classement.append(
        html.Div(className="driver row",
                 children=[html.Div(className="flex", children=[d_color, d_pos]), d_num, d_name, d_team, d_time,
                           d_time2, d_time3])
    )

    results.Q1 = pd.to_timedelta(results.Q1)
    results.Q2 = pd.to_timedelta(results.Q2)
    results.Q3 = pd.to_timedelta(results.Q3)

    def Q_time(time, results_time):
        if not pd.isnull(time):
            if time == results_time.min():
                classname = "time min"
            else:
                classname = "time"
            d_time = html.Div(className=classname,
                              children=f"{(time.seconds // 60) % 60:02d}:{time.seconds % 60:02d}.{int(time.total_seconds() * 1000) % 1000:03d}")
        else:
            d_time = html.Div(className="time", children="-")
        return d_time

    for index, row in results.iterrows():
        d_color = html.Div(className="color", style={"background-color": f"#{row['TeamColor']}"})
        d_pos = html.Div(className="pos", children=row['Position'])
        d_num = html.Div(className="num", children=row['DriverNumber'])
        d_name = html.Div(className="name", children=row['FullName'])
        d_team = html.Div(className="team", children=row['TeamName'])
        d_time = Q_time(row.Q1, results.Q1)
        d_time2 = Q_time(row.Q2, results.Q2)
        d_time3 = Q_time(row.Q3, results.Q3)
        if row['Position'] < 4:
            cl = "driver"
        else:
            cl = "driver full"
        classement.append(
            html.Div(className=cl,
                     children=[html.Div(className="flex", children=[d_color, d_pos]), d_num, d_name, d_team, d_time,
                               d_time2, d_time3])
        )
    more = html.Img(id="more-race", src="/assets/images/more.svg")
    content.append(html.Div(className="race", children=[html.Div(className="title", children="Qualifying Results"),
                                                        html.Div(id="race-results", children=classement), more]))
    return content


# Création du header pour toutes les différentes pages grand prix
def header(year, event, session, sprint, first, last):
    if session != "fp" and session != "qualif" and (session != "sprint" or not sprint) and session != "race":
        head = html.A(children=html.Div(className="active link",
                                        children=[html.Label(className="desktop", children="Overview"),
                                                  html.Label(className="mobile", children="Home")]),
                      href=f"/grand-prix/{year}/{event}/overview"),
    else:
        head = html.A(children=html.Div(className="link",
                                        children=[html.Label(className="desktop", children="Overview"),
                                                  html.Label(className="mobile", children="Home")]),
                      href=f"/grand-prix/{year}/{event}/overview"),
    if session == "fp":
        head += html.A(children=html.Div(className="active link",
                                         children=[html.Label(className="desktop", children="Free Practice"),
                                                   html.Label(className="mobile", children="FP")]),
                       href=f"/grand-prix/{year}/{event}/fp"),
    else:
        head += html.A(children=html.Div(className="link",
                                         children=[html.Label(className="desktop", children="Free Practice"),
                                                   html.Label(className="mobile", children="FP")]),
                       href=f"/grand-prix/{year}/{event}/fp"),
    if session == "qualif":
        head += html.A(children=html.Div(className="active link",
                                         children=[html.Label(className="desktop", children="Qualifying"),
                                                   html.Label(className="mobile", children="Q")]),
                       href=f"/grand-prix/{year}/{event}/qualif"),
    else:
        head += html.A(children=html.Div(className="link",
                                         children=[html.Label(className="desktop", children="Qualifying"),
                                                   html.Label(className="mobile", children="Q")]),
                       href=f"/grand-prix/{year}/{event}/qualif"),
    if sprint:
        if session == "sprint":
            head += html.A(children=html.Div(className="active link",
                                             children=[html.Label(className="desktop", children="Sprint"),
                                                       html.Label(className="mobile", children="S")]),
                           href=f"/grand-prix/{year}/{event}/sprint"),
        else:
            head += html.A(children=html.Div(className="link",
                                             children=[html.Label(className="desktop", children="Sprint"),
                                                       html.Label(className="mobile", children="S")]),
                           href=f"/grand-prix/{year}/{event}/sprint"),
    if session == "race":
        head += html.A(children=html.Div(className="active link",
                                         children=[html.Label(className="desktop", children="Race"),
                                                   html.Label(className="mobile", children="Race")]),
                       href=f"/grand-prix/{year}/{event}/race"),
    else:
        head += html.A(children=html.Div(className="link", children=[html.Label(className="desktop", children="Race"),
                                                                     html.Label(className="mobile", children="Race")]),
                       href=f"/grand-prix/{year}/{event}/race"),
    if first[0]:
        previous = html.A(className="previous change off",
                          children=[html.I(className='fas fa-arrow-left'), html.Label(children="Previous")])
    else:
        previous = html.A(className="previous change",
                          children=[html.I(className='fas fa-arrow-left'), html.Label(children="Previous")],
                          href=f"/grand-prix/{first[1]}/overview")
    if last[0]:
        next = html.A(className="next change off",
                      children=[html.Label(children="Next"), html.I(className='fas fa-arrow-right')])
    else:
        next = html.A(className="next change",
                      children=[html.Label(children="Next"), html.I(className='fas fa-arrow-right')],
                      href=f"/grand-prix/{last[1]}/overview")
    return html.Div(className="gp-header", children=[
        html.Div(className="left", children=[
            previous
        ]),
        html.Div(className="hor-nav", children=head),
        html.Div(className="right", children=[
            next
        ]),
    ])


# Creating the FP page
def fp_design(Fp, parts, fp):
    parts["lap_times"].append(
        html.Div(className="plot lap_times", children=dcc.Graph(id=f'{Fp}_lap_times', figure=fp.lap_times(Fp))))
    parts["violin_st"].append(
        html.Div(className="plot violin_st", children=dcc.Graph(id=f'{Fp}_violin_st', figure=fp.violin_st(Fp))))
    parts["violin_lap"].append(
        html.Div(className="plot violin_lap", children=dcc.Graph(id=f'{Fp}_violin_lap', figure=fp.violin_lap(Fp))))
    parts["race_sim"].append(
        html.Div(className="plot race_sim", children=dcc.Graph(id=f'{Fp}_race_sim', figure=fp.race_sim(Fp))))
    parts["top_speed"].append(
        html.Div(className="plot top_speed", children=dcc.Graph(id=f'{Fp}_top_speed', figure=fp.top_speed(Fp))))
    parts["lap_comp"].append(
        html.Div(className="plot lap_comp", children=dcc.Graph(id=f'{Fp}_lap_comp', figure=fp.lap_comp(Fp))))
    return parts


def fp(year, event):
    fp = f1.get_fp(year, event)
    fp1, fp2, fp3, date = fp.get_load
    parts = {
        "lap_times": [],
        "violin_st": [],
        "violin_lap": [],
        "race_sim": [],
        "top_speed": [],
        "lap_comp": [],
    }
    comming = []
    if fp1:
        parts = fp_design("Fp1", parts, fp)
    elif date[0] != "Never":
        comming.append(
            html.Div(className="plot comming", children=html.P(children=date[0]))
        )
    if fp2:
        parts = fp_design("Fp2", parts, fp)
    elif date[1] != "Never":
        comming.append(
            html.Div(className="plot comming", children=html.P(children=date[1]))
        )
    if fp3:
        parts = fp_design("Fp3", parts, fp)
    elif date[2] != "Never":
        comming.append(
            html.Div(className="plot comming", children=html.P(children=date[2]))
        )
    return parts["lap_times"] + parts["violin_st"] + parts["violin_lap"] + parts["race_sim"] + parts[
        "top_speed"] + comming + parts["lap_comp"]


def Qualy(year, event, name):
    qualy = f1.get_quali(year, event)
    q, date = qualy.get_load
    main = []
    if q:
        try:
            main = qualy_result(main, qualy.results)
        except:
            utils.error(f"Could not show Qualy results for {name} {year}")
        main.append(
            html.Div(className="plot lap_times", children=dcc.Graph(id='qualy_lap_times', figure=qualy.lap_times())))
        main.append(
            html.Div(className="plot violin_st", children=dcc.Graph(id='qualy_violin_st', figure=qualy.violin_st())))
        main.append(
            html.Div(className="plot violin_lap", children=dcc.Graph(id='qualy_violin_lap', figure=qualy.violin_lap())))
        main.append(
            html.Div(className="plot top_speed", children=dcc.Graph(id='qualy_top_speed', figure=qualy.top_speed())))
        main.append(
            html.Div(className="plot lap_comp", children=dcc.Graph(id='qualy_lap_comp', figure=qualy.lap_comp())))
    else:
        main.append(
            html.Div(className="plot comming", children=html.P(children=date))
        )
    return main


def Sprint(year, event, format, name):
    sprint = f1.get_sprint(year, event, format)
    q, r, q_date, r_date = sprint.get_load
    main = []
    try:
        main = race_result(main, sprint.results)
    except:
        if r:
            utils.error(f"Could not show Race results for {name} {year}")
    if format == "sprint_shootout" and q:
        main.append(
            html.Div(className="plot lap_times",
                     children=dcc.Graph(id='sprint_lap_times', figure=sprint.Q_lap_times())))
        main.append(
            html.Div(className="plot violin_st",
                     children=dcc.Graph(id='sprint_violin_st', figure=sprint.Q_violin_st())))
        main.append(
            html.Div(className="plot violin_lap",
                     children=dcc.Graph(id='sprint_violin_lap', figure=sprint.Q_violin_lap())))
        main.append(
            html.Div(className="plot top_speed",
                     children=dcc.Graph(id='sprint_top_speed', figure=sprint.Q_top_speed())))
        main.append(
            html.Div(className="plot lap_comp", children=dcc.Graph(id='sprint_lap_comp', figure=sprint.Q_lap_comp())))
    elif format == "sprint_shootout":
        main.append(
            html.Div(className="plot comming", children=html.P(children=q_date))
        )
    if r:
        try:
            main.append(html.Div(className="plot lap_comp",
                                 children=dcc.Graph(id='race_delta_to_first', figure=sprint.delta_to_first())))
        except:
            utils.error(f"Sprint delta to first from {event} {year} could not be displayed")
        main.append(
            html.Div(className="plot lap_comp", children=dcc.Graph(id='race_lap_times', figure=sprint.lap_times())))
        main.append(
            html.Div(className="plot violin_st", children=dcc.Graph(id='race_violin_st', figure=sprint.violin_st())))
        main.append(
            html.Div(className="plot violin_lap", children=dcc.Graph(id='race_violin_lap', figure=sprint.violin_lap())))
        main.append(
            html.Div(className="plot top_speed", children=dcc.Graph(id='race_top_speed', figure=sprint.top_speed())))
    else:
        main.append(
            html.Div(className="plot comming", children=html.P(children=r_date))
        )
    return main


def Race(year, event, name):
    race = f1.get_race(year, event)
    r, date = race.get_load
    main = []
    try:
        exist, predict = strat.strat(name)
        if exist:
            main.append(
                html.Div(className="plot lap_comp", children=dcc.Graph(id='race_predict', figure=predict)))
    except:
        utils.error(f'Something went wrong went trying to display the prediction of {name} {year}')
    if r:
        try:
            main = race_result(main, race.results)
        except:
            utils.error(f"Could not show Race results for {name} {year}")
        try:
            main.append(
                html.Div(className="plot lap_comp",
                         children=dcc.Graph(id='race_delta_to_first', figure=race.delta_to_first())))
        except:
            utils.error(f"Race delta to first from {name} {year} could not be displayed")
        main.append(
            html.Div(className="plot lap_comp", children=dcc.Graph(id='race_lap_times', figure=race.lap_times())))
        main.append(
            html.Div(className="plot lap_comp", children=dcc.Graph(id='race_pos_evo', figure=race.drivers_evo())))
        main.append(
            html.Div(className="plot violin_st", children=dcc.Graph(id='race_violin_st', figure=race.violin_st())))
        main.append(
            html.Div(className="plot violin_lap", children=dcc.Graph(id='race_violin_lap', figure=race.violin_lap())))
        main.append(
            html.Div(className="plot top_speed", children=dcc.Graph(id='race_top_speed', figure=race.top_speed())))
    else:
        main.append(
            html.Div(className="plot comming", children=html.P(children=date))
        )
    return main


def content(year, event, session, we):
    if session == "fp":
        main = fp(year, event)
    elif session == "qualif":
        main = Qualy(year, event, we.Name.iloc[0])
    elif session == "race":
        main = Race(year, event, we.Name.iloc[0])
    elif session == "sprint":
        main = Sprint(year, event, we.Format.iloc[0], we.Name.iloc[0])
    else:
        main = "overall"
    return html.Div(className="main", children=main)


def overview(year, event, gp):
    with open(path.join("data", 'races_desc.json'), 'r') as f:
        races_info = json.load(f)
    race = races_info[gp.Name.iloc[0]]
    content = []
    content.append(
        html.Div(className="we_title", children=html.H1(children=f"Round {gp.Round.iloc[0]} : {gp.Name.iloc[0]}")))

    try:
        results = f1.get_race(year, event).results
        content = race_result(content, results)
    except:
        results = 0

    track_stats = [
        html.Div(className="track_name", children=race['name']),
        html.Div(className="infos", children=[
            html.Div(className="info", children=[html.P(className="Label", children="First Grand Prix"),
                                                 html.P(className="stat", children=race['first_gp'])]),
            html.Div(className="info", children=[html.P(className="Label", children="Number of Laps"),
                                                 html.P(className="stat", children=race['nb_laps'])]),
            html.Div(className="info", children=[html.P(className="Label", children="Circuit Length"),
                                                 html.P(className="stat", children=race['length'])]),
            html.Div(className="info", children=[html.P(className="Label", children="Race Distance"),
                                                 html.P(className="stat", children=race['race_distance'])]),
            html.Div(className="info full", children=[html.P(className="Label", children="Lap Record"),
                                                      html.P(className="stat", children=[race['lap_record']['time'],
                                                                                         html.Small(children=
                                                                                                    race['lap_record'][
                                                                                                        'owner'])])]
                     ),
        ])
    ]
    content.append(html.Div(className="flex", children=[html.Div(className="box stats", children=track_stats),
                                                        html.Img(className="box circuit", src=f"/{race['image']}")]))

    content.append(html.Div(className="box built", children=[html.H1(children="When was the track built?"),
                                                             html.P(children=race["built"].replace('\u00e2\u0080\u0099',
                                                                                                   '’'))]))
    content.append(html.Div(className="box story", children=[html.H1(children="When was its first Grand Prix?"),
                                                             html.P(children=race["first_gp-story"].replace(
                                                                 '\u00e2\u0080\u0099', '’'))]))
    content.append(html.Div(className="box like", children=[html.H1(children="What’s the circuit like?"),
                                                            html.P(children=race["like"].replace('\u00e2\u0080\u0099',
                                                                                                 '’'))]))
    content.append(html.Div(className="box why", children=[html.H1(children="Why go?"),
                                                           html.P(children=race["why"].replace('\u00e2\u0080\u0099',
                                                                                               '’'))]))
    content.append(html.Div(className="box where", children=[html.H1(children="Where is the best place to watch?"),
                                                             html.P(children=race["where"].replace('\u00e2\u0080\u0099',
                                                                                                   '’'))]))
    content.append(html.Div(className="box cprights", children=html.P(children="Source : formula1.com")))

    return html.Div(className="main overview", children=content)


def layout(session=None, year=None, event=None, **other):
    gp_data = get_dataframe()
    if year == None or event == None:
        # Map creation
        filtered_data = gp_data[gp_data['Year'] == gp_data['Year'].max()]
        map_fig = make_map(filtered_data)

        # Dropdown creation
        year_options = [{'label': str(year), 'value': year} for year in gp_data['Year'].unique()]
        year_dropdown = dcc.Dropdown(
            id='year-dropdown',
            options=year_options,
            value=gp_data['Year'].max()
        )
        return html.Div(className="content-map", children=[
            html.Div(className="year", children=[
                html.Label("Choose the year : "),
                year_dropdown
            ]),
            dcc.Graph(id='map-graph', figure=map_fig,
                      config=dict(displayModeBar=False, scrollZoom=False,
                                  showAxisDragHandles=False, showAxisRangeEntryBoxes=False)),
            dcc.Location(id='url', refresh=True)
        ])

    year = int(year)
    event = int(event)
    chosen_gp = gp_data.loc[(gp_data['Year'] == year) & (gp_data["Round"] == event)]
    # Defining page if all variable are set
    if session == "fp" or session == "qualif" or session == "race" or session == "sprint":
        # page = content(year, event, session, chosen_gp)
        try:
            page = content(year, event, session, chosen_gp)
        except:
            # TODO : Make it better
            page = html.P(children="Sorry there is a problem here")
            utils.error(f'Something went wrong went trying to display {session} of {chosen_gp.Name.iloc[0]} {year}')
    else:
        page = overview(year, event, chosen_gp)
    if chosen_gp.Format.iloc[0] == "sprint_shootout" or chosen_gp.Format.iloc[0] == "sprint":
        is_sprint = True
    else:
        is_sprint = False
    if chosen_gp.index == gp_data.index.min():
        first = [True]
    else:
        first = [False,
                 f"{gp_data.loc[chosen_gp.index - 1, 'Year'].iloc[0]}/{gp_data.loc[chosen_gp.index - 1, 'Round'].iloc[0]}"]
    if chosen_gp.index == gp_data.index.max():
        last = [True]
    else:
        last = [False,
                f"{gp_data.loc[chosen_gp.index + 1, 'Year'].iloc[0]}/{gp_data.loc[chosen_gp.index + 1, 'Round'].iloc[0]}"]
    head = header(str(year), str(event), session, is_sprint, first, last)
    return html.Div(className="content", children=[head, page])


# Fonction de rappel pour mettre à jour la carte
@dash.callback(
    dash.dependencies.Output('map-graph', 'figure'),
    [dash.dependencies.Input('year-dropdown', 'value')]
)
def update_map(year):
    gp_data = get_dataframe()
    filtered_data = gp_data[gp_data['Year'] == year]
    map_fig = make_map(filtered_data)
    return map_fig


# Fonction de rappel pour la redirection
@dash.callback(
    dash.dependencies.Output('url', 'pathname'),
    [dash.dependencies.Input('map-graph', 'clickData')])
def update_url(clickData):
    if clickData is not None:
        # Récupérer le nom du pays cliqué
        year = clickData['points'][0]['customdata'][0]
        round = clickData['points'][0]['customdata'][1]
        # Mettre à jour l'URL avec le nom du pays
        return f'/grand-prix/{year}/{round}/overview/'


@dash.callback(
    [dash.dependencies.Output("race-results", "className"), dash.dependencies.Output("more-race", "src")],
    dash.dependencies.Input("more-race", "n_clicks"),
    [dash.dependencies.State("race-results", "className"), dash.dependencies.State("more-race", "src")],
)
def toggle_race_results(n_clicks, current_class, current_src):
    if n_clicks is None:
        return current_class, current_src
    if n_clicks % 2 == 1:
        return "display-all", "/assets/images/less.svg"
    else:
        return "", "/assets/images/more.svg"
