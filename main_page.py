import streamlit as st
import asyncio   
import base64
from pathlib import Path
from streamlit_extras import app_logo
import streamlit_option_menu
from streamlit_option_menu import option_menu
import pandas as pd
import time

from utils.http_api_helper import login_api
import json



st.set_page_config(
    page_title="机组建模与先进GPC控制系统",
    page_icon=":shield:",
    layout="wide",
    initial_sidebar_state="expanded",
)

login_data = {
    "username": "ics_data",
    "password": "123456",
}

if st.session_state.get("token") is None:

    token = json.loads(login_api(login_data))["data"]["token"]
    st.session_state["token"] = token

sub_page1 = st.Page("sub_page1.py", title="实时监控系统", icon="🕙")
sub_page2 = st.Page("sub_page2.py", title="离线数据回溯", icon="〽️")
sub_page3 = st.Page("sub_page3.py", title="先进控制系统", icon="©")
pg = st.navigation([sub_page1, sub_page2, sub_page3],position='hidden') #, position='hidden'
pg.run()
