import streamlit as st
from streamlit_option_menu import option_menu
from page.upload_page import show_upload_page
from page.explore_page import show_explore_page
from page.predict_page import show_predict_page

# use CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu('Shaping Our Education In An Innovative Way',
    ['Home', 'Dataset', 'Explore', 'Prediction'], icons=['house', 'cloud-fog2', 'clipboard-data', 'search'], menu_icon="cast", default_index=1)

if selected == "Home":
    st.title("home is where the heart is")
elif selected == "Dataset":
    show_upload_page()
elif selected == "Explore":
    show_explore_page()
elif selected == "Prediction":
    show_predict_page()

