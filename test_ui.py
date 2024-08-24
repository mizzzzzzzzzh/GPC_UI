import streamlit as st
import asyncio   
import base64
from pathlib import Path
from streamlit_extras import app_logo
import streamlit_option_menu
from streamlit_option_menu import option_menu
import pandas as pd
import time

st.set_page_config(
    page_title="机组建模与先进GPC控制系统",
    page_icon=":shield:",
    layout="wide",
    initial_sidebar_state="expanded",
)
# st.logo("logo2.png")
# st.header("机组建模与先进GPC控制系统")
    # Insert custom CSS for glowing effect
# st.markdown(
#     """
#     <style>
#     .cover-glow {
#         width: 120%;
#         height: auto;
#         padding: 3px;
#         box-shadow: 
#     0 0 5px #add8e6,   /* 浅淡蓝色 */
#     0 0 10px #87ceeb,  /* 淡蓝色 */
#     0 0 15px #1e90ff,  /* 深一点的淡蓝色 */
#     0 0 20px #00bfff,  /* 更深的淡蓝色 */
#     0 0 25px #007bff,  /* 蓝色 */
#     0 0 30px #0066cc,  /* 稍微深一些的淡蓝色 */
#     0 0 35px #004d99;  /* 深淡蓝色 */
#         position: relative;
#         z-index: -1;
#         border-radius: 10px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Load and display sidebar image
# img_path = "logo2.png"
# img_base64 = img_to_base64(img_path)
# if img_base64:
#     st.markdown(
#         f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
#         unsafe_allow_html=True,
#     )
# print("page home", st.session_state)

# st.sidebar.write("GPC 切投状态")
sub_page1 = st.Page("sub_page1.py", title="实时监控系统", icon="🕙")
sub_page2 = st.Page("sub_page2.py", title="离线数据回溯", icon="〽️")
sub_page3 = st.Page("sub_page3.py", title="先进控制系统", icon="©")
pg = st.navigation([sub_page1, sub_page2, sub_page3],position='hidden') #, position='hidden'
pg.run()

# st.sidebar.markdown('---')


# st.dataframe(pd.DataFrame({"负荷":["123.4 MW"], "转速":["3000"]}), hide_index=True)
# st.metric(label ='负荷',value = "123.4 MW")

# b1, b2, b3, b4 = st.columns(4)
# b1.metric("Humidity", f"{12}"+"%")
# b2.metric("Feels like", f"{23}")
# b3.metric("Highest temperature", f"{23}")
# b4.metric("Lowest temperature", f"{25}")
