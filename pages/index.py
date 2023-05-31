import dash
from dash import html, dcc

dash.register_page(__name__, path="/", title="Alpine Fan F1 Dashboard | Home", description="Stay connected with the thrilling world of Formula 1 with Alpine Fan\'s F1 Dashboard. Get Grand Prix datas, Formula analytics, and exclusive content.", image_url="https://alpinefan.robcorp.net/assets/images/logo.png")

def layout(*other):
    page = html.Div(className="inner", children=[
        html.Div(className="title", children=html.H1(children="Alpine Fan")),
        html.Div(className="creator", children=html.H3(children="Made by Robin Guerard")),
        html.Div(className="presentation", children=[html.P(children="Alpine Fan is a social media created by rob_runner (Robin Guerard)."),
                                                     html.P(children="On this Dashboard you will be able to access many Formula 1 plots very easily."),
                                                     html.P(children="Just 1 thing, if you are using some plots please keep the watermark to support us !"), html.Br(),
                                                     html.P(children="In the Grand Prix page you will be able to have data around all session since 2018."),
                                                     html.P(children="In season you will have plots around the different season statistiques."),
                                                     html.P(children="In statistics you have some global statistics around the Formula 1 world."), html.Br(),
                                                     html.P(children="Documentation contains all you need to know around this dashboard."),
                                                     html.P(children="Notebook contains some free analysis around some F1 week-ends."),
                                                     html.P(children="Contact is the page containing my infos if needed."), html.Br(),
                                                     html.P(children=["The Github link : ", html.A(children="https://github.com/RobinGuerard21/AlpineFanApp/", href="https://github.com/RobinGuerard21/AlpineFanApp")])])
    ])

    return html.Div(className="content centered", children=page)