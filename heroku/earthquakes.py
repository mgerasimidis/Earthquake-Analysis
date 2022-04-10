#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
from folium.plugins import HeatMap
import plotly.express as px
import folium
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from folium.plugins import FastMarkerCluster, MarkerCluster


from jupyter_dash import JupyterDash
import dash
from dash import dcc
from dash import html
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

from dash.dependencies import Input, Output


# ### Analysis Part I (All earthquakes)

# In[16]:


df = pd.read_csv(r'C:\Users\KOSTAS\Desktop\projects\repositories\repos_data\earthquakes_data\earthquake_data.csv')


# # Paizontas me folium 

# In[17]:


major_df = pd.read_csv(r'C:\Users\KOSTAS\Desktop\projects\repositories\repos_data\earthquakes_data\major_earthquake_data.csv')


# In[18]:


my_df = major_df[major_df['Year'] == 2000]


# In[19]:


my_df = my_df.reset_index()


# In[20]:


my_df.drop('index',axis=1,inplace=True)


# In[21]:


def map_from_df(year):
    major_df = pd.read_csv(r'C:\Users\KOSTAS\Desktop\projects\repositories\repos_data\earthquakes_data\major_earthquake_data.csv')
    my_df = major_df[major_df['Year'] == year]
    my_df = my_df.reset_index()
    my_df.drop('index',axis=1,inplace=True)
    
    base_map = folium.Map(location=[major_df['Latitude'].mean(), major_df['Longitude'].mean()],
                    zoom_start=6, control_scale=True)
    earthquakes_locations = my_df[['Latitude', 'Longitude']]
    earthquakes_location_list = earthquakes_locations.values.tolist()
    for point in range(len(earthquakes_location_list)):
        folium.Marker(earthquakes_location_list[point], popup = ["Month:"+str(my_df['Month'][point]),
                                                                 "Date:" + str(my_df['Date'][point]),
                                                                                       
            "Magnitude (R):"+str(my_df['Magnitude (Richter)'][point]) 
                                                                ] ).add_to(base_map)
    return base_map


# In[22]:


#map_1901.save('map_1901.html')


# In[23]:


# for i in df['Year'].unique()[0:-1]:
#     my_map = map_from_df(i)
#     my_map.save('map_'+str(i)+'.html')


# # Final Dash

# In[24]:


# Step 1. Launch the application
df = pd.read_csv(r'C:\Users\KOSTAS\Desktop\projects\repositories\repos_data\earthquakes_data\earthquake_data.csv')
year_min = df['Year'].min()
year_max = df['Year'].max() -1

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#FFFACA',
    'text': '#7FDBFF'
    },
    

app.layout = html.Div(style={'backgroundColor': colors[0]['background']},children = [
    html.P("Year:"),
    dcc.Dropdown(               #Create a dropdown
        id='drop-down',
        options=df['Year'].unique()[0:-1],
        value=df['Year'].unique()[0],
    ),
    
    dcc.Graph(id="bar-chart", figure = {},style = {'display': 'inline-block'}), #  Create a plotly figure
    
    dcc.Graph(id="map-chart", figure={}, style = {'display': 'inline-block'}), #  Create a plotly figure
    
    
    html.P("Major earthquakes map:"),
    html.Iframe(id = 'map', width = '50%', height = '600', style = {'display': 'inline-block'}),
    dcc.Graph(id="ball-plot", figure={}, style = {'display': 'inline-block'}),

    
    #html.P("Major earthquakes scatterplot:", style = {'margin':'auto','width': "50%"}),
    dcc.Graph(id="scatter-plot", figure={}, style = {'margin':'auto','width': "50%"}),
    
    
    dcc.RangeSlider(               # Step 3. Create a slider
        id='range-slider',
        min=year_min, max=year_max, step=1,
        marks={year_min: str(year_min), 1905:'1905',1910:'1910',1915:'1915',1920:'1920',1925:'1925',
               1930:'1930',1935:'1935',1940:'1940',1945:'1945',1950:'1950',1955:'1955',
               1960:'1960',1965:'1965',1970:'1970',1975:'1975',1980:'1980',1985:'1985',
               1990:'1990',1995:'1995',2000:'2000',2005:'2005',2010:'2010',2015:'2015',  year_max: str(year_max)},
        value=[0.5, 1.5]
    ),
    
    #dcc.Graph(id="ball-plot", figure={}, style = {'display': 'inline-block'})
    
])

@app.callback(
    Output("bar-chart", "figure"),
   # Output('map-chart',"figure")],
    [Input("drop-down", "value")])

def update_bar_chart(year):
    df = pd.read_csv(r'C:\Users\KOSTAS\Desktop\projects\repositories\repos_data\earthquakes_data\earthquake_data.csv')
    mask = df['Year'] == year
    
    df1 = df[mask].groupby('Earthquake_class').count()['Year'].to_frame().reset_index()
    
    df1.rename(columns = {'Year': 'Number of earthquakes'}, inplace = True)
    
    fig = px.bar(df1, x= 'Earthquake_class', y= 'Number of earthquakes',width=700, height=400,
                title="Observed earthquakes of each class for year " + str(year))
    
    style={'backgroundColor': colors[0]['background']}
    
    fig.update_layout({
        'plot_bgcolor': colors[0]['background'],
        'paper_bgcolor': colors[0]['background'],
    })
    
    return fig

@app.callback(
    Output("map-chart", "figure"),
   # Output('map-chart',"figure")],
    [Input("drop-down", "value")])

def update_bar_chart(year):
    df = pd.read_csv(r'C:\Users\KOSTAS\Desktop\projects\repositories\repos_data\earthquakes_data\earthquake_data.csv')
    mask = df['Year'] == year
    
    df1 = df[mask].groupby('Month').count()['Year'].to_frame().reset_index()
    
    df1.rename(columns = {'Year': 'Number of earthquakes'}, inplace = True)
    
    fig = px.bar(df1, x= 'Month', y= 'Number of earthquakes',width=700, height=400,
                title="Observed earthquakes per month for year " + str(year))
    
    fig.update_layout({
        'plot_bgcolor': colors[0]['background'],
        'paper_bgcolor': colors[0]['background'],
    })
    
    return fig
# ws edw doulevei ok

@app.callback(
    Output("scatter-plot", "figure"),
   # Output('map-chart',"figure")],
    [Input("range-slider", "value")])

def my_scatterplot(slider_range):
    major_df = pd.read_csv(r'C:\Users\KOSTAS\Desktop\projects\repositories\repos_data\earthquakes_data\major_earthquake_data.csv')
    low, high = slider_range
    my_df = major_df[(major_df['Year'] >= low) & (major_df['Year'] <= high)]
    fig = px.scatter(my_df, x='Year', y='Magnitude (Richter)', color='District',
                 size= 'Magnitude (Richter)', title = 'Major earthquakes (with districts)')
    
    fig.update_layout({
        'plot_bgcolor': colors[0]['background'],
        'paper_bgcolor': colors[0]['background'],
    })
    
    return fig


@app.callback(
    Output("ball-plot", "figure"),
   # Output('map-chart',"figure")],
    [Input("drop-down", "value")])

def ball_plot(year):
    df = pd.read_csv(r'C:\Users\KOSTAS\Desktop\projects\repositories\repos_data\earthquakes_data\earthquake_data.csv')
    many = df[(df['Year'] == 1953) & (df['Month'] == 8) & (df['Date'] == 13)]
    new_row = many.iloc[0] 
    many = many.append(new_row, ignore_index = True)
    many.at[6,'Earthquake_class']= 'Moderate_Earthquake'
    many.at[6,'Magnitude (Richter)']= 10
    
    ani = px.scatter(many, x="Hours", y="Magnitude (Richter)", animation_frame="Hours", 
           size="Magnitude (Richter)", color="Earthquake_class", hover_name="Magnitude (Richter)",
           size_max=30, range_x=[0,16], range_y=[4,6], title = 'Earthquakes in Ithaka 13/8/1953')
    
    ani.update_layout({
        'plot_bgcolor': colors[0]['background'],
        'paper_bgcolor': colors[0]['background'],
    })
    
    
    return ani


@app.callback(
    Output("map", "srcDoc"),
    [Input("drop-down", "value")])

def update_map(year):
    #if year == 1901:
     #   return open(r'C:\Users\KOSTAS\Desktop\projects\E_D_A-projects-python\Earthquakes_Analysis\maps\map_1901.html','r').read()
    #else:
     #   return open(r'C:\Users\KOSTAS\Desktop\projects\E_D_A-projects-python\Earthquakes_Analysis\maps\map_1910.html','r').read()
    for i in range(1901,2018):
        if i == year:
            return open(r'C:\Users\KOSTAS\Desktop\projects\repositories\Earthquake-Analysis\maps\map_' + str(i) + '.html','r').read()

    
    
    #return open('map_'+str(year)+'.html', 'r').read()


app.run_server(port=8050, debug = False)


# In[ ]:





# In[ ]:




