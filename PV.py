import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

import requests 
import json

def app():
    AC_TOTAL = 0 
    # datetime object containing current date and time
    now = datetime.now()
    
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)	

    d2 = now.strftime("%B %d, %Y")
    st.write(d2)

    latitude, longitude, capacity = st.beta_columns(3)
    lat = latitude.text_input('Lat:', '49') 
    long = longitude.text_input('Long:', '-112')
    cap = capacity.text_input('System Capacity:', '1') 
    #mod_t = st.selectbox('Module Type: 0 Standard   ||  1 Premium   ||  2 Thin film', ('0','1','2'))
    mod_t = st.selectbox('Module Type: 0 Standard   ||  1 Premium   ||  2 Thin film', ('0', '1', '2', '3'))

    array_t = st.selectbox('Array Type:  0	Fixed - Open Rack || 1	Fixed - Roof Mounted || 2	1-Axis || 3	1-Axis Backtracking || 4 2-Axis', ('0', '1', '2', '3', '4'))
    
    tilt_num, azm_num, losses_num = st.beta_columns(3)
    tilt = tilt_num.text_input('Tilt:', '0') 
    azm = azm_num.text_input('Azimuth:', '180') 
    losses = losses_num.text_input('Losses:', '20') 

    st.write("----------------------------")
    cust = st.text_input('application ac annual (kWh):', '0')
    Panel = st.text_input('Panel Size (kW):', '1')


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
        float_AC = float (AC_ANNUALS)
        float_AC_20 = float (AC_ANNUALS_20)
        float_Ideal = float (IDEAL_ANNUALS)
        float_Cust = float (cust)
        Percentage = round (float (AC_ANNUALS_20)/ float (IDEAL_ANNUALS) *100 ,1)
        Cust_range = round((((float_Cust)/float_AC)*100), 1) 

        AC_TOTAL = float_AC    
        print(Percentage)
        #st.write(r.url)    
        st.write(r.status_code)

        st.write(PARAMS)
        st.write(PARAMS_20)
        st.write(IDEAL)

        input_data = pd.DataFrame(PARAMS[]) 
        input_data.head()

        print(json.dumps(data["inputs"], indent=4, separators=(". ", " = ")))
        print(json.dumps(data["station_info"], indent=4, separators=(". ", " = ")))
        #print(json.dumps(data["outputs"]["ac_monthly"], indent=4))

        st.write("CUSTOMER_AC_ANNUALS: " + cust)
        st.write("AC_ANNUALS: " + AC_ANNUALS)
        st.write("AC_ANNUALS 20 Losses : " + AC_ANNUALS_20)
        
        st.write("IDEAL_ANNUALS: " + IDEAL_ANNUALS)
        st.write("Customer / AC_ANNUALS %: " + str (Percentage) )

        
        st.write("Customer withing 5%: " + str (Cust_range))

        if  -5 <= Cust_range <=5:
            st.write("WIthing Range: True")
        else:
            st.write("WIthing Range: False")

        float_Panel  =float (Panel)

        st.write("Num of Pannels: " + str (round(AC_TOTAL/float (Panel))))

app()
