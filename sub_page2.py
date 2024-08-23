import streamlit as st
from streamlit_date_picker import date_range_picker, date_picker, PickerType
from datetime import datetime, timedelta
from streamlit_extras.mandatory_date_range import date_range_picker
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from io import StringIO
import contextlib
import sys
    
df = pd.read_parquet("data/data.parquet")

print("page 2", st.session_state)
# st.set_page_config(
#     page_title="数据回溯系统",
#     page_icon=":shield:",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )
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

with st.form("retrieval_info"):
    # header = st.columns([1,2,3,1])
    # header[0].subheader('Color')
    # header[1].subheader('Opacity')
    # header[2].subheader('Size')

    row1 = st.columns([2,4,4,1], vertical_alignment='center', gap="large")
    option = row1[0].selectbox(
        "请选择要查看的控制系统",
        ("汽温控制系统", "风烟系统", "燃烧总图", "给水系统" ,"..."),
    )
    field_selected = row1[1].multiselect(
        "请选择严查看的变量",
        ["负荷", "主汽压", "主汽温", "主汽流量", "再热气压", "再热气温", "总风量", "总煤量", "汽包水位", "给水流量"],
        ["负荷", "主汽压", "主汽温", "主汽流量"],
    )
    with row1[2]:
        result = date_range_picker("Select a date range")

    # st.write("Result:", result[1].ctime())
    
    row1[3].form_submit_button('查  询',type="secondary", use_container_width=True)

# st.markdown("This text is :red[colored red], and this is **:blue[colored]** and bold.")

# print("page 2 end")
row2 = st.columns([1,3], gap="large")
def df_info_to_markdown(df):
    # 获取列名和数据类型
    columns = df.columns.tolist()
    dtypes = df.dtypes.tolist()
    
    # 计算每列的非空值数量
    non_null_counts = df.count().tolist()
    
    # 创建Markdown表格
    markdown_table = "| Column | Non-null Count | Dtype |\n"
    markdown_table += "| --- | --- | --- |\n"
    
    for i in range(len(columns)):
        markdown_table += f"| {columns[i]} | {non_null_counts[i]} | {dtypes[i]} |\n"
    
    return markdown_table

with row2[0]:
    st.subheader("数据统计")
    st.markdown('---')
    st.dataframe(df.describe().T)
    # st.markdown(df_info_to_markdown(df))
    

with row2[1]:
    # st.subheader("数据视图")
    # Create random data with numpy
    # np.random.seed(1)

    N = 100
    random_x = np.linspace(0, 1, N)
    random_y0 = np.random.randn(N) + 5
    random_y1 = np.random.randn(N)
    random_y2 = np.random.randn(N) - 5

    # Create figure with secondary y-axis
    fig = go.Figure()

    # Add traces on the primary y-axis
    fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                            mode='lines',
                            name='lines',
                            yaxis='y1'))  # Specify the default y-axis

    # Add traces on the secondary y-axis
    fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                            mode='lines+markers',
                            name='lines+markers',
                            yaxis='y2'))  # Use the secondary y-axis

    # Add traces on the tertiary y-axis
    fig.add_trace(go.Scatter(x=random_x, y=random_y2,
                            mode='markers',
                            name='markers',
                            yaxis='y3'))  # Use the tertiary y-axis

    # Define layout for secondary and tertiary y-axes
    fig.update_layout(
        yaxis=dict(title='Primary Y-axis'),
        yaxis2=dict(title='Secondary Y-axis', overlaying='y', side='right', anchor='free', position=0.95),
        yaxis3=dict(title='Tertiary Y-axis', overlaying='y', side='right', anchor='free', position=1),
        xaxis=dict(title='X-axis', domain=[0, 0.95]),
        width=800, 
        height=600
    )
   
    st.plotly_chart(fig, use_container_width=True)


