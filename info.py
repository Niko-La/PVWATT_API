import streamlit as st

def info():
    st.write("INFO")
    lat, long = st.beta_columns(2)
    cap, tilt = st.beta_columns(2)

    lat.text_input('Lat:') 
    long.text_input('Long:')

    cap.text_input('System Capacity:', '1')

    first, id = st.beta_columns([2,1])

    first.text_input("Reviewer Name")
    id.text_input("Solar Review #")



info()