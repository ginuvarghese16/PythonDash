#import packages to create app
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd
import numpy as np

vaccine_data = pd.read_csv("E:\covid_vaccines.csv", index_col=False, na_values =("N/A", "NA", "--", " ", "-"))

vaccine_data1 = vaccine_data.sort_values('month_year', ascending=True)

cont_names = vaccine_data['continent'].unique()
cols=list(vaccine_data.columns)


color_discrete_map = {'Asia': '#636EFA', 'Africa': '#EF553B', 
    'Europe': '#AB63FA','North America': '#00CC96', 'Oceania': '#FFA15A','South America':'#FFFF00'}

# needed only if running this as a single page app
from app import app
#app = dash.Dash(__name__)
#change background and color text
colors = {
    #background to rgb(233, 238, 245)
    'background': '#e9eef5',
    'text': '#1c1cbd'
}



# change to app.layout if running as single page app instead
layout = html.Div(style={'backgroundColor': colors['background']},children=[
    dbc.Container([
        dbc.Row([
            #Header span the whole row
            #className: Often used with CSS to style elements with common properties.
            dbc.Col(html.H1("COVID-19 Vaccination around the globe",        
             style={
            'textAlign': 'center',
            'color': colors['text']}), 
            className="mb-5 mt-5")
        ]),
        html.Div([
            html.Div([
                html.Label('Select Continent/Continents'),
                dcc.Dropdown(id='cont_dropdown',
                            options=[{'label': i, 'value': i}
                                    for i in cont_names],
                            value=['Asia','Europe','Africa','North America','South America','Oceania'],
                            multi=True
                )
            ],style={'width': '49%', 'display': 'inline-block'}),
            html.Div([
                    html.Label('Select Variable to display on the Graphs'),
                    dcc.Dropdown(id='y_dropdown',
                        options=[        
                            {'label': 'People Vaccinated', 'value': 'people_vaccinated'},
                            {'label': 'Fully Vaccinated People', 'value': 'people_fully_vaccinated'},
                            {'label': 'Total Booster Vaccinations', 'value': 'total_boosters'}],
                        value='people_vaccinated',
                    )
                ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
            ]),
        html.Div([
            dcc.Graph(
                id='mapchart'
            ),
            ],style={'width': '80%', 'margin-left': '10%','display': 'inline-block'}),
        
        html.Div([
                dcc.Graph(
                        id='bubblechart'
                ),
            ]),
        html.Div([
                dcc.Graph(
                    id='topvacc'
                ),
            ],style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),
        html.Div([
                dcc.Graph(
                    id='leastvacc'
                ),
            ],style={'width': '50%',  'display': 'inline-block'}),
    ])
])


@app.callback(
    [Output(component_id='mapchart', component_property='figure'),
    Output(component_id='bubblechart', component_property='figure')],
    [Input(component_id='cont_dropdown', component_property='value'),
    Input(component_id='y_dropdown', component_property='value')]
)
def update_graphs(selected_count,eyvar):
    if not (selected_count or eyvar):
        return dash.no_update
    data =[]
    for j in selected_count:
            data.append(vaccine_data[vaccine_data['continent'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=cols)
    df=df.infer_objects()
    
    geofig= px.choropleth(df,locations="iso_code", color=eyvar,
                       hover_name="location",hover_data=['continent','people_vaccinated'],animation_frame="date",    
                       color_continuous_scale='Turbo',range_color=[df[eyvar].min(), df[eyvar].max()],
                       labels={'people_vaccinated':'people_vaccinated','year':'Year','continent':'Continent',
    'location':'Country'})


    #update text to be number format rounded with unit 
    geofig.update_traces(hovertemplate='%{text:.2s}')
    #update text to be fo7nt size 8 and hide if text can not stay with the uniform size
    geofig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',
        plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)',
        showlegend=False, margin=dict( b=200),xaxis_title="")
    geofig['layout']['updatemenus'][0]['pad']=dict(r= 50, t= 90)
    geofig['layout']['sliders'][0]['pad']=dict(r= 20, t= 80,)
    geofig.update_layout( width=800, height=550, margin={"r":0,"t":0,"l":0,"b":0})
    geofig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 50
    geofig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5

    scat_fig = px.scatter(data_frame=df, y= "total_vaccinations_per_hundred",x="total_vaccinations",
               size="total_vaccinations_per_hundred", color="continent", hover_name="location",
               #add frame by date to create animation grouped by location
               animation_frame="date", animation_group="location",
               #specify formating of markers and axes
               log_x = True, size_max=60, range_x=[100000,100000000], range_y=[0,350],
               # change labels
               labels={'continent':'continent',
                       'location':'Country'})
               # Change the axis titles
    scat_fig.update_layout({'xaxis': {'title': {'text': 'Total Vaccinations'}},
                       'yaxis': {'title': {'text': 'Total Vaccinations per hundred'}}})
    scat_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')
    scat_fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 50
    scat_fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5  
        
    return [geofig, scat_fig]

@app.callback(
    [Output(component_id='topvacc', component_property='figure'),
    Output(component_id='leastvacc', component_property='figure')],
    Input(component_id='cont_dropdown', component_property='value')
    )

def update_bars(selected_count):
    if not (selected_count):
        return dash.no_update
    data =[]
    for j in selected_count:
            data.append(vaccine_data[vaccine_data['continent'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=cols)
    df=df.infer_objects()
    
    tot_vacc = df.groupby(['location','continent'])['total_vaccinations', 'daily_vaccinations'].max().reset_index()
    top_ = tot_vacc.sort_values('total_vaccinations', ascending=False).head(10)
    low_ = tot_vacc.sort_values('total_vaccinations', ascending=True).head(10)
    
    fig = px.bar(top_, x="location", y="total_vaccinations", color="location", title="Top Vaccinated Countries", labels={'total_vaccinations':'Total Vaccinations',
            'location':'Country'})
    fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')
    fig.update_layout(margin={"r":10,"t":100,"l":10,"b":0})
    
    fig_ = px.bar(low_, x="location", y="total_vaccinations", color="location", title="Least Vaccinated Countries", labels={'total_vaccinations':'Total Vaccinations',
            'location':'Country'}).update_xaxes(categoryorder='total descending')
    fig_.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')
    fig_.update_layout(margin={"r":1,"t":100,"l":1,"b":0})
    
    return [fig, fig_]
    
# needed only if running this as a single page app
#if __name__ == '__main__':
#    app.run_server(port=8079,debug=True)
