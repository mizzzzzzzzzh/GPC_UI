import streamlit as st
import asyncio
import time
from streamlit_extras.metric_cards import style_metric_cards
import numpy as np
from collections import deque, defaultdict
from functools import partial
import pandas as pd
import altair as alt

import plotly.graph_objs as go
import plotly.express as px



print("page 1", st.session_state)



c1,c2, c3,c4,c5= st.columns((2,4,2,2,2), vertical_alignment='center')
c1.image("logo2.png", width=200)
st.tabs(["Real-time monitoring system"])    


async def header_clock(field):
    # c2.header(f"机组建模与先进GPC控制系统 \n {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    while True:
        field.markdown(f"### 机组建模与先进GPC控制系统\n{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        await asyncio.sleep(1)

header_time_col = c2.empty()

col_1 = st.columns((1.5, 6, 6, ), gap='medium')
col_2 = st.columns((1.5, 6, 6, ), gap='medium')
col_3=st.columns((1,1), gap='medium')


async def consumer(graph, window_size):
    windows1 = defaultdict(partial(deque, [0]*window_size, maxlen=window_size))

    while True:
        with graph:
            new_num_y1 = np.random.randint(1,10)
            new_num_y2 = np.random.randint(1,10)

            windows1['y1'].append(new_num_y1)
            windows1['y2'].append(new_num_y2)
            i = 0
            x = np.arange(i, i+window_size)
            y1 = np.array(windows1['y1'])
            y2 = np.array(windows1['y2'])
            
            df = pd.concat([pd.DataFrame({'x': x, 'value':y1, 'label':'y1'}),pd.DataFrame({'x': x, 'value':y2, 'label':'y2'})])

            # 创建第一个图层，用于'y1'数据
            chart_y1 = alt.Chart(df[df['label'] == 'y1']).mark_line().encode(
                x='x',
                y=alt.Y('value', title='Value Y1'),
                color=alt.Color('label:N', legend=alt.Legend(title='label', 
                                              orient='right',  # 设置为右侧
                                              direction='vertical',  # 垂直方向
                                              offset=3))
            ).properties(width=600, title='y1 data')

            # 创建第二个图层，用于'y2'数据
            chart_y2 = alt.Chart(df[df['label'] == 'y2']).mark_line().encode(
                x='x',
                y=alt.Y('value', title='Value Y2', scale=alt.Scale(zero=False)),
                color=alt.Color('label:N', legend=None)  # 这里我们不需要图例，因为已经由第一个图层添加了
            ).properties(width=600, title='y2 data')

            # 将两个图层组合在一起，并确保Y轴是独立的
            combined_chart = (chart_y1 + chart_y2).resolve_scale(y='independent').properties(title='末级过热器温度SP，PV')

            # 显示图表
            st.altair_chart(combined_chart, use_container_width=True)


            

            
            await asyncio.sleep(1)
        

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

    if c3.button("🕙 实时监控系统", type="primary", use_container_width=True):
        st.switch_page("sub_page1.py")
    if c4.button("〽️ 离线数据回溯", use_container_width=True):
        st.switch_page("sub_page2.py")
    if c5.button("© 先进控制系统", use_container_width=True):
        st.switch_page("sub_page3.py")

    with col_1[0]:

        st.metric("当前负荷", value="100 MW", delta= '10 MW')
        st.metric("变负荷率", value="-20 MW/Min", delta= '+2 MW/Min')
        st.metric("主汽压力", value="12 MPa", delta= '-1 Mpa')
    with col_2[0]:
        st.metric("主汽温度", value="500 ℃", delta= '0 ℃')
        st.metric("主汽流量", value="600 t/h", delta= '10 t/h')
        st.metric("总煤量", value="88 t/h", delta= '3 t/h')


style_metric_cards(border_left_color="#393939",border_color="#393939", background_color="#1E1E1E")


c11 = col_1[1].empty()
c12 = col_1[2].empty()
c21 = col_2[1].empty()
c22 = col_2[2].empty()

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
c31 = col_3[0].empty()
c32 = col_3[1].empty()

async def main():
    await asyncio.gather(
        header_clock(header_time_col),
        metric(),
        consumer(c11, 30),
        consumer(c12, 30),
        consumer(c21, 30),
        consumer(c22, 30),
        tables(c31, ctl_df),
        tables(c32, warning_df),
    )


asyncio.run(main())
print("page 1 end", st.session_state)















