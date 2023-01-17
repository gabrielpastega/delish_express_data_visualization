# ======================================================================================================
# Libraries Imports
# ======================================================================================================

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

st.set_page_config(page_title='Restaurants', page_icon=':knife_fork_plate:', layout='wide')

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

def delivery_distance(df1, fig):
    if fig == False:
        cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
        df1['Distance_delivery'] = df1.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                                                 (x['Delivery_location_latitude'], x['Delivery_location_longitude']), unit='km'), axis=1)
        df1 = df1.loc[df1['Distance_delivery'] < 100, :]
        avg_distance = np.round(df1['Distance_delivery'].mean(), 2)

        return avg_distance
    
    else:
        cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
        df1['Distance_delivery'] = df1.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                                                 (x['Delivery_location_latitude'], x['Delivery_location_longitude']), unit='km'), axis=1) 
        df1 = df1.loc[df1['Distance_delivery'] < 100, :]
        avg_distance = df1.loc[:, ['City', 'Distance_delivery']].groupby('City').mean().reset_index()

        fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['Distance_delivery'], pull=[0, 0.05, 0])])
        
        return fig
    
def festival_time_delivery_avg_std(df1, festival, op):
    """
        Calculates the average and standard deviation of the delivery time in case there is a festival.
                    
        Parameters
        ----------
            Input:
                df1: Dataframe with the data necessary

                festival:str {'Yes', 'No'}
                    'Yes': if there is a festival.
                    'No': if there is no festival.

                op: str {'avg_time', 'std_time'}
                    'avg_time': calculates the average delivery time
                    'std_time': calculates the standard deviation of the delivery time

            Output:
                df_festival: Dataframe with 2 columns and 1 row with the results
                    
    """
    df_festival = df1.loc[:, ['Festival', 'Time_taken(min)']].groupby('Festival').agg({'Time_taken(min)':['mean', 'std']}).reset_index()
    df_festival.columns = ['Festival', 'avg_time', 'std_time']
    df_festival = np.round(df_festival.loc[df_festival['Festival'] == festival, op], 2)
                
    return df_festival


def delivery_city_avg_std(df1):
    df_delivery_city = df1.loc[:, ['City', 'Time_taken(min)']].groupby('City').agg({'Time_taken(min)':['mean', 'std']})
    df_delivery_city.columns = ['avg_time', 'std_time']
    df_delivery_city = df_delivery_city.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Delivery Time', x=df_delivery_city['City'], y=df_delivery_city['avg_time'], 
                                     error_y=dict(type='data', array=df_delivery_city['std_time'])))

    fig.update_layout(barmode='group')
            
    return fig
            
def delivery_city_traffic_avg_std(df1):
    df_delivery_city_traffic = (df1.loc[:, ['Time_taken(min)', 'City', 'Road_traffic_density']]
                                   .groupby(['City', 'Road_traffic_density'])
                                   .agg({'Time_taken(min)':['mean', 'std']}).reset_index())

    df_delivery_city_traffic.columns = ['City', 'Road_traffic_density', 'avg_time', 'std_time']

    df_delivery_city_traffic = df_delivery_city_traffic.reset_index()
    fig = px.sunburst(df_delivery_city_traffic, path=['City', 'Road_traffic_density'], values='avg_time', 
                                  color='std_time', color_continuous_scale='RdBu', 
                                  color_continuous_midpoint=np.average(df_delivery_city_traffic['std_time']))
    return fig
    
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

st.header('FOOD DELIVERY OVERVIEW')

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
# RESTAURANTS TAB
# ======================================================================================================

with st.container():
    st.title('Time and Distance Metrics')

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    st.markdown("""----""")

    with col1:
        deliveryperson_unique = len(df1['Delivery_person_ID'].unique())
        col1.metric('Unique Deliverers', deliveryperson_unique)

    with col2:
        avg_distance = delivery_distance(df1, fig=False)
        col2.metric('Avg Distance KM', avg_distance)

    with col3:

        df_festival = festival_time_delivery_avg_std(df1, 'Yes', 'avg_time')      
        col3.metric('Festival Avg Time', df_festival)

    with col4:

        df_festival = festival_time_delivery_avg_std(df1, 'Yes', 'std_time')
        col4.metric('Festival Std Time', df_festival)

    with col5:        

        df_festival = festival_time_delivery_avg_std(df1, 'No', 'avg_time')
        col5.metric('Delivery Avg Time', df_festival)

    with col6:                    

        df_festival = festival_time_delivery_avg_std(df1, 'No', 'std_time')
        col6.metric('Delivery Std Time', df_festival)

with st.container():

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('###### Avg Delivery Time by City')

        fig = delivery_city_avg_std(df1)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('###### Avg Delivery Time - City & Order Type')

        df_delivery_city_order = df1.loc[:, ['Time_taken(min)', 'City', 'Type_of_order']].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)':['mean', 'std']}).reset_index()
        df_delivery_city_order.columns = ['City', 'Type_of_order', 'Time_taken_mean', 'Time_taken_std']
        df_delivery_city_order = df_delivery_city_order.reset_index()

        st.dataframe(df_delivery_city_order)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('###### Avg delivery distance by City')

        fig = delivery_distance(df1, fig=True)
        st.plotly_chart(fig, use_container_width=True)


    with col2:
        st.markdown('###### Avg Delivery Time by City and Traffic')

        fig = delivery_city_traffic_avg_std(df1)
        st.plotly_chart(fig, use_container_width=True)
