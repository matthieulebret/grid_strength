import streamlit as st

import plotly.express as px

import numpy as np
import pandas as pd
import datetime
import pytz
from pytz import timezone
import time
import calendar
from datetime import date, timedelta
import xlrd
import openpyxl
import xlsxwriter

from geopy.distance import great_circle

from geopy.geocoders import Nominatim


st.set_page_config('System strength',layout='wide')

st.title('System strength lookup')

st.image('https://images.unsplash.com/photo-1554769945-af468c934022?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MzF8fGVsZWN0cmljaXR5JTIwZ3JpZHxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60')


# df = pd.read_csv('layer_2021.txt',skiprows=4,header=None).iloc[:,1:10]
# df.columns=['ID','Station','Year','Modelled System Strength 2020-2021','Percentage 2020-2021','Colour','Geometry','Lat','Lon']
#
# def splitid(item):
#     try:
#         item = str(item).split(': ')[1]
#     except:
#         pass
#     return  item
#
# def splitstation(item):
#     try:
#         item = str(item).split('"STATION": ')[1]
#         item = str(item).replace('"','')
#     except:
#         pass
#     return  item
#
# def splityear(item):
#     try:
#         item = str(item).split('"YEAR": ')[1]
#     except:
#         pass
#     return  item
#
# def splitsyststr(item):
#     try:
#         item = str(item).split('/br>')[1]
#         item = str(item).split('<')[0]
#     except:
#         pass
#     return  item
#
# def splitpct(item):
#     try:
#         item = str(item).split(': ')[1]
#     except:
#         pass
#     return  item
#
# def splitlat(item):
#     try:
#         item = str(item).split('[ ')[1]
#     except:
#         pass
#     return  item
#
# def splitlon(item):
#     try:
#         item = str(item).split(' ]')[0]
#     except:
#         pass
#     return  item
#
#
# df['ID'] = df['ID'].apply(splitid)
# df['Station'] = df['Station'].apply(splitstation)
# df['Year'] = df['Year'].apply(splityear)
# df['Modelled System Strength 2020-2021'] = df['Modelled System Strength 2020-2021'].apply(splitsyststr)
# df['Percentage 2020-2021'] = df['Percentage 2020-2021'].apply(splitpct)
# df['Lat'] = df['Lat'].apply(splitlat)
# df['Lon'] = df['Lon'].apply(splitlon)
#
# df = df[['Station','Modelled System Strength 2020-2021','Percentage 2020-2021','Lat','Lon']]
# # df.set_index('Station',inplace=True)
#
# df1 = df
#
#
#
# ########### 2029-2030
#
# df = pd.read_csv('layer_2930.txt',skiprows=4,header=None).iloc[:,1:10]
# df.columns=['ID','Station','Year','Modelled System Strength 2029-2030','Percentage 2029-2030','Colour','Geometry','Lat','Lon']
#
# df['ID'] = df['ID'].apply(splitid)
# df['Station'] = df['Station'].apply(splitstation)
# df['Year'] = df['Year'].apply(splityear)
# df['Modelled System Strength 2029-2030'] = df['Modelled System Strength 2029-2030'].apply(splitsyststr)
# df['Percentage 2029-2030'] = df['Percentage 2029-2030'].apply(splitpct)
# df['Lat'] = df['Lat'].apply(splitlat)
# df['Lon'] = df['Lon'].apply(splitlon)
#
# df = df[['Station','Modelled System Strength 2029-2030','Percentage 2029-2030','Lat','Lon']]
# # df.set_index('Station',inplace=True)
# df2 = df
#
#
# ########## 2034-2035
#
#
# df = pd.read_csv('layer_3435.txt',skiprows=4,header=None).iloc[:,1:10]
# df.columns=['ID','Station','Year','Modelled System Strength 2034-2035','Percentage 2034-2035','Colour','Geometry','Lat','Lon']
#
#
# df['ID'] = df['ID'].apply(splitid)
# df['Station'] = df['Station'].apply(splitstation)
# df['Year'] = df['Year'].apply(splityear)
# df['Modelled System Strength 2034-2035'] = df['Modelled System Strength 2034-2035'].apply(splitsyststr)
# df['Percentage 2034-2035'] = df['Percentage 2034-2035'].apply(splitpct)
# df['Lat'] = df['Lat'].apply(splitlat)
# df['Lon'] = df['Lon'].apply(splitlon)
#
# df = df[['Station','Modelled System Strength 2034-2035','Percentage 2034-2035','Lat','Lon']]
# # df.set_index('Station',inplace=True)
# df3 = df

##### MERGE #####

# df = pd.merge(df1,df2,on='Station',how='outer')
#
# df = pd.merge(df,df3,on='Station',how='outer')
#
# df

syst = pd.read_excel('system_strength_output.xlsx').iloc[:,1:]


horizlist = ['Modelled System Strength 2020-2021','Modelled System Strength 2029-2030','Modelled System Strength 2034-2035']

for horiz in horizlist:
    syst[horiz] = syst[horiz].apply(lambda x: str(x).split('modelled')[0])


stationlist = syst['Station'].sort_values(ascending=True).unique().tolist()
stationlist.insert(0,'All')

with st.beta_expander('Show grid strength data'):

    selectstation = st.selectbox('Select Station',stationlist,0)

    if selectstation != 'All':
        showdf = syst[syst['Station']==selectstation]
        showdf['Size']=10
        fig = px.scatter_mapbox(showdf,lat='lat',lon='lon',hover_name='Station', hover_data={'Modelled System Strength 2020-2021':True,'Modelled System Strength 2029-2030':True,'Modelled System Strength 2034-2035':True,'Size':False,'lat':False,'lon':False},zoom=3.2,size='Size',center=dict(lat=-30,lon=133),height=600)
        fig.update_layout(mapbox_style='open-street-map',title='System strength in Australia',legend=dict(orientation='h'))
        st.plotly_chart(fig,use_container_width=True)

    else:
        showdf = syst

    belletable = showdf.iloc[:,:7].style.format({'Percentage 2020-2021':'{:,.2f}','Percentage 2029-2030':'{:,.2f}','Percentage 2034-2035':'{:,.2f}'})
    st.write(belletable)

    # belletable = belletable.style.format({'Surface vente':'{:,.2f}',
    # 'Prix / m2 vente':'{:,.2f}',



    syst['Size'] = 10

    selecthoriz = st.selectbox('Select time horizon',horizlist,0)

    showlist = syst[selecthoriz].unique().tolist()
    if selecthoriz == 'Modelled System Strength 2020-2021':
        order = [0,2,3,1,4]
        showlist = [showlist[i] for i in order]
    elif selecthoriz == 'Modelled System Strength 2029-2030':
        order = [0,2,3,1,4]
        showlist = [showlist[i] for i in order]
    else :
        order = [0,3,2,1,4]
        showlist = [showlist[i] for i in order]



    fig = px.scatter_mapbox(syst,lat='lat',lon='lon',hover_name='Station', hover_data={'Modelled System Strength 2020-2021':True,'Modelled System Strength 2029-2030':True,'Modelled System Strength 2034-2035':True,'Size':False,'lat':False,'lon':False},color=selecthoriz,color_discrete_sequence=['green','goldenrod','magenta','red','red'],category_orders={selecthoriz:showlist},zoom=3.2,size='Size',center=dict(lat=-30,lon=133),height=600)
    fig.update_layout(mapbox_style='open-street-map',title='System strength in Australia',legend=dict(orientation='h'))
    st.plotly_chart(fig,use_container_width=True)

    order = ['High ','Neutral ','Poor ','Very poor ','nan']
    # category_orders = {'Modelled System Strength 2020-2021':order,'Modelled System Strength 2029-2030':order,'Modelled System Strength 2034-2035':order}


    fig = px.histogram(syst,x=[horiz for horiz in horizlist],barmode='group')
    fig.update_layout(title='System strength in Australia',showlegend=True,legend=dict(orientation='h'))
    fig.update_xaxes(categoryorder='array',categoryarray=order)
    st.plotly_chart(fig,use_container_width=True)



####################################
##### Find closest station #########
####################################

st.header('Check grid strength for a certain location')

choice = st.radio('Location search mode',['Text search','Latitude Longitude'],0)

placeholder = st.empty()

if choice == 'Text search':
    geolocator = Nominatim(user_agent='latlong.py')
    st.markdown('')

    farm = st.text_input('Please enter the name of the place you are looking for (recommend format: Karadoc, Australia):','Karadoc, Australia')

    def getlatlon(place):
        try:
            location = geolocator.geocode(place)
            return (location.latitude,location.longitude)
        except:
            return ('N/A','N/A')

    if getlatlon(farm)[0] == 'N/A':
        placeholder = st.write('Wrong location, please enter a new location or select Location search mode = Latitude Longitude')
        st.stop()

    latitude = getlatlon(farm)[0]
    longitude = getlatlon(farm)[1]

    # if latitude or longitude == 'N/A'


elif choice == 'Latitude Longitude':
    latitude = st.number_input('Latitude',value=-24.2131906)
    longitude = st.number_input('Longitude',value=151.5789714)




station_to_find = {'lat':latitude,'lon':longitude}


distlist = []
nearlist = []
strengthlist = []

for horiz in horizlist:

    syst = syst[syst[horiz]!='nan']

    stationdict=dict()
    i=0
    for station in syst['Station'].tolist():
        stationdict[station] = {'lat':syst['lat'].tolist()[i],'lon':syst['lon'].tolist()[i]}
        i=i+1

    stationlist = [station for station in stationdict]

    # List of lat lon:
    latlonlist = list(stationdict.values())
    project = (station_to_find['lat'],station_to_find['lon'])

    distancelist = []
    for item in latlonlist:
        station = (item['lat'],item['lon'])
        distancelist.append(great_circle(station,project).km)

    distance = min(distancelist)
    newdist = '{:,.2f}'.format(distance)
    distlist.append(newdist)

    stationnear = stationlist[distancelist.index(min(distancelist))]
    nearlist.append(stationnear)

    strength = syst[syst['Station']==stationnear][horiz].iloc[0]
    strengthlist.append(strength)


df = pd.DataFrame([distlist,nearlist,strengthlist])
df.columns = ['2020-2021','2029-2030','2034-2035']
df.index = ['Distance in km','Nearest station','System strength']

st.table(df)

loclook = [station_to_find['lat'],station_to_find['lon']]
station = [syst[syst['Station']==stationnear]['lat'].iloc[0],syst[syst['Station']==stationnear]['lon'].iloc[0]]

mapdf = pd.DataFrame([loclook,station])
mapdf.index=['Location',stationnear]
mapdf.reset_index(inplace=True)
mapdf.columns=['Location','lat','lon']
mapdf['Size']=20

fig = px.scatter_mapbox(mapdf,lat='lat',lon='lon',hover_name='Location', color='Location',zoom=8,size='Size',center=dict(lat=mapdf['lat'].iloc[0],lon=mapdf['lon'].iloc[0]),height=600)
fig.update_layout(mapbox_style='open-street-map',title='Map of selected area',legend=dict(orientation='h'))
st.plotly_chart(fig,use_container_width=True)


####################################
##### Load all projects ############
####################################

st.header('Check grid strength for a certain project')

pj = pd.read_excel('DUID_Project_List.xlsx',sheet_name="Operational_pj")
projectlist = pj['Station Name'].sort_values(ascending=True).unique().tolist()

projectlist.insert(0,'All')

selectproject = st.selectbox('Select Project',projectlist,0)

if selectproject != 'All':
    showdf = pj[pj['Station Name']==selectproject]
else:
    showdf = pj


showdf['Size'] = 1

# fig = px.scatter_mapbox(showdf,lat='lat',lon='lon',hover_name='Station Name', hover_data=['Station Name','lat','lon'],size='Size',zoom=3.2,center=dict(lat=-30,lon=133),height=600)
# fig.update_layout(mapbox_style='open-street-map',title='Projects in Australia')
# st.plotly_chart(fig,use_container_width=True)


places = []
for station in stationlist:
    if ' Solar' in station:
        station = station.split('Solar')[0]
    if ' Wind' in station:
        station = station.split('Wind')[0]
    places.append(station)

places = pd.DataFrame(places)
places.columns = ['Place']


####################################
##### Find closest station #########
####################################


if selectproject != 'All':

    subheadertext = 'Project location on the grid: '+selectproject

    st.subheader(subheadertext)

    latitude = showdf[showdf['Station Name']==selectproject]['lat'].iloc[0]
    longitude = showdf[showdf['Station Name']==selectproject]['lon'].iloc[0]

    station_to_find = {'lat':latitude,'lon':longitude}

############### Nearest station

    distlist = []
    nearlist = []
    strengthlist = []

    for horiz in horizlist:

        syst = syst[syst[horiz]!='nan']

        stationdict=dict()
        i=0
        for station in syst['Station'].tolist():
            stationdict[station] = {'lat':syst['lat'].tolist()[i],'lon':syst['lon'].tolist()[i]}
            i=i+1

        stationlist = [station for station in stationdict]

        # List of lat lon:
        latlonlist = list(stationdict.values())
        project = (station_to_find['lat'],station_to_find['lon'])

        distancelist = []
        for item in latlonlist:
            station = (item['lat'],item['lon'])
            distancelist.append(great_circle(station,project).km)
        distance = min(distancelist)
        newdist = '{:,.2f}'.format(distance)
        distlist.append(newdist)

        stationnear = stationlist[distancelist.index(min(distancelist))]
        nearlist.append(stationnear)

        strength = syst[syst['Station']==stationnear][horiz].iloc[0]
        strengthlist.append(strength)


    df = pd.DataFrame([distlist,nearlist,strengthlist])
    df.columns = ['2020-2021','2029-2030','2034-2035']
    df.index = ['Distance in km','Nearest station','System strength']

    st.table(df)

    markdowntext = 'Nearby projects sharing the same station: '+stationnear
    st.markdown(markdowntext)

    pj = pd.read_csv('project_syst_strength.csv').iloc[:,1:]
    neardf = pj[(pj['Nearest Station 2020-2021']==stationnear)&(pj['Station Name']!=selectproject)]
    neardf

    loclook = [station_to_find['lat'],station_to_find['lon']]
    station = [syst[syst['Station']==stationnear]['lat'].iloc[0],syst[syst['Station']==stationnear]['lon'].iloc[0]]

    neardf = neardf[['Station Name','lat','lon']]
    neardf.columns = ['Location','lat','lon']


    mapdf = pd.DataFrame([loclook,station])
    mapdf.index=[selectproject,stationnear]
    mapdf.reset_index(inplace=True)
    mapdf.columns=['Location','lat','lon']
    mapdf = pd.concat([mapdf,neardf])
    mapdf['Size']=20

    fig = px.scatter_mapbox(mapdf,lat='lat',lon='lon',hover_name='Location', color='Location',zoom=7,size='Size',center=dict(lat=mapdf['lat'].iloc[0],lon=mapdf['lon'].iloc[0]),height=600)
    fig.update_layout(mapbox_style='open-street-map',title='Map of selected area',legend=dict(orientation='h'))
    st.plotly_chart(fig,use_container_width=True)



#
# def getlatlon(project):
#     lat = pj[pj['Station Name']==project]['lat'].iloc[0]
#     lon = pj[pj['Station Name']==project]['lon'].iloc[0]
#     return (lat,lon)
#
# def getdistance(farm):
#     project = getlatlon(farm)
#     distancelist = []
#     for item in latlonlist:
#         station = (item['lat'],item['lon'])
#         distancelist.append(great_circle(station,project).km)
#     distance = min(distancelist)
#     return '{:,.2f}'.format(distance)
#
# def getnearest(farm):
#     project = getlatlon(farm)
#     distancelist = []
#     for item in latlonlist:
#         station = (item['lat'],item['lon'])
#         distancelist.append(great_circle(station,project).km)
#     return stationlist[distancelist.index(min(distancelist))]
#
# def getstrength(farm):
#     stationnear = getnearest(farm)
#     return syst[syst['Station']==stationnear][horiz].iloc[0]
#
# for horiz in horizlist:
#
#     syst = syst[syst[horiz]!='nan']
#
#     stationdict=dict()
#     i=0
#     for station in syst['Station'].tolist():
#         stationdict[station] = {'lat':syst['lat'].tolist()[i],'lon':syst['lon'].tolist()[i]}
#         i=i+1
#
#     stationlist = [station for station in stationdict]
#
#     # List of lat lon:
#     latlonlist = list(stationdict.values())
#
#     pj['Distance to Station '+horiz.replace('Modelled System Strength ','')] = pj['Station Name'].apply(getdistance)
#     pj['Nearest Station '+horiz.replace('Modelled System Strength ','')] = pj['Station Name'].apply(getnearest)
#     pj['Modelled System Strength '+horiz.replace('Modelled System Strength ','')] = pj['Station Name'].apply(getstrength)
#
#
# pj.to_csv('project_syst_strength.csv')

st.header('Check grid strength for all projects')

pj = pd.read_csv('project_syst_strength.csv').iloc[:,1:]

pj['Size']=5

selecthoriz = st.selectbox('Select time horizon',horizlist,0,key=1)

showlist = pj[selecthoriz].unique().tolist()
if selecthoriz == 'Modelled System Strength 2020-2021':
    order = [1,3,2,0]
    showlist = [showlist[i] for i in order]
elif selecthoriz == 'Modelled System Strength 2029-2030':
    order = [2,3,1,0]
    showlist = [showlist[i] for i in order]
else :
    order = [1,3,2,0]
    showlist = [showlist[i] for i in order]


fig = px.scatter_mapbox(pj,lat='lat',lon='lon',hover_name='Station Name', hover_data={'Modelled System Strength 2020-2021':True,'Modelled System Strength 2029-2030':True,'Modelled System Strength 2034-2035':True,'Size':False,'lat':False,'lon':False},color=selecthoriz,color_discrete_sequence=['green','goldenrod','magenta','red'],category_orders={selecthoriz:showlist},zoom=3.2,size='Size',center=dict(lat=-30,lon=133),height=600)
fig.update_layout(mapbox_style='open-street-map',title='System strength in Australia - view by project',legend=dict(orientation='h'))
st.plotly_chart(fig,use_container_width=True)

order = ['High','Neutral','Poor','Very poor']


fig = px.histogram(pj,x=[horiz for horiz in horizlist],barmode = 'group')
fig.update_layout(title='System strength by project in Australia',showlegend=True,legend=dict(orientation='h'))
fig.update_xaxes(categoryorder='array',categoryarray=order)
st.plotly_chart(fig,use_container_width=True)

    # fig = px.histogram(syst,x=[horiz for horiz in horizlist],barmode='group',color_discrete_sequence=['green','goldenrod','magenta','red','red'],category_orders={selecthoriz:showlist})
    # fig.update_layout(title='System strength in Australia',showlegend=True,legend=dict(orientation='h'))
    # st.plotly_chart(fig,use_container_width=True)

with st.beta_expander('Show data'):

    col1,col2,col3 = st.beta_columns(3)
    strength2021 = ['All','High','Neutral','Poor','Very poor']
    strength2930 = ['All','High','Neutral','Poor','Very poor']
    strength3435 = ['All','High','Neutral','Poor','Very poor']

    with col1:
        select1 = st.selectbox('System strength 2020-2021',strength2021,0)
        if select1 != 'All':
            pj = pj[pj['Modelled System Strength 2020-2021']==select1]
    with col2:
        select2 = st.selectbox('System strength 2029-2030',strength2930,0)
        if select2 != 'All':
            pj = pj[pj['Modelled System Strength 2029-2030']==select2]
    with col3:
        select3 = st.selectbox('System strength 2034-2035',strength3435,0)
        if select3 != 'All':
            pj = pj[pj['Modelled System Strength 2034-2035']==select3]

    collist = [1,2,21,22,23,24,25,26,27,28,29]

    pj = pj.iloc[:,collist]
    pj
