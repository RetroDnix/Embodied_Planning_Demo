import streamlit as st
from datetime import datetime
from prompt_handler import NL_planning, code_planning
from induce.induce_actions import induce
from custiom_action_set import CustomActionSet

# 配置页面
st.set_page_config(
    page_title="具身规划Demo",
    page_icon="🧪",
    layout="wide"
)

if "nl_messages" not in st.session_state:
    st.session_state.nl_messages = []

if "code_messages" not in st.session_state:
    st.session_state.code_messages = []


# 初始化会话状态
def init_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
        if "current_session" not in st.session_state:
            st.session_state.current_session = {
                "question": None,
                "code_response": "",
                "nl_response": "",
                "timestamp": None,
                "is_streaming": False
            }

    if "selected_history" not in st.session_state:
        st.session_state.selected_history = None # 添加一个标志来避免重复保存到历史记录
    if "already_saved" not in st.session_state:
        st.session_state.already_saved = False

init_session_state()

# 历史记录管理函数
def save_to_history():
    """保存当前会话到历史记录"""
    if st.session_state.current_session["question"] and not st.session_state.already_saved:
        st.session_state.history.append(st.session_state.current_session.copy())
        st.session_state.already_saved = True  # 标记为已保存

def reset_current_session():
    """重置当前会话状态"""
    st.session_state.current_session = {
        "question": None,
        "code_response": "",
        "nl_response": "",
        "function_bodies": None,
        "timestamp": None,
        "is_streaming": False
    }
    st.session_state.already_saved = False# 重置保存标志

def select_history(index):
    """选择并加载历史记录"""
    st.session_state.selected_history = index
    st.session_state.current_session = st.session_state.history[index].copy()
    st.session_state.current_session["is_streaming"] = False  # 确保历史记录不会触发流式生成
    st.rerun()

def clear_all_history():
    """清除所有历史记录和当前会话"""
    st.session_state.history = []
    st.session_state.selected_history = None
    reset_current_session()
    st.rerun()

# 处理OpenAI流式响应
def process_streaming_response(generator):
    """处理流式响应，返回完整响应并生成流式输出"""
    full_response = ""
    for chunk in generator:
        if hasattr(chunk,'choices') and chunk.choices:  # 处理ChatCompletionChunk
            content = chunk.choices[0].delta.content
            if content:
                full_response += content
                yield content
        elif isinstance(chunk, str):  # 处理普通字符串
            full_response += chunk
            yield chunk
        
    return full_response

# 生成响应的函数
def generate_responses(prompt, code_placeholder, nl_placeholder):
    """生成代码规划和NL规划响应"""
    user_message = {"role": "user", "content": prompt}
    # 添加用户消息到各自的对话历史
    st.session_state.nl_messages.append(user_message)
    st.session_state.code_messages.append(user_message)
    
    
    # 生成代码规划响应
    code_response = ""
    # import pdb; pdb.set_trace()
    # print(st.session_state.code_messages, st.session_state.current_session["question"])
    code_generator = code_planning(st.session_state.code_messages, st.session_state.current_session["question"])
    for chunk in process_streaming_response(code_generator):
        code_response += chunk if isinstance(chunk, str) else str(chunk)
        # 使用占位符更新内容，而不是重新创建元素
        code_placeholder.markdown(code_response)
        # 如果有提取的函数定义，在代码栏顶部添加引用块
    action_set = CustomActionSet()
    function_bodies = action_set.get_function_bodies_from_code(code_response)

    if function_bodies:
        # 更新当前会话状态，包含提取的函数代码
        st.session_state.current_session.update({
            "function_bodies" : function_bodies
        })
        with code_placeholder.container():
            # 创建可折叠的引用代码块
            with st.expander("引用代码 (点击展开)", expanded=False):
                for i, func_body in enumerate(function_bodies, 1):
                    st.markdown(f"**函数 {i}:**")
                    st.code(func_body, language='python')
                    st.divider()
            # 显示原始代码响应
            st.markdown(code_response)
    code_assistant_message = {"role": "assistant", "content": code_response}
    st.session_state.code_messages.append(code_assistant_message)
    # 生成NL规划响应
    nl_response = ""
    nl_generator = NL_planning(st.session_state.nl_messages)
    for chunk in process_streaming_response(nl_generator):
        nl_response += chunk if isinstance(chunk, str) else str(chunk)
        # 使用占位符更新内容，而不是重新创建元素
        nl_placeholder.markdown(nl_response)
    # 添加NL响应到NL消息历史
    nl_assistant_message = {"role": "assistant", "content": nl_response}
    st.session_state.nl_messages.append(nl_assistant_message)
    return code_response, nl_response

# 主页面布局
st.title("具身规划Demo")
col1, col2 = st.columns(2)

# 在两列中创建标题
with col1:
    st.subheader("代码规划")
    
with col2:
    st.subheader("NL规划（BaseLine）")

# 侧边栏 - 历史问答模块
with st.sidebar:
    st.header("历史问答")
    
    # 显示历史记录列表
    with st.container(height=550, border=False):
        if not st.session_state.history:
            st.info("暂无历史记录")
        else:
            for index, entry in enumerate(st.session_state.history):
                question_preview = entry['question'][:50] + "..." if len(entry['question']) > 50 else entry['question']
                with st.expander(f"Q{index+1}: {question_preview}", expanded=False):
                    st.caption(f"时间：{entry['timestamp']}")
                    # 将按钮放在expander内部更合理
                    if st.button("查看详情", key=f"view_{index}"):
                        select_history(index)
                    if entry.get("function_bodies"):  # 更安全的字典访问方式
                        st.markdown("**引用代码：​**")
                        for i, func_body in enumerate(entry["function_bodies"], 1):
                            st.markdown(f"**函数 {i}:**")
                            st.code(func_body, language='python')
                            if i < len(entry["function_bodies"]):  # 避免最后一个divider
                                st.divider()

    st.divider()
    
    # 清除历史按钮
    if st.button("清除所有历史", type="primary", use_container_width=True):
        clear_all_history()
    if st.button("重置任务", type="primary", use_container_width=True):
        st.session_state.nl_messages = []
        st.session_state.code_messages = []

# 显示当前状态信息
if display_data := (st.session_state.history[st.session_state.selected_history] if st.session_state.selected_history is not None 
                   else st.session_state.current_session if st.session_state.current_session["question"] 
                   else None):
    status_text = f"{'正在查看历史问题' if st.session_state.selected_history is not None else '当前处理的问题'}: {display_data['question']}"
    st.info(status_text)

# 处理新问题输入
if new_prompt := st.chat_input("提出任何任务"):
    # 如有必要，先保存当前会话 
    if st.session_state.current_session["question"] and not st.session_state.already_saved:
        save_to_history()
    
    # 初始化新会话
    st.session_state.selected_history = None
    st.session_state.already_saved = False# 重置已保存标志
    st.session_state.current_session = {
        "question": new_prompt,
        "code_response": "",
        "nl_response": "",
        "function_bodies": None,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "is_streaming": True# 标记为流式生成中
    }
    # 立即显示用户问题
    st.rerun()

# 创建内容占位符（而不是容器）
code_placeholder = col1.empty()
nl_placeholder = col2.empty()

# 显示内容（当前会话或历史记录）
display_data = None
if st.session_state.selected_history is not None:
    display_data = st.session_state.history[st.session_state.selected_history]
elif st.session_state.current_session["question"] and not st.session_state.current_session["is_streaming"]:
    display_data = st.session_state.current_session

# 如果不是流式生成状态，显示内容
if not st.session_state.current_session["is_streaming"]:
    if display_data and display_data["code_response"]:
        code_placeholder.markdown(display_data["code_response"])
    elif not display_data:
        code_placeholder.info("请输入任务以开始")
    
    if display_data and display_data["nl_response"]:
        nl_placeholder.markdown(display_data["nl_response"])
    elif not display_data:
        nl_placeholder.info("请输入任务以开始")
# 流式生成响应（仅对新问题）
elif (st.session_state.current_session["is_streaming"] and 
      st.session_state.current_session["question"] and
      st.session_state.selected_history is None):
    
    with st.spinner("正在生成响应..."):
        try:
            # 生成规划响应
            code_response, nl_response = generate_responses(
                st.session_state.current_session["question"],
                code_placeholder,
                nl_placeholder
            )
            
            # 更新会话状态
            st.session_state.current_session.update({
                "code_response": code_response,
                "nl_response": nl_response,
                "is_streaming": False
            })
            
            # 执行诱导动作
            with st.spinner("正在执行任务..."):
                induce(st.session_state.current_session["question"], code_response)
                st.toast("任务执行完成!", icon="✅")
            
            # 保存到历史
            save_to_history()
        
        except Exception as e:
            st.error(f"处理请求时出错: {str(e)}")
            st.session_state.current_session["is_streaming"] = False

# 返回按钮- 仅在查看历史时显示
if st.session_state.selected_history is not None:
    if st.button("返回当前会话", type="secondary"):
        st.session_state.selected_history = None
        st.rerun()
