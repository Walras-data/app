#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import plotly.graph_objects as go # or plotly.express as px
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

final = pd.read_csv("finals.csv")
final = final[final["year"] == 2019]
final.drop(["year"],1, inplace = True)
final = pd.melt(final, id_vars=['country'])

fig = go.Figure()

countries = list(set(final.country.tolist()))
ctry = final['country'].unique()




import dash
import dash_core_components as dcc
import dash_html_components as html
import random

from dash.dependencies import Input, Output

app = dash.Dash()
server = app.server
app.layout = html.Div([
    html.Div([
        html.Label('Country'),
        dcc.Dropdown(
            id='country_drop',
            options=[{'label': i, 'value': i} for i in ctry],
            value='',
            placeholder='Select...',
            multi=True
        )
    ],    
    style={'width': '20%', 'display': 'inline-block', 'margin-bottom': '20px'}),    
    dcc.Graph(id = "graph")
])

@app.callback(
    Output('graph', 'figure'),
    [Input('country_drop', 'value')])

def update_graph(country_drop):


    #country_color = [{
    #    country_drop: '#002366' 
   # } ]
    fig = go.Figure()

    for country in countries:
        #color = country_color.get(country, 'lightslategrey')
        col = ["purple", "red", "rosybrown",
            "royalblue", "rebeccapurple", "saddlebrown", "salmon"]
        color = random.choice(col) if country in country_drop else 'lightslategrey'
        highlight = color != 'lightslategrey' 
        data_filtered = final[final.country == country]
        plot_data = data_filtered
        axis = plot_data.variable.tolist()
        axis.append(axis[0])
        value = plot_data.value.tolist()
        value.append(value[0])
        fig.add_trace(
            go.Scatterpolar(
                r=value, 
                theta=axis,
                showlegend=highlight, 
                name=country, 
                hoverinfo='name+r',
                mode='lines',
                line_color=color,
                opacity=0.8 if highlight else 0.2,
                line_width=2.6 if highlight else 0.5 
            )
        )

    title = 'Comparison between countries in each indicator.'             '<br><span style="font-size:10px"><i>'             'Values range from 0 to 1</span></i>'

    fig.update_layout(
        title_text = title,
        title_font_color = '#333333',
        title_font_size = 14,    
        polar_bgcolor='white',
        polar_radialaxis_visible=True,
        polar_radialaxis_showticklabels=True,
        polar_radialaxis_tickfont_color='darkgrey',
        polar_angularaxis_color='grey',
        polar_angularaxis_showline=False,
        polar_radialaxis_showline=False,
        polar_radialaxis_layer='below traces',
        polar_radialaxis_gridcolor='#F2F2F2',
        polar_radialaxis_range=(0,1),
        polar_radialaxis_tickvals=[25, 50],
        polar_radialaxis_tickmode='array',

        legend_font_color = 'grey', # We don't want to draw attention to the legend 
        legend_itemclick = 'toggleothers', # Change the default behaviour, when click select only that trace
        legend_itemdoubleclick = 'toggle', # Change the default behaviour, when double click ommit that trace
        width = 1000, # chart size 
        height = 600 # chart size
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=False, use_reloader = False)
#app.run_server()  # Turn off reloader if inside Jupyter


# In[ ]:




