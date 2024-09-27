import streamlit as st
from streamlit_date_picker import date_range_picker, date_picker, PickerType
from datetime import datetime, timedelta, time
from streamlit_extras.mandatory_date_range import date_range_picker
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from io import StringIO
import contextlib
import sys
from utils.http_api_helper import history_data_retrieve_api, login_api
import json 






df = pd.read_parquet("data/data.parquet")

# print("page 2", st.session_state)
# st.set_page_config(
#     page_title="数据回溯系统",
#     page_icon=":shield:",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

SYS_VARS_MAP = {
    "汽温控制系统": ["功率", "给煤", "给水", "阀门开度", "主汽压力", "中间点温度"],
    "XXX": ["XXX","XXX"],
    "...": []
}

VARS_DICT = {
    "给煤": "coal_feed",
    "给水": "water_supply",
    "阀门开度": "valve_opening",
    "主汽压力": "main_steam_pressure",
    "中间点温度": "intermediate_point_temperature",
    "功率": "power",
    "coal_feed": "給煤",
    "water_supply": "給水",
    "valve_opening": "阀门开度",
    "power": "功率",
    "intermediate_point_temperature": "中间点温度",
    "main_steam_pressure": "主汽压力"
}

login_data = {
    "username": "ics_data",
    "password": "123456",
}

if st.session_state.get("sys_selected") is None:
    st.session_state["sys_selected"] = "汽温控制系统"
if st.session_state.get("vars_selected") is None:
    st.session_state["vars_selected"] = SYS_VARS_MAP["汽温控制系统"]
if not st.session_state.get("token"):
    st.session_state["token"] = json.loads(login_api(login_data))["data"]["token"]
    
css="""
<style>
    [data-testid="stForm"] {
        background: #1E1E1E;
    }
</style>
"""
st.write(css, unsafe_allow_html=True)

c1,c2, c3,c4,c5= st.columns((2,4,2,2,2,), vertical_alignment='center')
c1.image("logo2.png", width=200)
c2.markdown(f"### 机组建模与先进GPC控制系统")
st.tabs(["Data Retrieval System"])

if c3.button("🕙 实时监控系统", use_container_width=True):
    st.switch_page("sub_page1.py")
if c4.button("〽️ 离线数据回溯", type="primary", use_container_width=True):
    st.switch_page("sub_page2.py")
if c5.button("© 先进控制系统", use_container_width=True):
    st.switch_page("sub_page3.py")


@st.fragment
def sys_and_vars():
    row1 = st.columns([1,2], vertical_alignment='center', gap="large")

    sys_select = row1[0].selectbox(
        "请选择要查看的控制系统",
        list(SYS_VARS_MAP.keys()),
        
    )
    field_selected = row1[1].multiselect(
        "请选择查看的变量",
        SYS_VARS_MAP[sys_select],
        SYS_VARS_MAP[sys_select][:4]
    )
    st.session_state["sys_selected"] = sys_select
    st.session_state["vars_selected"] = field_selected

sys_and_vars()


with st.form("retrieval_info", border = True):
    row2 = st.columns([1,1,6,1], vertical_alignment='center', gap="medium")
    # header = st.columns([1,2,1,1])
    # header[0].subheader('Color')
    # header[1].subheader('Opacity')
    # header[2].subheader('Size')
    # row12 = st.columns([1,1,2,1])

    start_date = row2[0].date_input("数据开始日期", value=datetime(year=2023, month=2, day=25))
    start_time = row2[1].time_input("数据开始时间", value=time(hour=1, minute=0))


    
    plus_min = row2[2].select_slider(
            "数据持续时间（不超过300分钟）",
            options= [f"{i} min" for i in list(range(1, 301))]
        )    # st.write("Result:", result[1].ctime())
    
    row2[3].form_submit_button('查  询',type="secondary", use_container_width=True)

# st.markdown("This text is :red[colored red], and this is **:blue[colored]** and bold.")

# print("page 2 end")
row2 = st.columns([1,3], gap="large")

with row2[0]:
    st.subheader("数据统计")
    st.markdown('---')
    header = {"token":st.session_state.token}
    print(header)
    body = {
        "endTime": (datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %H:%M:%S') + timedelta(minutes=int(plus_min.split(' ')[0]))).strftime('%Y-%m-%d %H:%M:%S'), 
        "includeBounds": "True",
        "interval": 1000,
        "startTime": f"{start_date} {start_time}",
        "namespace": "unit01",
        "tags": [VARS_DICT[col] for col in st.session_state["vars_selected"]]
        # "tags": ["coal_feed", "water_supply", "valve_opening", "main_steam_pressure","intermediate_point_temperature", "power"]
    }
    print(body)
    resp = history_data_retrieve_api(header, body)
    pdlist = []
    for data in resp.json()['data']:
        base_dict = {"name":data['tag']}
        if data['data']:
            series = pd.DataFrame(data['data']).value.describe().to_dict()
            base_dict.update(series)
        pdlist.append(base_dict)
    st.dataframe(pd.DataFrame(pdlist).set_index("name").T)
    # st.markdown(df_info_to_markdown(df))
    

with row2[1]:
    def history_mutli_plot(resp):
        colors = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#e377c2"]
        fig = go.Figure()
        pdict = {
                "title":"历史曲线",
                "xaxis": dict(title='时间', domain=[0, min(1, 1 - (len(resp['data'])-2) * 0.08)],automargin=True),
            }
        for idx, data in enumerate(resp['data']):
            y_label = data['tag']
            # x = [datetime.strptime(d['time'], '%Y-%m-%d %H:%M:%S') for d in data['data']]
            x = [datetime.fromtimestamp(d['time']/1000) for d in data['data']]
            y = [d['value'] for d in data['data']]
            fig.add_trace(go.Scatter(x=x, y=y, name=VARS_DICT[y_label],yaxis=f'y{idx+1}', line_color=colors[idx]))
            if idx==0:
                pdict["yaxis"] = dict( title=VARS_DICT[y_label], titlefont=dict(color=colors[idx]), tickfont=dict(color=colors[idx]), automargin=True)
            else:
                pdict[f"yaxis{idx+1 if idx!=0 else ''}"] = dict( title=VARS_DICT[y_label], titlefont=dict(color=colors[idx]), tickfont=dict(color=colors[idx]), anchor="free", overlaying="y", side="right", position=1-max(0, idx-1)*0.08,automargin=True)
            
        fig.update_layout(**pdict)
        return fig

    st.plotly_chart(history_mutli_plot(resp.json()), use_container_width=True)


