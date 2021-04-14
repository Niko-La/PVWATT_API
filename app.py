import streamlit as st
import numpy as np
import pandas as pd
import datetime
from datetime import datetime, date, time

import json
import requests

#import geopy
#from geopy.geocoders import Nominatim
#from geopy.extra.rate_limiter import RateLimiter

st.set_page_config(page_title="Solar PV Audit",page_icon="🧊",layout="wide",initial_sidebar_state="collapsed",)


st.write("""
    # PV SOLAR AUDIT PROGAM
    a tool for efficient deployment & verification of ON-SITE ENERGY installation

    > **Demo Project:** 
    > ☝Before moving on with this notebook you might want to take a look at:
    > - 📗[Robotic process automation](https://en.wikipedia.org/wiki/Robotic_process_automation)
    > - ⚙️[Computational Engineering](https://en.wikipedia.org/wiki/Computational_engineering)
    
    
    TODO PV ANALYSIS USE 2 Calculation, ignore 1
    """)


def info():
    st.header("1. Enter Project Info")

    first, id = st.beta_columns([2,1])

    first.text_input("Reviewer Name")
    id.text_input("Solar Review #")

    user_input = st.text_area("Customer", "Paste Info ")

    st.write(user_input)

    df = pd.DataFrame(np.random.randn(5, 2), columns=('col %d' % i for i in range(2)))
    st.dataframe(df)

    #lat, lon = 46.2437, 6.0251



def app():

    st.sidebar.title("Facility Location")

    street = st.sidebar.text_input("Street", "75 Bay Street")
    city = st.sidebar.text_input("City", "Calgary")
    province = st.sidebar.text_input("Province", "Alberta")
    country = st.sidebar.text_input("Country", "Canada")

    #geolocator = Nominatim(user_agent="GTA Lookup")
    #geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    #location = geolocator.geocode(street+", "+city+", "+province+", "+country)

    lat_project = 44
    lon_project = 120

    st.sidebar.write("LAT: " +  str(round(lat_project,2)))
    st.sidebar.write("LONG: " + str(round(lon_project,2)))
    #map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})

    #st.map(map_data) 




    reviewer , application_id = st.beta_columns(2)

    reviewer.selectbox("Reviewer", ["Kava", "Jenan", "David"])
    application_id.text_input("Application Id", "ESD-XXXXX")

    # datetime object containing current date and time
    now = datetime.now()
    
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)	

    d2 = now.strftime("%B %d, %Y")
    st.write(dt_string)


    st.header("1.Project & Location")
    st.write("""
    Enter project dates and address and verify it is durng the program windo and located in Alberta 

    """)

    #address = st.sidebar.text_input("Project location", "2390 47 Ave SW, Calgary, AB T2T 5W5")

    d1,d2,d3 = st.beta_columns(3)

    start = d1.date_input('project start date')
    end = d2.date_input('project end date')
    submit = d3.date_input('application received')
    
    if start > end:
        st.write("IR: project starting after end date")
        st.write(start.month+1)
    if end > start:
        st.write("Project Dates Approved")
    if end.year >= (start.year+1):
        st.write("PProject too long")
    st.text("Check that the start date is acceptable (If between Nov 2 and Jan 31, Application Submission date must be before Feb 28, otherwise any date after Feb 1 is fine)")

    AC_TOTAL = 0 

    st.header("2.Energy Calculation")
    st.write("""
    Verify Project is withing scope and calculate that Energy production is withing project requirments
    """)

    latitude, longitude, capacity, tilt_num, azm_num, losses_num = st.beta_columns(6)
    lat = latitude.text_input('Lat:', '49') 
    long = longitude.text_input('Long:', '-112')
    cap = capacity.text_input('System DC Size (kW):', '1') 
    
    tilt = tilt_num.text_input('Tilt:', '0') 
    azm = azm_num.text_input('Azimuth:', '180') 
    losses = losses_num.text_input('Losses:', '20')

    mod_t_num , array_t_num = st.beta_columns(2)
    cust_num, Panel_num = st.beta_columns(2)
    
    #mod_t = st.selectbox('Module Type: 0 Standard   ||  1 Premium   ||  2 Thin film', ('0','1','2'))
    mod_t = mod_t_num.selectbox('Module Type: 0 Standard   ||  1 Premium   ||  2 Thin film', ('0', '1', '2', '3'))

    array_t = array_t_num.selectbox('Array Type:  0	Fixed - Open Rack || 1	Fixed - Roof Mounted || 2	1-Axis || 3	1-Axis Backtracking || 4 2-Axis', ('0', '1', '2', '3', '4'))
     

    cust = cust_num.text_input('application ac annual (kWh):', '0')
    Panel = Panel_num.text_input('Panel Size (kW):', '1')


    #Sif long:
        #st.write(lat)

    # importing the requests library 
    # api-endpoint 
    URL = "https://developer.nrel.gov/api/pvwatts/v6.json?api_key=DEMO_KEY&lat=40&lon=-115&system_capacity=1&azimuth=180&tilt=40&array_type=1&module_type=1&losses=10"
    api = "https://developer.nrel.gov/api/pvwatts/v6.json"

    #PARAMS
    PARAMS = {
        'api_key':'qKdNoYtHuVG97n9W2pHysnHccDgzTUyWM78V8od2',
        'lat' : lat,
        'lon' : long,   
        'system_capacity': cap,
        'azimuth' : azm,
        'tilt' : tilt,
        'array_type': array_t,
        'module_type' : mod_t,
        'losses' : losses    
        

    }

    PARAMS_20 = {
        'api_key':'qKdNoYtHuVG97n9W2pHysnHccDgzTUyWM78V8od2',
        'lat' : lat,
        'lon' : long,   
        'system_capacity': cap,
        'azimuth' : azm,
        'tilt' : tilt,
        'array_type': array_t,
        'module_type' : mod_t,
        'losses' : 20    
        

    }

    IDEAL = {
        'api_key':'qKdNoYtHuVG97n9W2pHysnHccDgzTUyWM78V8od2',
        'lat' : lat,
        'lon' : long,   
        'system_capacity': cap,
        'azimuth' : 180 ,
        'tilt' : lat,
        'array_type': array_t,
        'module_type' : mod_t,
        'losses' : 20    
        

    }




    if st.button('Calculate'):

        r = requests.get(url = api, params = PARAMS)
        r_20 =  requests.get(url = api, params = PARAMS_20)
        i = requests.get(url = api, params = IDEAL) 
        #st.write('result: %s' % r)




        data = r.json()
        data_20 = r_20.json()
        ideal = i.json()
        AC_ANNUALS= json.dumps(data["outputs"]["ac_annual"], indent=4)
        AC_ANNUALS_20= json.dumps(data_20["outputs"]["ac_annual"], indent=4)
        IDEAL_ANNUALS = json.dumps(ideal["outputs"]["ac_annual"], indent=4)
        float_cap = round(float (cap),1)
        float_AC = round(float (AC_ANNUALS),1)
        st.text("rounding")
        st.write(float_AC)
        float_AC_20 = round(float (AC_ANNUALS_20),1)
        float_Ideal = round(float (IDEAL_ANNUALS),1)
        float_Cust = round(float (cust),2)
        Percentage = round (float (AC_ANNUALS_20)/ float (IDEAL_ANNUALS) *100 ,1)
        Cust_range = round((((float_Cust)/float_AC)*100), 1) 

        AC_TOTAL = float_AC    
        print(Percentage)
        #st.write(r.url)    
        st.write(r.status_code)

        #col1, col2, col3 = st.beta_columns(3)

        #col1 = st.write(PARAMS)
        #col2 = st.write(PARAMS_20)
        #col3 = st.write(IDEAL)


        print(json.dumps(data["inputs"], indent=4, separators=(". ", " = ")))
        print(json.dumps(data["station_info"], indent=4, separators=(". ", " = ")))
        print(json.dumps(data["outputs"]["ac_monthly"], indent=4))

        st.write("CUSTOMER_AC_ANNUALS: " + str(float_Cust))
        st.write("AC_ANNUALS: " + str(float_AC))
        st.write("AC_ANNUALS 20 Losses : " + str(float_AC_20))
        
        st.write("IDEAL_ANNUALS: " + str(float_Ideal))
        st.write("AC_A_20% / AC_AN_IDEAL %: " + str (Percentage) )

        
        st.write("Customer withing 5%: " + str (Cust_range))

        float_Panel  =float (Panel)

        st.write("Num of Panels: " + str (round(float_cap*1000/float (Panel))))

def about():
    st.title("About")
    st.info(
    """
    a reproducible audit and computational framework. You can learn more about 
    [Compurational_Engineering](https://en.wikipedia.org/wiki/Computational_engineering).
    """
    )


st.sidebar.title("Navigation")
radio = st.sidebar.radio(label="", options=["PV Calculator", "Project Info" , "About - changelog"])
#selection = st.sidebar.radio("Go to", "PV Calculator","About")


if radio == "PV Calculator":
    app()
elif radio == "Project Info":
    info()
elif radio == "About - changelog":
    about()




st.sidebar.title("Note:")
st.sidebar.info(
    "A **computational science** method to use advanced computing to address scientific" 
    "& engineering challenges to solve energy problems using high-performance computing (HPC),"
    " datascience, applied mathematics, scientific data management, visualization")


#rev = st.sidebar.selectbox("Reviewer", ["Kava", "Jenan", "David"])
#app_id = st.sidebar.text_input("Application Id", "ESD-XXXXX")
#start = st.sidebar.button("Start")