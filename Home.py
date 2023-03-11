# Import library
import streamlit as st
import pandas as pd
#from numerize.numerize import numerize
#from PIL import Image
#import streamlit.components.v1 as components


# set the general page configuration 
st.set_page_config(
    page_title="Fuel Consumption Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)
hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
with open('/Agilis_DashBoard/Agilis_Consommation_dash/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# put a global header for the home page
st.header('متابعة التزود و إستهلاك الوقود بالبطاقة الذكية')
# create cards
#st.markdown('### Metrics')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")
col4.metric("unknown", "45%", "10%")




