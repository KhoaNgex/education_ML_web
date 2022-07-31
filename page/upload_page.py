import os
import os.path
import streamlit as st
import pandas as pd 

def save_uploadedfile(uploadedfile):
    dirname = os.path.dirname(__file__)
    data_dir = os.path.join(dirname, '../data')
    with open(os.path.join(data_dir,"dataset.csv"),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File: {} to data Dir".format(uploadedfile.name))

def show_upload_page():
    st.subheader("Dataset")
    data_file = st.file_uploader("Upload CSV",type=['csv'])
    if st.button("Process"):
        if data_file is not None:
            file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
            st.write(file_details)
            df = pd.read_csv(data_file)
            st.dataframe(df)
            save_uploadedfile(data_file)