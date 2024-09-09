import streamlit as st
import asyncio
import time
from streamlit_extras.metric_cards import style_metric_cards
import numpy as np
from collections import deque, defaultdict
from functools import partial
import pandas as pd
import altair as alt
import websockets
import json
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime


# st.set_page_config(
#     page_title="实时监控系统",
#     page_icon=":shield:",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# logo_container：logo，title_container：标题&时间，subpage1_container：按钮sub_page1，subpage2_container：按钮sub_page2，subpage3_container：按钮sub_page3
logo_container,title_container, subpage1_container,subpage2_container,subpage3_container= st.columns((2,4,2,2,2), vertical_alignment='center') 
if subpage1_container.button("🕙 实时监控系统", type="primary", use_container_width=True):
    st.switch_page("sub_page1.py")
if subpage2_container.button("〽️ 离线数据回溯", use_container_width=True):
    st.switch_page("sub_page2.py")
if subpage3_container.button("© 先进控制系统", use_container_width=True):
    st.switch_page("sub_page3.py")
st.tabs(["Real-time monitoring system"])    

header_time_col = title_container.empty()
col_1 = st.columns((1.5, 6, 6, ), gap='medium')
c11 = col_1[1].empty() # 折线图1 的容器
c12 = col_1[2].empty() # 折线图2 的容器
col_2 = st.columns((1.5, 6, 6, ), gap='medium')
c21 = col_2[1].empty() # 折线图3 的容器
c22 = col_2[2].empty() # 折线图4 的容器
col_3=st.columns((1,1), gap='medium')
c31 = col_3[0].empty() # 切投状态的容器
c32 = col_3[1].empty() # 机组预警状态的容器

logo_container.image("logo2.png", width=200)

async def header_clock(field):
    # c2.header(f"机组建模与先进GPC控制系统 \n {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    while True:
        field.markdown(f"### 机组建模与先进GPC控制系统\n{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        await asyncio.sleep(1)
        
window_size = 60
if "c11_plot" not in st.session_state:
    st.session_state["c11_plot"] = defaultdict(partial(deque, [np.nan]*window_size, maxlen=window_size))
if "c12_plot" not in st.session_state:
    st.session_state["c12_plot"] = defaultdict(partial(deque, [np.nan]*window_size, maxlen=window_size))
if "c21_plot" not in st.session_state:
    st.session_state["c21_plot"] = defaultdict(partial(deque, [np.nan]*window_size, maxlen=window_size))
    
# 蒸汽阀开度、功率是一对输入输出；给煤量和蒸汽压力是一对；给水量和温度是一对


# todo 需要根据生产环境重写该函数，以适应生产环境数据格式。
def c11_plot(rtdata:str):
    # 蒸汽阀开度、功率 plot。 
    data = json.loads(rtdata)
    for k, v in data.items():
        if k=='time_period':
            st.session_state["c11_plot"][k].append(datetime.strptime(v, '%Y-%m-%d %H:%M:%S'))
            # st.session_state["c11_plot"][k].append(v)
        else:
            st.session_state["c11_plot"][k].append(v)
            
        with c11:
            x = pd.to_datetime(np.array(st.session_state["c11_plot"]["time_period"]))
            # x = np.arange(window_size)[::-1]
            y1 = np.array(st.session_state["c11_plot"]["power"])
            y2 = np.array(st.session_state["c11_plot"]["valve_opening"])
            _d = pd.concat([pd.DataFrame({'x': x, 'value':y1, 'label':'功率'}),pd.DataFrame({'x': x, 'value':y2, 'label':'蒸汽阀门开度'})])

            # 创建第一个图层，用于'y1'数据
            chart_y1 = alt.Chart(_d[_d['label'] == '功率']).mark_line().encode(
                x=alt.X('x', title=' ', axis=alt.Axis(format='%H:%M:%S',  labelAngle=-45)),
                y=alt.Y('value', title='功率 (MW)',scale=alt.Scale(zero=False)),
                color=alt.Color('label:N', legend=alt.Legend(title='', 
                                              orient='right',  # 设置为右侧
                                              direction='vertical',  # 垂直方向
                                              offset=3))
            ).properties(width=600, title='y1 data')
            
            # 创建第二个图层，用于'y2'数据
            chart_y2 = alt.Chart(_d[_d['label'] == '蒸汽阀门开度']).mark_line().encode(
                x='x',
                y=alt.Y('value', title='阀门开度（%）', scale=alt.Scale(zero=False)),
                color=alt.Color('label:N', legend=None)  # 这里我们不需要图例，因为已经由第一个图层添加了
            ).properties(width=600, title='y2 data')

            # 将两个图层组合在一起，并确保Y轴是独立的
            combined_chart = (chart_y1 + chart_y2).resolve_scale(y='independent').properties(title='蒸汽阀门开度&功率')

            # 显示图表
            st.altair_chart(combined_chart, use_container_width=True)

# todo 需要根据生产环境重写该函数，以适应生产环境数据格式。
def c12_plot(rtdata:str):
    # 给煤量与蒸汽压力
    data = json.loads(rtdata)
    for k, v in data.items():
        if k=='time_period':
            st.session_state["c12_plot"][k].append(datetime.strptime(v, '%Y-%m-%d %H:%M:%S'))
        else:
            st.session_state["c12_plot"][k].append(v)
            
        with c12:
            x = pd.to_datetime(np.array(st.session_state["c12_plot"]["time_period"]))
            y1 = np.array(st.session_state["c12_plot"]["coal_feed"])
            y2 = np.array(st.session_state["c12_plot"]["main_steam_pressure"])
            _d = pd.concat([pd.DataFrame({'x': x, 'value':y1, 'label':'给煤量'}),pd.DataFrame({'x': x, 'value':y2, 'label':'蒸汽压力'})])

            # 创建第一个图层，用于'y1'数据
            chart_y1 = alt.Chart(_d[_d['label'] == '给煤量']).mark_line().encode(
                x=alt.X('x', title=' ', axis=alt.Axis(format='%H:%M:%S', labelAngle=-45)),
                y=alt.Y('value', title='给煤量 (t/h)',scale=alt.Scale(zero=False)),
                color=alt.Color('label:N', legend=alt.Legend(title='', 
                                              orient='right',  # 设置为右侧
                                              direction='vertical',  # 垂直方向
                                              offset=3))
            ).properties(width=600, title='y1 data')
            
            # 创建第二个图层，用于'y2'数据
            chart_y2 = alt.Chart(_d[_d['label'] == '蒸汽压力']).mark_line().encode(
                x='x',
                y=alt.Y('value', title='蒸汽压力（MPa）', scale=alt.Scale(zero=False)),
                color=alt.Color('label:N', legend=None)  # 这里我们不需要图例，因为已经由第一个图层添加了
            ).properties(width=600, title='y2 data')

            # 将两个图层组合在一起，并确保Y轴是独立的
            combined_chart = (chart_y1 + chart_y2).resolve_scale(y='independent').properties(title='给煤量&蒸汽压力')

            # 显示图表
            st.altair_chart(combined_chart, use_container_width=True)

# todo 需要根据生产环境重写该函数，以适应生产环境数据格式。
def c21_plot(rtdata:str):
    # 给水量&温度
    data = json.loads(rtdata)
    for k, v in data.items():
        if k=='time_period':
            # st.session_state["c21_plot"][k].append(datetime.strptime(v, '%Y-%m-%d %H:%M:%S'))
            st.session_state["c21_plot"][k].append(v)
        else:
            st.session_state["c21_plot"][k].append(v)
            
        with c21:
            x = pd.to_datetime(np.array(st.session_state["c21_plot"]["time_period"]))
            # x = np.arange(window_size)[::-1]
            y1 = np.array(st.session_state["c21_plot"]["intermediate_point_temperature"])
            y2 = np.array(st.session_state["c21_plot"]["water_supply"])
            _d = pd.concat([pd.DataFrame({'x': x, 'value':y1, 'label':'中间点温度'}),pd.DataFrame({'x': x, 'value':y2, 'label':'给水流量'})])

            # 创建第一个图层，用于'y1'数据
            chart_y1 = alt.Chart(_d[_d['label'] == '中间点温度']).mark_line().encode(
                x=alt.X('x', title=' ', axis=alt.Axis(format='%H:%M:%S', labelAngle=-45)),
                y=alt.Y('value', title='中间点温度 (℃)',scale=alt.Scale(zero=False)),
                color=alt.Color('label:N', legend=alt.Legend(title='', 
                                              orient='right',  # 设置为右侧
                                              direction='vertical',  # 垂直方向
                                              offset=3))
            ).properties(width=600, title='y1 data')
            
            # 创建第二个图层，用于'y2'数据
            chart_y2 = alt.Chart(_d[_d['label'] == '给水流量']).mark_line().encode(
                x='x',
                y=alt.Y('value', title='给水流量（t/h）', scale=alt.Scale(zero=False)),
                color=alt.Color('label:N', legend=None)  # 这里我们不需要图例，因为已经由第一个图层添加了
            ).properties(width=600, title='y2 data')

            # 将两个图层组合在一起，并确保Y轴是独立的
            combined_chart = (chart_y1 + chart_y2).resolve_scale(y='independent').properties(title='给水量&温度')

            # 显示图表
            st.altair_chart(combined_chart, use_container_width=True)



async def metric():
    st.markdown(
            """
        <style>
        [data-testid="stMetricValue"] {
            font-size: 20px;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
    st.markdown(
            """
        <style>
        [data-testid="stMetricLabel"] {
            font-size: 100px;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

# todo 修改为从ws api服务中获取数据
    with col_1[0]:

        st.metric("当前负荷", value="100 MW", delta= '10 MW')
        st.metric("变负荷率", value="-20 MW/Min", delta= '+2 MW/Min')
        st.metric("主汽压力", value="12 MPa", delta= '-1 Mpa')
    with col_2[0]:
        st.metric("主汽温度", value="500 ℃", delta= '0 ℃')
        st.metric("主汽流量", value="600 t/h", delta= '10 t/h')
        st.metric("总煤量", value="88 t/h", delta= '3 t/h')


style_metric_cards(border_left_color="#393939",border_color="#393939", background_color="#1E1E1E")



async def tables(c, data):
    c.dataframe(data,hide_index=True, use_container_width=True)
    
async def container(c, data):
    c.container

def set_row_background_css(row):
    v = row.iloc[0]
    if v == '未投入':  # 第一行设置CornflowerBlue 矢车菊的蓝色..
        _css = 'background-color: #2f75e2'
    elif v == '报警':  # 第5行设置橘黄色
        _css = 'background-color: #EA0E0E'
    else:
        _css = None
    return [_css] * len(row)



ctl_df = pd.DataFrame({'优化控制器—1': ['投入'],'优化控制器—2': ['未投入'],'优化控制器—3': ['投入'],'优化控制器—4': ['投入'],'优化控制器—5': ['未投入'],'优化控制器—6': ['投入']}).style.apply(set_row_background_css, axis=0)
warning_df = pd.DataFrame({'预警状态—1': ['正常'],'预警状态—2': ['报警'], '预警状态—3': ['正常'],'预警状态—4': ['正常'],'预警状态—5': ['报警'],'预警状态—6': ['正常']}).style.apply(set_row_background_css, axis=0)

from utils.ws_api_helper import receive_realtime_data
namespace = "dummy_namespace"
st.session_state['token'] = ''
uri = f"ws://localhost:8720/rtdata?namespace={namespace}&token={st.session_state['token']}"
async def main():
    await asyncio.gather(
        header_clock(header_time_col),
        metric(),
        receive_realtime_data(uri, { "type":"point", "cols":[ "time_period", "power", "valve_opening" ] } , c11_plot),
        receive_realtime_data(uri, { "type":"point", "cols":[ "time_period", "coal_feed", "main_steam_pressure" ] } , c12_plot),
        receive_realtime_data(uri, { "type":"point", "cols":[ "time_period", "intermediate_point_temperature", "water_supply" ] } , c21_plot),

        tables(c31, ctl_df),
        tables(c32, warning_df),
    )


asyncio.run(main())
# print("page 1 end", st.session_state)















