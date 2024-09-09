import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.mandatory_date_range import date_range_picker
from streamlit_modal import Modal
from utils.http_api_helper import history_data_retrieve_api, login_api

import json
import pandas as pd

print("page 3", st.session_state)
df = pd.read_parquet("data/data.parquet")

st.set_page_config(
    page_title="先进控制系统",
    page_icon=":shield:",
    layout="wide",
    initial_sidebar_state="expanded",
)



class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.error_integral = 0
        self.previous_error = 0

    def update(self, setpoint, process_variable):
        error = setpoint - process_variable
        self.error_integral += error
        error_derivative = error - self.previous_error
        output = (self.Kp * error) + (self.Ki * self.error_integral) + (self.Kd * error_derivative)
        self.previous_error = error
        return output

login_data = {
    "username": "ics_data",
    "password": "123456",
}
if st.session_state.get("token") is None:
    st.session_state["token"] = json.loads(login_api(login_data))["data"]["token"]

c1,c2, c3,c4,c5= st.columns((2,4,2,2,2,), vertical_alignment='center')
c1.image("logo2.png", width=200)
c2.markdown(f"### 机组建模与先进GPC控制系统")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["控制系统-1", "控制系统-2", "控制系统-3", "控制系统-4", "控制系统-5"])

if c3.button("🕙 实时监控系统", use_container_width=True):
    st.switch_page("sub_page1.py")
if c4.button("〽️ 离线数据回溯", use_container_width=True):
    st.switch_page("sub_page2.py")
if c5.button("© GPC先进控制系统", type="primary", use_container_width=True):
    st.switch_page("sub_page3.py")


with tab1:
    
    row_1 = st.columns((3,3,1))
    with row_1[0]:
        st.subheader("GPC控制系统")
        with st.form("pred_mode"):
            pred_mode_row1 = st.columns((1,1,1,1))
            number = pred_mode_row1[0].number_input("控制参数-1")
            number = pred_mode_row1[1].number_input("控制参数-2")
            number = pred_mode_row1[2].number_input("控制参数-3")
            number = pred_mode_row1[3].number_input("控制参数-4")
            option = st.selectbox(
                "选择预测模型",
                ("Model-1  (some info 如：优化目标函数值，优化算法描述信息等)", "Model-2", "Model-3", "Model-4" ,"..."),
            )
            result = date_range_picker("选择数据日期")
            submitted = st.form_submit_button("查看预测模型效果")
            if "model_pushed" not in st.session_state:
                st.session_state.model_pushed = False
            if submitted or st.session_state.model_pushed:
                st.session_state.model_pushed = True
                tab1, tab2, tab3, tab4, tab5 = st.tabs(["变量-1", "变量-2", "变量-3", "变量-4", "变量-5"])
                y = [3.704, 3.703, 3.702, 3.69 , 3.69 , 3.694, 3.662, 3.691, 3.683,3.693, 3.698, 3.682, 3.675, 3.683, 3.682, 3.69 , 3.699, 3.698,3.698, 3.698, 3.687, 3.659, 3.687, 3.712, 3.697, 3.697, 3.697,3.698, 3.698, 3.698, 3.689, 3.649, 3.685, 3.666, 3.666, 3.658,3.654, 3.708, 3.663, 3.707, 3.678, 3.688, 3.678, 3.677, 3.646,3.663, 3.658, 3.659, 3.715, 3.664, 3.679, 3.642, 3.642, 3.696,3.658, 3.702, 3.703, 3.679, 3.661, 3.651, 3.704, 3.684, 3.671,3.651, 3.668, 3.69 , 3.667, 3.68 , 3.686, 3.701, 3.681, 3.694,3.669, 3.707, 3.655, 3.686, 3.666, 3.683, 3.638, 3.631, 3.665,3.679, 3.686, 3.65 , 3.637, 3.646, 3.685, 3.709, 3.668, 3.686,3.644, 3.672, 3.672, 3.691, 3.704, 3.672, 3.662, 3.645, 3.629,3.637, 3.698, 3.702, 3.653, 3.659, 3.671, 3.684, 3.682, 3.679,3.694, 3.66 , 3.668, 3.657, 3.696, 3.674, 3.655, 3.652, 3.663,3.654, 3.671, 3.67 , 3.652, 3.648, 3.666, 3.658, 3.694, 3.689,3.674, 3.645, 3.645, 3.679, 3.649, 3.649, 3.713, 3.663, 3.696,3.654, 3.702, 3.65 , 3.686, 3.644, 3.656, 3.67 , 3.673, 3.653,3.677, 3.643, 3.673, 3.673, 3.666, 3.663, 3.686, 3.669, 3.663,3.669, 3.642, 3.687, 3.675, 3.671, 3.67 , 3.672, 3.673, 3.67 ,3.672, 3.673, 3.674, 3.674, 3.674, 3.675, 3.675, 3.675, 3.675,3.675, 3.675, 3.676, 3.676, 3.676, 3.676, 3.676, 3.676, 3.676,3.676, 3.676]
                y_pred = [3.691, 3.691, 3.691, 3.685, 3.68 , 3.674, 3.666, 3.677, 3.677,3.685, 3.687, 3.672, 3.67 , 3.676, 3.676, 3.683, 3.686, 3.689,3.689, 3.689, 3.68 , 3.671, 3.657, 3.673, 3.698, 3.689, 3.689,3.689, 3.689, 3.689, 3.684, 3.658, 3.685, 3.667, 3.662, 3.66 ,3.656, 3.692, 3.672, 3.676, 3.683, 3.687, 3.673, 3.675, 3.649,3.648, 3.66 , 3.681, 3.69 , 3.679, 3.671, 3.655, 3.661, 3.679,3.668, 3.68 , 3.696, 3.674, 3.668, 3.666, 3.68 , 3.684, 3.676,3.658, 3.672, 3.696, 3.678, 3.674, 3.675, 3.669, 3.677, 3.714,3.672, 3.679, 3.691, 3.683, 3.67 , 3.653, 3.658, 3.668, 3.663,3.664, 3.683, 3.659, 3.65 , 3.647, 3.67 , 3.68 , 3.687, 3.685,3.658, 3.676, 3.665, 3.669, 3.693, 3.678, 3.666, 3.659, 3.651,3.654, 3.671, 3.686, 3.681, 3.658, 3.704, 3.674, 3.672, 3.702,3.68 , 3.67 , 3.664, 3.67 , 3.676, 3.692, 3.657, 3.66 , 3.668,3.66 , 3.656, 3.665, 3.67 , 3.657, 3.704, 3.669, 3.673, 3.671,3.683, 3.677, 3.648, 3.661, 3.649, 3.662, 3.7  , 3.68 , 3.676,3.687, 3.652, 3.671, 3.681, 3.663, 3.664, 3.671, 3.677, 3.671,3.673, 3.68 , 3.665, 3.678, 3.669, 3.666, 3.69 , 3.678, 3.664,3.685, 3.658, 3.668, 3.686, 3.678, 3.677, 3.676, 3.678, 3.678,3.677, 3.678, 3.678, 3.679, 3.679, 3.679, 3.679, 3.679, 3.679,3.679, 3.679, 3.679, 3.68 , 3.68 , 3.68 , 3.68 , 3.68 , 3.68 ,3.68 , 3.68 ]

                with tab1:
                    fig = go.Figure([
                        go.Scatter(x=list(range(len(y))), y=y, name='truth', mode='markers'),
                        go.Scatter(x=list(range(len(y))), y=y_pred, name='prediction')
                    ])
                    fig.update_layout(title="变量-1 预测曲线")
                    st.plotly_chart(fig)
                with tab2:
                    fig = go.Figure([
                        go.Scatter(x=list(range(len(y))), y=y, name='truth', mode='markers'),
                        go.Scatter(x=list(range(len(y))), y=y_pred, name='prediction')
                    ])
                    fig.update_layout(title="变量-2 预测曲线")
                    st.plotly_chart(fig)
            
    with row_1[1]:
        st.subheader("控制系统仿真")
        with st.form("simulation"):
            simulation_row1 = st.columns((1,1,1,1))
            number = simulation_row1[0].number_input("仿真参数-1")
            number = simulation_row1[1].number_input("仿真参数-2")
            number = simulation_row1[2].number_input("仿真参数-3")
            number = simulation_row1[3].number_input("仿真参数-4")
            
            submitted = st.form_submit_button("开始仿真")
            if "simu_pushed" not in st.session_state:
                st.session_state.simu_pushed = False
            if submitted or st.session_state.simu_pushed:
                st.session_state.simu_pushed = True
            # 设定PID参数
                Kp = 1.0
                Ki = 1.0  # 增加积分作用
                Kd = 0.1

                # 创建PID控制器实例
                pid_controller = PIDController(Kp, Ki, Kd)

                # 模拟数据
                time_steps = 20  # 增加时间步长
                setpoint = 10.0
                initial_process_value = 0.0
                process_values = [initial_process_value]
                control_outputs = []

                for _ in range(time_steps):
                    # 计算PID输出
                    output = pid_controller.update(setpoint, process_values[-1])
                    
                    # 更新过程变量
                    new_process_value = process_values[-1] + output
                    
                    # 存储结果
                    process_values.append(new_process_value)
                    control_outputs.append(output)

                # 绘制图形
                fig = go.Figure()

                # 添加过程变量的变化
                fig.add_trace(go.Scatter(x=np.arange(time_steps + 1), y=process_values,
                                        mode='lines+markers', name='Process Variable'))

                # 添加控制输出的变化
                fig.add_trace(go.Scatter(x=np.arange(time_steps), y=control_outputs,
                                        mode='lines+markers', name='Control Output'))

                # 添加设定值的水平线
                fig.add_shape(type="line", x0=0, y0=setpoint, x1=time_steps, y1=setpoint, line=dict(color="LightSeaGreen", dash="dash"), name='Setpoint')

                fig.update_layout(title='GPC Controller Simulation ',
                                xaxis_title='Time Step',
                                yaxis_title='Value',
                                legend_title='Legend')
                st.plotly_chart(fig)
                
            
    with row_1[2]:
        st.subheader("应用状态")
        on = st.toggle("投入", value=True)
        if on:
            st.markdown("XXXGPC控制系统:green[已投入]")
        else :
            st.markdown("XXXGPC控制系统:red[已停止]")
            # st.markdown("This text is :red[colored red], and this is **:blue[colored]** and bold.")
        st.session_state.on = on
        apply = st.button("应用")
        st.markdown("""
                当前配置：
                ```
                "控制参数-1": 1
                "控制参数-2": 2
                "控制参数-3": 3
                "控制参数-4": 4
                "预测模型": model-1
                ``` """)
            
        modal = Modal(
            "确认应用当前配置？", 
            key="demo-modal",
            # Optional
            padding=20,    # default value
            max_width=744  # default value
        )
        
        if apply:
            modal.open()
            
        if modal.is_open():
            with modal.container():
                st.markdown("""
                            当前配置：
                            ```
                                "控制参数-1": 1,
                                "控制参数-2": 2,
                                "控制参数-3": 3,
                                "控制参数-4": 4,
                                "预测模型": model-1
                            ``` \n
                            即将应用配置：
                            ```
                                "控制参数-1": 1,
                                "控制参数-2": 2,
                                "控制参数-3": 3,
                                "控制参数-4": 4,
                                "预测模型": model-2
                            ```
                            """)
                button_row = st.columns((2,2,2,2),gap="large")
                if button_row[1].button("确认"):
                    modal.close()
                
                if button_row[2].button("放弃"):
                    modal.close()
            
            