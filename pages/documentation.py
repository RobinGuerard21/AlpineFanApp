import dash
from dash import html, dcc

dash.register_page(__name__, path="/documentation", path_template="/documentation/<part>", title="Alpine Fan F1 Dashboard | Documentation", description="Have a better understanding of this Formula 1 dashboard or about Alpine Fan !", image="images/logo.png")

def get_page(part):
    if part == None or part == 0:
        with open('README.md', 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        content = html.Div(className="doc-main", children=[
            html.Div(className="change"),
            dcc.Markdown(children=markdown_content, className="md read"),
            html.A(children=html.Div(className="change right", children=html.Div(children=html.I(className="fas fa-chevron-right"))),
                   href="/documentation/process")
        ])
    else:
        with open('docs/process.md', 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        content = html.Div(className="doc-main", children=[
            html.A(children=html.Div(className="change left", children=html.Div(children=html.I(className="fas fa-chevron-left"))), href="/documentation"),
            dcc.Markdown(children=markdown_content, className="md doc"),
            html.Div(className="change")
        ])
    return content

def layout(part=None, **other):
    page = get_page(part)
    # if part != None:
    #     page = get_page(part)
    # else:
    #     page = html.Div(className="Comming-soon", children=html.P(children="Coming Soon ..."))
    return page
