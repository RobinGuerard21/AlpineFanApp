import dash
from dash import html, dcc

dash.register_page(__name__, path="/documentation", path_template="/documentation/<part>")

def get_page(part):
    with open('docs/process.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    return dcc.Markdown(children=markdown_content, className="md-doc")

def layout(part=None, **other):
    page = get_page(part)
    # if part != None:
    #     page = get_page(part)
    # else:
    #     page = html.Div(className="Comming-soon", children=html.P(children="Coming Soon ..."))
    return html.Div(className="content", children=page)