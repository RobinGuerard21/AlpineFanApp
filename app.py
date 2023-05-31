import dash
from dash import Dash, html
import logger
import flask
import os

logger

app = Dash(__name__, use_pages=True, external_stylesheets=['https://use.fontawesome.com/releases/v5.7.2/css/all.css'])

server = app.server

app.layout = html.Div(className="window", children=[
    # Beginning of the sidebar
    html.Div(className="side-bar", children=[
        # Top part of the sidebar
            html.Div(className="vert-nav", children=[
                html.A(children=html.Img(className="logo", src=app.get_asset_url('images/logo.png')), href='/'),
                html.A(children=html.Div(className="link", children='Grand Prix'), href='/grand-prix'),
                html.A(children=html.Div(className="link", children='Seasons'), href='/seasons'),
                html.A(children=html.Div(className="link", children='Statistics'), href='/statistics')
            ]),
        # Bottom part of the sidebar
            html.Div(className="vert-nav", children=[
                html.A(children=html.Div(className="link", children='Documentation'), href='/documentation'),
                html.A(children=html.Div(className="link", children='Notebooks'), href='/notebooks'),
                html.A(children=html.Div(className="link", children='Contact'), href='/contact')
            ]),
        ]),
    # End of the sidebar
    # Pages part
    dash.page_container

    ]
)

@server.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(server.root_path, 'assets'),
                                     'favicon.ico')

if __name__ == '__main__':
    app.run_server(debug=True)