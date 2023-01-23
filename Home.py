import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon=":bar_chart:",
    layout='wide'
)



#image_path = '/home/gabriel/repos/food_delivery_data_visualization/img/'
image = Image.open('logo_food_delivery.png')
st.sidebar.image(image, use_column_width='auto',)

#st.sidebar.markdown

st.write('# Delish Express Company Dashboard')

with st.container():
    st.markdown('## How to use this Dashboard?')
    
    video_path = 'img/tutorialvideo.mp4'
    video_file = open(video_path, 'rb')
    st.video(video_file)
    
with st.container():
    st.markdown("## What's new?")
    st.subheader("You can now view the central regions of the orders!")
    image_path = 'img/map.png'
    image = Image.open(image_path)
    st.image(image)
    
with st.container():
    st.markdown('# Ask for Help \n ## Team of Data Science on Discord\n - @gabrielpastega')
    
