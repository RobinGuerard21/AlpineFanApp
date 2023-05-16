import dash
from dash import html, dcc
import os

dash.register_page(__name__, path="/notebooks", path_template="/notebooks/<part>")

app = dash.get_app()

def get_page(part):
    with open('notebooks/bahrein2023.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    return dcc.Markdown(children=markdown_content)

def layout(part=None, **other):
    page = get_page(part)

    # Create the HTML iframe element to display the notebook
    # iframe = html.Iframe(src=notebook_path, style={'width': '100%', 'height': '800px'})

    return html.Div(className="content", children=page)