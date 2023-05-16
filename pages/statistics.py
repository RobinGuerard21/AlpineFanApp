import dash
from dash import html, dcc

dash.register_page(__name__, path="/statistics")

def layout(**other):
    page = html.Div(className="Comming-soon", children=html.P(children="Coming Soon ..."))
    return html.Div(className="content", children=page)