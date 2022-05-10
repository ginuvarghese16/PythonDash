#import packages to create app
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd
import numpy as np

covid_data = pd.read_csv("E:\covid_all.csv", index_col=False, na_values =("N/A", "NA", "--", " ", "-"))

#get unique continents
cont_names = covid_data['continent'].unique()
cols=list(covid_data.columns)
loc_cols=list(covid_data.columns)

covid_data1 = covid_data.sort_values('month_year', ascending=True)

#covid_data['month_year'] = pd.to_datetime(covid_data['month_year'], format='%Y/%B')
# needed only if running this as part of a multipage app
from app import app
#app = dash.Dash(__name__)
#change background and color text
colors = {
    #background to rgb(233, 238, 245)
    'background': '#e9eef5',
    'text': '#1c1cbd'
}
color_discrete_map = {'Asia': '#636EFA', 'Africa': '#EF553B', 
    'Europe': '#AB63FA','North America': '#00CC96', 'Oceania': '#FFA15A','South America':'#FFFF00'}


# change to app.layout if running as single page app instead
layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1('COVID-19 WORLDWIDE AT A GLANCE',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    #Add multiple line text 
    html.Div('''
        Visualizing COVID-19 around the Globe from 2020 to 2022 
    ''', style={
        'textAlign': 'center',
        'color': colors['text']}
    ),
    html.Div([
        html.Div([
            html.Label('Select Continent/Continents'),
            dcc.Dropdown(id='cont_dropdown',
                        options=[{'label': i, 'value': i}
                                for i in cont_names],
                        value=['Asia','Europe','North America','Africa','South America','Oceania'],
                        multi=True
            )
        ],style={'width': '49%', 'display': 'inline-block'}),
        ]),
    dcc.Graph(
        id='coviddeaths'
    ),
    html.Label('Select Variable to display on Graphs'),
        dcc.Dropdown(id='y_dropdown',
            options=[  
                {'label': 'Total Cases', 'value': 'total_cases'},                      
                {'label': 'New Cases', 'value': 'new_cases'},
                {'label': 'ICU Patients', 'value': 'icu_patients'}],
            value='total_cases',
            style={'width':'50%'}
    ),
    html.Div([
        dcc.Graph(id ='covidcases')]),
    html.Label('Select top or bottom'),
        dcc.Dropdown(id='toportail',
            options=[  
                {'label': 'Top 10', 'value': 'head(10)'},                      
                {'label': 'Bottom 10', 'value': 'tail(10)'},],
            value='head(10)',
            style={'width':'50%',}
    ),
    html.Div([
            dcc.Graph(
                id='topcovid'
            ),
        ],style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),
    html.Div([
            dcc.Graph(
                id='topdeath'
            ),
        ],style={'width': '50%', 'display': 'inline-block'}),

])

@app.callback(
    Output(component_id='coviddeaths', component_property='figure'),
    Input(component_id='cont_dropdown', component_property='value')
   
)
def update_graph(selected_cont):
    if not selected_cont:
        return dash.no_update
    data =[]
    for j in selected_cont:
            data.append(covid_data[covid_data['continent'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=cols)
    df=df.infer_objects()
    scat_fig = px.scatter(data_frame=df, y= "life_expectancy",x="total_deaths",
                          size="population", color="continent", hover_name="location",
                          #add frame by year to create animation grouped by country
                          animation_frame="date", animation_group="location",
                          color_discrete_map=color_discrete_map,
                          #specify formating of markers and axes
                          log_x = True, size_max=50, range_x=[10,10000000], range_y=[28,92],
                          # change labels
                          labels={'continent':'continent',
                                  'location':'Country'})
                            # Change the axis titles
    scat_fig.update_layout({'xaxis': {'title': {'text': 'Total Covid deaths'}},
                                      'yaxis': {'title': {'text': 'Life Expectancy'}}},  
                                                # Change the axis titles and add background colour using rgb syntax
                                                  plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')
    scat_fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 10
    scat_fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5

    return scat_fig



@app.callback(
    Output(component_id='covidcases', component_property='figure'),
    [Input(component_id='cont_dropdown', component_property='value'),
    Input(component_id='y_dropdown', component_property='value')]
)
def update_map(selected_cont,yvar):
    if not (selected_cont or yvar):
        return dash.no_update
    data =[]
    for j in selected_cont:
            data.append(covid_data1[covid_data1['continent'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=cols)
    df=df.infer_objects()
    
    map_fig= px.choropleth(df,locations="iso_code", color=df[yvar],
            hover_name="location",hover_data=['continent','location'],animation_frame="date",    
            color_continuous_scale='Turbo',range_color=[df[yvar].min(), df[yvar].max()],
            labels={'year':'Year','continent':'Continent',
                'location':'country', 'total_cases':'Total cases'})
    map_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')
    map_fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 2
    map_fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5
        
    return map_fig

@app.callback(
    [Output(component_id='topcovid', component_property='figure'),
    Output(component_id='topdeath', component_property='figure')],
    [Input(component_id='cont_dropdown', component_property='value'),
    Input(component_id='toportail', component_property='value')]
)
def update_maps(selected_cont,yvar):
    if not (selected_cont or yvar):
        return dash.no_update  
    data =[]
    for j in selected_cont:
            data.append(covid_data[covid_data['continent'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=cols)
    
    df=df.infer_objects()
    
    total = df.groupby(['continent','location'])['total_cases', 'total_deaths'].max().reset_index()
    if yvar == 'tail(10)':
        top_cases = total.sort_values('total_cases', ascending=False).tail(10)
        top_deaths = total.sort_values('total_deaths', ascending=False).tail(10)
        fig_t = px.bar(top_cases, x="location", y="total_cases", color="location", title="Least Covid Affected Countries",labels={'total_cases':'Total Covid Cases',
                'location':'Country'}).update_xaxes(categoryorder='total descending')
        fig_l = px.bar(top_deaths, x="location", y="total_deaths", color="location", title="Countries with Least Covid Deaths",labels={'total_deaths':'Total Covid Deaths',
                'location':'Country'} )
    else:
        top_cases = total.sort_values('total_cases', ascending=False).head(10)
        top_deaths = total.sort_values('total_deaths', ascending=False).head(10)
        fig_l = px.bar(top_deaths, x="location", y="total_deaths", color="location", title="Top Countries with Covid Deaths",labels={'total_deaths':'Total Covid Deaths',
                'location':'Country'} )
        fig_t = px.bar(top_cases, x="location", y="total_cases", color="location", title="Top Covid Affected Countries",labels={'total_cases':'Total Covid Cases',
                'location':'Country'}).update_xaxes(categoryorder='total descending')  
    
    fig_t.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')
    
    
    fig_l.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')
    
    return [fig_t, fig_l]

# needed only if running this as a single page app
#if __name__ == '__main__':
#    app.run_server(port=8097,debug=True)
