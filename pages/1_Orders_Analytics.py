# Libraries Imports
import datetime
import folium

import pandas               as pd
import numpy                as np
import streamlit            as st
import plotly.express       as px
import matplotlib.pyplot    as plt
import plotly.graph_objects as go

from PIL              import Image
from haversine        import haversine, Unit
from streamlit_folium import folium_static

st.set_page_config(page_title='Orders', page_icon=':heavy_dollar_sign:', layout='wide')

# ======================================================================================================
# FUNCTIONS
# ======================================================================================================

def clean_dataframe(df1):
    """ This function is responsible for cleaning the dataframe
        
        Actions executed:
        1. NaN data removed
        2. Data types conversion
        3. Blank spaces removed
        4. Creates a day and week of year columns
        5. Cleans text on the Time_taken(min) column
        
        Input: Dataframe
        Output: Dataframe
    
    """
    # removing NA
    df1 = df1.loc[(df1['Delivery_person_Age'] != 'NaN '), :]
    df1 = df1.loc[(df1['City'] != 'NaN '), :]
    df1 = df1.loc[(df1['Road_traffic_density'] != 'NaN '), :]
    df1 = df1.loc[(df1['Festival'] != 'NaN '), :]
    df1 = df1.loc[(df1['multiple_deliveries'] != 'NaN '), :]
    df1 = df1.loc[(df1['Time_Orderd'] != 'NaN '), :]
    
    # data types conversion
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    
    # removing blank spaces
    # columns - ID, Road_traffic_density, Type_of_order, Type_of_vehicle, City, Festival
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    # time taken column
    df1['Time_taken(min)'] = df1['Time_taken(min)'].str.strip(('(min) ')).astype(int)
    
    # creating the day and week of year columns
    df1['Order_Date_Day'] = df1.Order_Date.dt.day.astype(int)
    df1['Week_Of_Year'] = df1.Order_Date.dt.isocalendar().week.astype(int)
    
    return df1

def orders_day_metric(df1):
    df1 = df1.loc[:, ['ID', 'Order_Date_Day']].groupby('Order_Date_Day').count().reset_index()
    fig = px.bar(df1, x='Order_Date_Day', y='ID');
                        
    return fig

def traffic_orders_share(df1):
    df1 = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    df1['delivery_perc'] = df1['ID'] / df1['ID'].sum()
    
    fig = px.pie(df1, values='delivery_perc', names='Road_traffic_density')

    return fig

def order_city_traffic(df1):
    df1 = df1.loc[:,['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
    fig = px.scatter(df1, x='City', y='Road_traffic_density', size='ID', color='City')
                
    return fig
        
def orders_by_week(df1):
    df1 = df1.loc[:, ['ID', 'Week_Of_Year']].groupby('Week_Of_Year').count().reset_index()
    fig = px.bar(df1, x='Week_Of_Year', y='ID')
            
    return fig
        
        
def orders_driver_weekly(df1):
    df_aux1 = df1.loc[:, ['ID', 'Week_Of_Year']].groupby('Week_Of_Year').count().reset_index()
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'Week_Of_Year']].groupby('Week_Of_Year').nunique().reset_index()

    df1 = pd.merge(df_aux1, df_aux2, how='inner')
    df1['Orders_By_Delivery_Person_Weekly'] = df1['ID'] / df1['Delivery_person_ID']

    fig = px.line(df1, x='Week_Of_Year', y='Orders_By_Delivery_Person_Weekly')

    return fig

def orders_central_region_map(df1):
    df1 = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()

    mapa = folium.Map(location=[19.552911,76.902847], zoom_start=7)
    
    for index, location_info in df1.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']], location_info['City']).add_to(mapa)
    
    folium_static(mapa, width=1400, height=600)

    return None

#--------------------------------------------------------------------CODE STRUCTURE----------------------------------------------------------------------------

# ======================================================================================================
# LOADING DATA
# ======================================================================================================

# Loading Dataset
df = pd.read_csv('data/train.csv')

# cleaning the data
df1 = clean_dataframe(df)

# ======================================================================================================
# SIDEBAR
# ======================================================================================================

st.header('Delish Express Company Dashboard')

#image_path = '/home/gabriel/repos/food_delivery_data_visualization/img/'
image = Image.open('logo_food_delivery.png')
st.sidebar.image(image, width=150)

st.sidebar.markdown('# MENU')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Select the date')
date_slider = st.sidebar.slider('Limit date',
                  value=pd.datetime(2022, 4, 6),
                  min_value=pd.datetime(2022, 2, 11),
                  max_value=pd.datetime(2022, 4, 6),
                  format='DD-MM-YYYY')
st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect('Traffic conditions', ['Low', 'Medium', 'High', 'Jam'], default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""---""")

# DATE FILTER
rows_selected = (df1['Order_Date'] < date_slider)
df1 = df1.loc[rows_selected, :]

# TRAFFIC FILTER
rows_selected = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[rows_selected, :]

# ======================================================================================================
# ORDERS TAB
# ======================================================================================================
with st.container():
    # Orders Metric
    st.markdown('# Orders by Day')
    fig = orders_day_metric(df1)
    st.plotly_chart(fig, use_container_width=True)       

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('# Orders distribution by Traffic Type')
        fig = traffic_orders_share(df1)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('# Comparison of the orders by city and traffic type')
        fig = order_city_traffic(df1)
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown('# Orders by Week')
    fig = orders_by_week(df1)
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown('# Weekly Orders by Delivery Person')
    fig = orders_driver_weekly(df1)
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown('# Orders Central Region')
    orders_central_region_map(df1)
