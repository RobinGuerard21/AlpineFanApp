import dash
from dash import html, dcc

dash.register_page(__name__, path="/contact")

def layout(**other):
    page = html.Div(className="inner", children=[
        html.Div(className="title", children=html.H1(children="Contact")),
        html.Div(className="presentation",
                 children=[html.P(children=html.H3(children="Concerning Alpine Fan")),
                           html.P(children="If you encounter any problem on the dashboard or the Alpine package"),
                           html.P(children="Or that you have any suggestions you can open an issue on Github"),
                           html.P(children=html.A(href="https://github.com/RobinGuerard21/AlpineFanApp/issues", children=[html.I(className='fab fa-github'), "Issues Page"])),
                           html.Br(),
                           html.P(children=html.H3(children="Robin Guerard")),
                           html.P(
                               children="You can come see me on social medias !"),
                           html.Div(className="media", children=[
                               html.A(href="https://instagram.com/alpines_fan?igshid=MzRlODBiNWFlZA==",
                                      children=[html.I(className='fab fa-instagram'), "@alpines_fan"]),
                               html.A(href="https://discord.gg/QsUPRsEjWT",
                                      children=[html.I(className='fab fa-discord'), "Rob_runner's Community"]),
                               html.A(href="https://www.youtube.com/channel/UC4KP84qfnu9RmbmLFZDSv9A",
                                      children=[html.I(className='fab fa-youtube'), "rob_runner"]),
                           ]),
                           html.Br(),
                           html.P(children="For any professionnal contact here's my mail."),
                           html.P(children="robin.guerard@ynov.com")])
    ])

    return html.Div(className="content centered", children=page)