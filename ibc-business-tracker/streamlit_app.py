import streamlit as st
import numpy as np
import pandas as pd
import openpyxl

# Set page title and layout
st.set_page_config(page_title='IBC Data Explorer Dashboard', page_icon='📊', layout='wide')

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Sales", "Traffic", "Manage"])

# Page routing
if page == "Home":
    import page.home as home
    home.app()
elif page == "Sales":
    import page.sales as sales
    sales.app()
elif page == "Traffic":
    import page.traffic as traffic
    traffic.app()
elif page == "Manage":
    import page.manage as manage
    manage.app()
