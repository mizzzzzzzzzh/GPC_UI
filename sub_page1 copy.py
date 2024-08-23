import streamlit as st
import asyncio
import time
from streamlit_extras.metric_cards import style_metric_cards

print("page 1", st.session_state)



c1,c2= st.columns((3,1))
c1.image("logo long.png", width=800)
# c2.header(f"机组建模与先进GPC控制系统")

async def header_clock(field):
    # c2.header(f"机组建模与先进GPC控制系统 \n {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    while True:
        field.header(f" {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        await asyncio.sleep(1)


c2_empty = c2.empty()




async def metric():
    # c1,_,c2,_,c3 = st.columns((5,1,5,1,5))

    # if c1.button("🕙 实时监控系统", type="primary", use_container_width=True):
    #     st.switch_page("sub_page1.py")
    # if c2.button("〽️ 离线数据回溯", use_container_width=True):
    #     st.switch_page("sub_page2.py")
    # if c3.button("© 先进控制系统", use_container_width=True):
    #     st.switch_page("sub_page3.py")
    # st.tabs(["Real-time monitoring system"])    
    col = st.columns((1.5, 3, 3, 2), gap='small')
    with col[0]:
        st.markdown(
            """
        <style>
        [data-testid="stMetricValue"] {
            font-size: 15px;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
        st.metric("当前负荷", value="100 MW", delta= '10 MW')
        st.metric("变负荷率", value="-20 MW/Min", delta= '+2 MW/Min')
        st.metric("主汽压力", value="12 MPa", delta= '-1 Mpa')
        st.metric("主汽温度", value="500 ℃", delta= '0 ℃')
        st.metric("主汽流量", value="600 t/h", delta= '10 t/h')
        st.metric("总煤量", value="88 t/h", delta= '3 t/h')


style_metric_cards(border_left_color="#393939",border_color="#393939", background_color="#1E1E1E")


async def main():
    await asyncio.gather(
        header_clock(c2_empty),
        metric(),
        
    )
    
asyncio.run(main())
print("page 1 end", st.session_state)















