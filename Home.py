import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🚚",
    layout='wide'
)



#image_path = '/home/gabriel/repos/food_delivery_data_visualization/img/'
image = Image.open('logo_food_delivery.png')
st.sidebar.image(image, width=150)

#st.sidebar.markdown

st.write("# Food Delivery Overview Dashboard")

#st.markdown("""