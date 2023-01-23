# Libraries Imports

import datetime
import folium

import pandas               as pd
import numpy                as np
import streamlit            as st
import plotly.express       as px
import matplotlib.pyplot    as plt
import plotly.graph_objects as go

from PIL                    import Image
from haversine              import haversine, Unit
from streamlit_folium       import folium_static

st.set_page_config(page_title='Delivery Person', page_icon=':truck:', layout='wide')

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

def top_deliveries(df1, top_asc):
    """ This function will organize the top fastest or slowest deliveries from the dataset.
        
        If top_asc=True will return the top 10 fastest deliveries and when top_asc=False
        results in the top 10 slowest deliveries.
        
    """
    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
                      .groupby(['City', 'Delivery_person_ID'])
                      .mean()
                      .sort_values(['City', 'Time_taken(min)'], ascending=top_asc).reset_index())
            
    df_top_aux1 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_top_aux2 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_top_aux3 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
            
    df3 = pd.concat([df_top_aux1, df_top_aux2, df_top_aux3]).reset_index(drop=True)
            
    return df3


#--------------------------------------------------------------------CODE STRUCTURE----------------------------------------------------------------------------

# ======================================================================================================
# LOADING DATA
# ======================================================================================================

# Loading Dataset
df = pd.read_csv('data/train.csv')

# Cleaning Data
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
# DELIVERY PERSON TAB
# ======================================================================================================
with st.container():
    st.title('Delivery Person Metrics')

    df_person_metrics = df1.copy()

    col1, col2, col3, col4 = st.columns(4, gap='medium')

    with col1:
        maximum_age = df_person_metrics.loc[:, 'Delivery_person_Age'].max()
        col1.metric('Maximum Age', maximum_age)

    with col2:
        minimum_age = df_person_metrics.loc[:, 'Delivery_person_Age'].min()
        col2.metric('Minimum Age', minimum_age)

    with col3:
        best_condition = df_person_metrics.loc[:, 'Vehicle_condition'].max()
        col3.metric('Best Vehicle Condition', best_condition)

    with col4:
        worst_condition = df_person_metrics.loc[:, 'Vehicle_condition'].min()
        col4.metric('Worst Vehicle Condition', worst_condition)

with st.container():
    st.title('Ratings')

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Avg Ratings by Delivery Person')
        df_delivery_ratings_mean = (df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index())
        st.dataframe(df_delivery_ratings_mean)

    with col2:
        # media por trafego
        st.markdown('### Avg Ratings by Traffic')
        df_ratings_traffic = df1.copy()

        df_ratings_traffic = df_ratings_traffic.loc[:, ['Road_traffic_density', 'Delivery_person_Ratings']].groupby('Road_traffic_density').agg({'Delivery_person_Ratings' : ['mean', 'std']})

        df_ratings_traffic.columns = ['Delivery_rating_mean', 'Delivery_rating_std']
        df_ratings_traffic.reset_index()

        st.dataframe(df_ratings_traffic)

        # media por clima
        st.markdown('### Avg Ratings by Weather')
        df_ratings_weather = df1.copy()

        df_ratings_weather['Weatherconditions'] = df_ratings_weather['Weatherconditions'].str.strip(('conditions '))
        df_ratings_weather = df_ratings_weather.loc[df_ratings_weather['Weatherconditions'] != 'NaN', :]

        df_ratings_weather = df_ratings_weather.loc[:, ['Weatherconditions', 'Delivery_person_Ratings']].groupby('Weatherconditions').agg({'Delivery_person_Ratings' : ['mean', 'std']})
        df_ratings_weather.columns = ['Delivery_rating_mean', 'Delivery_rating_std']
        df_ratings_weather.reset_index()

        st.dataframe(df_ratings_weather)

with st.container():
    st.title('Delivery Time')

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Fastest Deliveries by City')
        df3 = top_deliveries(df1, top_asc=True)
        st.dataframe(df3)


    with col2:
        st.markdown('### Slowest Deliveries by City')
        df3 = top_deliveries(df1, top_asc=False)
        st.dataframe(df3)

