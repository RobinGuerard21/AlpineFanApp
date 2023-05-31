import dash
from dash import html, dcc

dash.register_page(__name__, path="/statistics", title="Alpine Fan F1 Dashboard | Statistics", description="Get all Formula 1's statistics you want ! With Alpine Fan you will never miss F1 again ! ", image="images/logo.png")

def layout(**other):
    page = html.Div(className="Comming-soon", children=html.P(children="Coming Soon ..."))
    return html.Div(className="content", children=page)