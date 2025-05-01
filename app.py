import streamlit as st
import os
import json
from datetime import datetime
from prompt_handler import NL_planning, code_planning

# 配置页面
st.set_page_config(
    page_title="具身规划Demo",
    page_icon="🧪",
    layout="wide"
)

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

if "retry_count" not in state:
    state.retry_count = 0

if "code_feedback" not in state:
    state.code_feedback = None

if "needs_code_update" not in state:
    state.needs_code_update = False

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
        state.needs_code_update = False  # 重置代码更新标志
        st.rerun()
    
    # 如果需要更新代码
    if state.needs_code_update:
        with st.chat_message("assistant"):
            with st.spinner(text="正在修改代码...", show_time=False):
                state.response_code = code_planning(state.code_messages)
        state.needs_code_update = False
        st.rerun()

col1, col2 = st.columns(2, border=True)
with col1:
    st.subheader("代码规划")
    if state.response_code != None:
        response = st.write_stream(state.response_code)
        state.code_messages.append({
            "role": "assistant",
            "content": response
        })
        # 添加执行结果部分
        st.subheader("执行结果")
        try:
            # 处理代码，移除markdown代码块标记
            code_to_execute = response
            code_to_execute = code_to_execute.replace("```python", "").replace("```", "").strip()
            with open("temp_code.py", "w") as f:
                f.write(code_to_execute)
            
            # 捕获输出
            import io
            import sys
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                exec(code_to_execute, globals())
            
            # 显示执行结果
            output = f.getvalue()
            if output:
                st.code(output, language="text")
            else:
                st.info("代码执行完成，没有输出内容")
            
            # 执行成功，重置重试计数
            state.retry_count = 0

            # 添加反馈输入框
            feedback = st.text_area("执行反馈（如果需要修改代码，请在这里描述问题）：", key="feedback_input")
            if st.button("提交反馈"):
                if feedback:
                    # 将反馈添加到消息历史
                    feedback_message = {
                        "role": "user",
                        "content": f"代码执行反馈：{feedback}\n原代码：\n```python\n{code_to_execute}\n```\n请你根据当前代码和用户反馈生成新的代码，必要时可以修改api工具中的模拟数据"
                    }
                    state.code_messages.append(feedback_message)
                    state.sys_messages.append({"role": "user", "content": feedback})
                    state.needs_code_update = True
                    st.rerun()
                
        except Exception as e:
            st.error(f"执行出错: {str(e)}")
            st.error("处理后的代码内容：")
            st.code(code_to_execute, language="python")
            
            if state.retry_count < 5:
                state.retry_count += 1
                # 自动将错误信息作为反馈
                error_feedback = {
                    "role": "user",
                    "content": f"代码执行出现错误（第{state.retry_count}次重试）：{str(e)}\n原代码：\n```python\n{code_to_execute}\n```\n请修复这个错误。"
                }
                state.code_messages.append(error_feedback)
                state.sys_messages.append({"role": "user", "content": f"代码执行出现错误（第{state.retry_count}次重试）：{str(e)}"})
                
                # 立即请求新的代码
                with st.spinner(text=f"正在修复代码（第{state.retry_count}次重试）..."):
                    state.response_code = code_planning(state.code_messages)
                st.rerun()
            else:
                st.error("已达到最大重试次数（5次），请手动提供反馈或重新开始。")
                state.retry_count = 0  # 重置重试计数
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
