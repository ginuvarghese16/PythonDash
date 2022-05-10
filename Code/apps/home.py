import dash
from dash import html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

from app import app

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            #Header span the whole row
            #className: Often used with CSS to style elements with common properties.
            dbc.Col(html.H1("Welcome to the COVID-19 dashboard", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='This app shows the COVID-19 situation around the world using Plotly, Dash and Bootstrap. '
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children='It consists of two main pages: Global, which gives an overview of the COVID-19 situation around the world from 2020 to 2022, '
                                     'Vaccination, which gives an overview of the COVID-19 vaccination around the world.')
                    , className="mb-5")
        ]),

        dbc.Row([
            # 2 columns of width 6 with a border
            dbc.Col(dbc.Card(children=[html.H3(children='Get the original datasets used in this dashboard',
                                               className="text-center"),
                                       dbc.Row([dbc.Col(dbc.Button("Global", href="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv",
                                                                   color="primary"),
                                                        className="mt-3"),
                                                dbc.Col(dbc.Button("Vaccination", href="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv",
                                                                   color="primary"),
                                                        className="mt-3")], justify="center")
                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this dashboard',
                                               className="text-center"),
                                       dbc.Button("GitHub",
                                                  href="https://github.com/ginuvarghese16/PythonDash",
                                                  color="primary",
                                                  className="mt-3"),
                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-4"),

        ], className="mb-5"),
        dbc.Row([
            dbc.Col(html.Img(src=app.get_asset_url('Covid19.jpeg'),height="400px"), 
            width={"size": 3, "offset": 2})
        ],align="center"),
        html.A("Special thanks to metacept for the icon in COVID-19 Dash's logo and the image.",
               href="https://metacept.com/intellectual-property-rights-a-serious-impediment-to-global-immunization-or-a-mere-red-herring/")

    ])

])

# needed only if running this as a single page app
#if __name__ == '__main__':
#    app.run_server(port=8098,debug=True)