import dash
from dash import Dash, html, dcc
import logger
import flask
import os
from dash.dependencies import Input, Output
import Alpine.utils as utils
import gen.data


app = Dash(__name__, use_pages=True, external_stylesheets=['https://use.fontawesome.com/releases/v5.7.2/css/all.css'],
           meta_tags=[{'name': 'viewport',
                       'content': "width=device-width, initial-scale=1.0, viewport-fit=cover, user-scalable=no, maximum-scale=1"},
                      {'name': "apple-mobile-web-app-capable", 'content': 'yes'},
                      {'name': "apple-mobile-web-app-status-bar-style", 'content': "black-translucent"}])

server = app.server

app.index_string = '''
<!DOCTYPE html>
<html lang="en">
    <head>
        <link rel="manifest" href="/manifest.webmanifest">
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-7KZYT80WN5"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-7KZYT80WN5');
    </script>
    <script>
        document.addEventListener("DOMContentLoaded", function(event) {
            function splash() {
                document.getElementById("latest").style.display = "none"
                document.querySelector("body").classList.add("loading");
                document.querySelector(".load").classList.add("show");
                const welcomeText = document.getElementById("welcome");
                const welcomeMessage = "Welcome!";
                const delayBetweenLetters = 150; // milliseconds

                let index = 0;
                function showWelcomeText() {
                    if (index < welcomeMessage.length) {
                        welcomeText.innerHTML += welcomeMessage.charAt(index);
                        index++;
                        setTimeout(showWelcomeText, delayBetweenLetters);
                    }
                }

                setTimeout(showWelcomeText, 500); // Delay before showing the welcome text
                function close() {
                    document.querySelector(".load").classList.remove("show");
                    document.querySelector("body").classList.remove("loading");
                    document.getElementById("latest").style.display = "block"
                }
                setTimeout(close, 2500);    
            }
            function latest() {
                function close_latest() {
                    document.getElementById("latest").classList.remove("active");
                }
                document.getElementById("latest").classList.add("active")
                setTimeout(close_latest, 5000)
            }
            const splashDisplayed = sessionStorage.getItem("splashDisplayed");
            if (!splashDisplayed) {
                sessionStorage.setItem("splashDisplayed", "true");
                splash()
                setTimeout(latest, 3000)
            } else {
                setTimeout(latest, 500)
            }
        });
    </script>
    <body class="">
        <div class="load">
            <div class="logo"><img src="/assets/images/logo.svg"></div>
            <div id="welcome">
            </div>
        </div>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div(className="window", children=[
    html.Div(id="latest", children=[html.Label(className="desktop", children="Last Race"), html.I(className="fas fa-arrow-right")]),
    dcc.Location(id='urllatest', refresh=True),
    # Beginning of the sidebar
    html.Div(className="side-bar", children=[
        # Top part of the sidebar
        html.Div(className="vert-nav", children=[
            html.A(children=html.Img(className="logo", src=app.get_asset_url('images/logo.png')), href='/'),
            html.A(href='/grand-prix', children=html.Div(className="link",
                                                         children=[html.I(className="fas fa-flag-checkered"),
                                                                   html.Label(className="desktop",
                                                                              children='Grand Prix')])),
            html.A(href='/seasons', children=html.Div(className="link",
                                                      children=[html.I(className="fas fa-trophy"),
                                                                html.Label(className="desktop", children='Seasons')])),
            html.A(href='/statistics', children=html.Div(className="link",
                                                         children=[html.I(className="fas fa-chart-line"),
                                                                   html.Label(className="desktop",
                                                                              children='Statistics')]))
        ]),
        # Bottom part of the sidebar
        html.Div(className="vert-nav", children=[
            html.A(href='/documentation', children=html.Div(className="link",
                                                            children=[html.I(className="fas fa-book"),
                                                                      html.Label(className="desktop",
                                                                                 children='Documentation')])),
            html.A(href='/notebooks', children=html.Div(className="link",
                                                        children=[html.I(className="fas fa-file"),
                                                                  html.Label(className="desktop",
                                                                             children='Notebooks')])),
            html.A(href='/contact', children=html.Div(className="link",
                                                      children=[html.I(className="fas fa-address-card"),
                                                                html.Label(className="desktop", children='Contact')]))
        ]),
    ]),
    # End of the sidebar
    # Pages part
    dash.page_container
])

@dash.callback(Output('urllatest', 'pathname'),
              [Input('latest', 'n_clicks')])
def redirect_to_gp(n_clicks):
    if n_clicks is not None:
        return utils.time.get_latest()

@server.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(server.root_path, 'assets'),
                                     'favicon.ico')


@server.route('/manifest.webmanifest')
def manifest():
    return flask.send_from_directory(os.path.join(server.root_path, 'assets'),
                                     'manifest.json', mimetype='application/manifest+json')


@server.route('/robots.txt')
def robot():
    return flask.send_from_directory(server.root_path,
                                     'robots.txt')


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
