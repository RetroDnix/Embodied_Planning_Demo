import streamlit as st
import os
import json
from datetime import datetime
from prompt_handler import NL_planning, code_planning
from induce.induce_actions import induce
# 配置页面
st.set_page_config(
    page_title="具身规划Demo",
    page_icon="🧪",
    layout="wide"
)
new_prompt = ""
state = st.session_state

# 初始化会话状态
if "sys_messages" not in state:
    state.sys_messages = []

if "NL_messages" not in state:
    state.NL_messages = []

if "code_messages" not in state:
    state.code_messages = []

if "response_NL" not in state:
    state.response_NL = None

if "response_code" not in state:
    state.response_code = None

if "prompt" not in state:
    state.prompt = None

# 侧边栏 - 聊天界面
with st.sidebar:
    st.header("具身规划Demo")
    # 显示聊天历史
    with st.container(height=400):
        for message in state.sys_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 显示用户消息
        if state.prompt != None:
            # 显示助手正在响应的消息
            with st.chat_message("assistant"):
                with st.spinner(text="正在思考...", show_time=False):
                    # 调用两种不同的提示方式获取流式回复
                    state.response_NL = NL_planning(state.NL_messages)
                    state.response_code = code_planning(state.code_messages)
            state.sys_messages.append({"role": "assistant", "content": "回复已完成"})
            state.prompt = None
            st.rerun()
    
    # 聊天输入
    if new_prompt := st.chat_input("提出任何任务"):
        state.prompt = new_prompt
        # 添加用户消息到历史
        user_input = {"role": "user", "content": new_prompt}
        state.sys_messages.append(user_input)
        state.NL_messages.append(user_input)
        state.code_messages.append(user_input)
        st.rerun()

col1, col2 = st.columns(2, border=True)
with col1:
    st.subheader("代码规划")
    if state.response_code != None:
        # print(state.response_code)
        response = st.write_stream(state.response_code)
        state.code_messages.append({
            "role": "assistant",
            "content": response
        })
        induce(new_prompt, response)
    else:
        st.badge("输入任务以开始", icon=":material/check:", color="green")

with col2:
    st.subheader("NL规划(BaseLine)")
    if state.response_NL != None:
        response = st.write_stream(state.response_NL)
        state.NL_messages.append({
            "role": "assistant",
            "content": response
        }) 
    else:
        st.badge("输入任务以开始", icon=":material/check:", color="green")

# 添加清除聊天按钮
if st.button("清除聊天历史"):
    state.sys_messages = []
    state.NL_messages = []
    state.code_messages = []
    state.response_NL = None
    state.response_code = None
    st.rerun()