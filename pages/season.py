import dash
from dash import html, dcc

dash.register_page(__name__, path="/seasons", path_template="/seasons/<year>", title="Alpine Fan F1 Dashboard | Seasons", description="Comming Soon ! Here you will have access to some statistics around the season !", image="images/logo.png")

def layout(year=None, **other):
    page = html.Div(className="Comming-soon", children=html.P(children="Coming Soon ..."))
    return html.Div(className="content", children=page)