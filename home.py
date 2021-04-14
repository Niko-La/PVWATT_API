#app.py
import PV
import app
import info
import streamlit as st
PAGES = {
    "PV Calculator": app,
    "Project Info": info,
    "PV": PV
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
st.write(str(page))
page.home()