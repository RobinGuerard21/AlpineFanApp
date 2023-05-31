import dash
from dash import html, dcc
import os

dash.register_page(__name__, path="/notebooks", path_template="/notebooks/<part>", title="Alpine Fan F1 Dashboard | Notebooks", description="Enjoy some short Analysis around some F1 Week-ends ! Take 5 minute to chill and have a better understanding of the week-end !", image="images/logo.png")

app = dash.get_app()

def get_page(part):
    with open('notebooks/bahrain2023.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    return dcc.Markdown(children=markdown_content, className="md ")

def layout(part=None, **other):
    page = get_page(part)

    # Create the HTML iframe element to display the notebook
    # iframe = html.Iframe(src=notebook_path, style={'width': '100%', 'height': '800px'})

    return html.Div(className="content centered", children=page)