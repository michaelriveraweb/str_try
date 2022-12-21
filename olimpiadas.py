import pandas as pd
import plotly.io as pio
import plotly.express as px
import streamlit as st
import numpy as np
from datetime import datetime,timedelta
import plotly.graph_objs as go

df_og = pd.read_csv('olimpics_records.csv')
hombres = df_og.drop(df_og.loc[df_og['Event']=="100 m hurdles"].index)
mujeres = df_og.drop(df_og.loc[df_og['Event']=="110 m hurdles"].index)

#------------------------------------------------------------
def get_event(df,event,gender):
    df = df.loc[df['Event'] == event]
    df = df.loc[df['genero'] == gender]
    return df

#------------------------------------------------------------

st.set_page_config(page_title="Olympics World Records by Country",
                    layout="wide",
                    initial_sidebar_state="expanded")

px.set_mapbox_access_token(open('./mapbox_token').read())
st.title("Olympics World Records by Country")

with st.sidebar:
    original_title = '<p style="color:red;">Type of Visualization</p>'
    st.markdown(original_title,unsafe_allow_html=True)
visualizacion = st.sidebar.selectbox("",options=['Scatterplot','Choropleth','Treemap'],
                            index=0,format_func=str)    
#------------------------------------------------------------
with st.sidebar:
    original_title = '<p style="color:red;">Gender</p>'
    st.markdown(original_title,unsafe_allow_html=True)
genero = st.sidebar.selectbox("",options=['Male','Female'],
                            index=0,format_func=str)
#------------------------------------------------------------
with st.sidebar:
    original_title = '<p style="color:red;">Event</p>'
    st.markdown(original_title,unsafe_allow_html=True)
#------------------------------------------------------------
if genero == "Male":
    evento = st.sidebar.selectbox("",options=list(sorted(hombres['Event'].unique())),
                                index=0,format_func=str)
else:
    evento = st.sidebar.selectbox("",options=list(sorted(mujeres['Event'].unique())),
                                index=0,format_func=str)
#------------------------------------------------------------
df = get_event(df_og,evento,genero)

menorTiempo = ["100 m", "200 m", "300 m", "400 m", "800 m", "1500 m", "3000 m", "5000 m",
                "1000 m", "2000 m", "10000 m", "Half marathon", "Marathon", "Mile",
                "110 m hurdles", "400 m hurdles", "100 m hurdles", "3000 m steeplechase",
                "4 × 100 m relay", "4 × 400 m relay"]

color_palet = "Hot_r"

if evento in menorTiempo:
    # ascending = True
    z = df["Records"]
    recordMin = z.min()
    size = 'menor'
    
    
else:
    # ascending = False
    z = df["Records"]
    recordMin = z.max()
    size = ''

#------------------------------------------------------------
if visualizacion == 'Scatterplot':
    st.write('<b>You are currently seeing a Scatterplot where the best' \
             'performing countries hava a darker and bigger:</b>', unsafe_allow_html=True)
        
        

    # mayorDistancia = ["High jump", "Pole vault", "Long jump", "Triple jump", "Shot put",
    #                   "Discus throw", "Hammer throw", "Javelin throw"]

        
    # z = df["Records_2"]
    # recordMin = z.min()

    pais = df.loc[df['Records'] == recordMin]
    latRecordMin = pais["latitude"].iloc[0]
    lonRecordMin = pais["longitude"].iloc[0]
    
    if size == 'menor':
        df['Records_3'] = 1.001**(df['Records'].max() - df['Records'])
        #df['Records_3'] = (df['Records_3'] - df['Records_3'].min())/(df['Records_3'].max() - df['Records_3'].min())       
    else:
        df['Records_3'] = 1.001**(df['Records'])
    
    fig = px.scatter_mapbox(df,
                            lat="latitude",
                            lon= "longitude",
                            color= "Records_3",hover_name='Athlete',
                            # center = dict(lat = 0,lon = 0),
                            size= 'Records_3',
                            hover_data = {'Records':False,'Record':True,'Country':True,
                                          'latitude':False, 'longitude':False
                                          ,'Records_3':False},
                            color_continuous_scale= color_palet,
                            #mapbox_style='white-bg',
                            zoom= 5,
                            center=dict(lat=latRecordMin, lon=lonRecordMin)
                            )
    fig.update_layout(
        coloraxis_colorbar=dict(
        title="",
        thicknessmode="pixels",
        lenmode="pixels",
        yanchor="top",y=1,
        #ticks="outside",
        tickvals=[0,4,8,12],
        ticktext=["", "", "", ""],
        dtick=4
))
    fig.update_layout(width=1000, height=700)
    # # plot_map = st.sidebar.checkbox('Mostrar mapa',value = True)
    # st.sidebar.write('\n\nAplicación desarrollada por:<p><u> Michael J. Rivera Lazú</p></u> <p><u> Alexandra Rosario Santana </p></u><p><i>CDAT-3001</i></p> <p><i>Departamento de Matemáticas</i></p> <p><i>Universidad de Puerto Rico en Humacao</i></p>',unsafe_allow_html=True)
    # st.sidebar.markdown("<hr style=margin:2px>", unsafe_allow_html=True)
    st.plotly_chart(fig)

elif visualizacion == 'Choropleth':
    st.write('<b>You are currently seeing a Choropleth world map where the darker' \
             'the color of the countrie, the better the record:</b>', 
             unsafe_allow_html=True)
        
        

    if size == 'menor':
        df['Records_3'] = 1.001**(df['Records'].max() - df['Records'])
        #df['Records_3'] = (df['Records_3'] - df['Records_3'].min())/(df['Records_3'].max() - df['Records_3'].min())       
    else:
        df['Records_3'] = 1.001**(df['Records'])
        
    fig = px.choropleth(df, locations="Alpha-3 code",
                    color="Records_3", # lifeExp is a column of gapminder
                    hover_name="Athlete", # column to add to hover information
                    color_continuous_scale=color_palet,
                    #range_color = [0,1],
                    hover_data = {'Records':False,'Record':True,'Country':True,
                                          'latitude':False, 'longitude':False
                                          ,'Records_3':False,'Alpha-3 code':False})
    fig.update_layout(
        coloraxis_colorbar=dict(
    title="",
    thicknessmode="pixels",
    lenmode="pixels",
    yanchor="top",y=1,
    #ticks="outside",
    tickvals=[0,4,8,12],
    ticktext=["", "", "", ""],
    dtick=4
    ))b
    
    st.plotly_chart(fig, use_container_width=True)
    # pio.renderers.default = "browser"
    
elif visualizacion == "Treemap":
    st.write('<b>You are currently seeing a Tree map where the best' \
             'performing countries hava a darker color:</b>', unsafe_allow_html=True)
        
        
    if size == 'menor':
        df['Records_3'] = 1.001**(df['Records'].max() - df['Records'])
        #df['Records_3'] = (df['Records_3'] - df['Records_3'].min())/(df['Records_3'].max() - df['Records_3'].min())       
    else:
        df['Records_3'] = 1.001**(df['Records'])
    fig = px.treemap(df, path=[px.Constant(evento), 'Continent', 'Country'], 
                     values='Records_3',
                  color='Records_3',  hover_data=['Athlete'],
                  # hoverinfo =[]
                  # {'Records':False,'Record':True,'Country':True,
                  #                         'latitude':False, 'longitude':False,
                  #                         'Records_3':False,'Alpha-3 code':False
                  #                         #'Records_3_sum':False,'Records_3':False
                  #                         },
                  color_continuous_scale=color_palet,
                  color_continuous_midpoint=np.average(df['Records_3'],
                                                        weights=df['Records_3']))
    fig.update_layout(
        coloraxis_colorbar=dict(
        title="",
        thicknessmode="pixels",
        lenmode="pixels",
        yanchor="top",y=1,
        #ticks="outside",
        tickvals=[0,4,8,12],
        ticktext=["", "", "", ""],
        dtick=4
        ))
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig)
    
    
#------------------------------------------------------------   
st.sidebar.write('\n\nApplication developed by:<p><u> Michael J. Rivera Lazú</p></u> <p><u> Alexandra Rosario Santana </p></u><p><i>CDAT-3001</i></p> <p><i>Departament of Mathematics</i></p> <p><i>University of Puerto Rico in Humacao</i></p>',unsafe_allow_html=True)
st.sidebar.markdown("<hr style=margin:2px>", unsafe_allow_html=True)

