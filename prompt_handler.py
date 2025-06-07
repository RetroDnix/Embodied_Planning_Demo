import os
import openai
from dotenv import load_dotenv

from prompt import NL_sys_prompt, code_sys_prompt, code_example
from custiom_action_set import CustomActionSet



load_dotenv()
GPT_MODEL = 'gpt-4o'

OPENAI_API_KEY = "sk-DRxEVD9NJPfTNZn9852f350063B249Dc9aD49503B1Ad70Ad"
OPENAI_API_BASE = "http://vip.ooo.cool/v1"

client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

def get_score(prompt: str) -> str:
    """将简单的提示词发送给大模型并返回结果"""
    try:
        messages = [
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
            stream=False
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"调用大模型时出错: {str(e)}"

def extract_action_sequence(code_response: str) -> list[str]:
    """从代码响应中提取动作序列"""
    try:
        # 构建提示来提取动作序列
        extraction_prompt = f"""请从以下代码中提取一个有序的动作序列列表。每个动作应该是一个具体的、可执行的步骤，动作列表中每一个动作要用自然语言表示出来。
        只返回动作列表，不要包含任何其他解释或格式。

        代码：
        {code_response}
        """
        
        messages = [
            {"role": "system", "content": "你是一个动作序列提取专家。你的任务是从代码中提取有序的动作序列。只返回动作列表，每行一个动作。"},
            {"role": "user", "content": extraction_prompt}
        ]
        
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
            stream=False
        )
        
        # 处理响应，将文本分割成动作列表
        actions = [action.strip() for action in response.choices[0].message.content.split('\n') if action.strip()]
        return actions
    except Exception as e:
        st.error(f"提取动作序列时出错: {str(e)}")
        return []
def extract_action_sequence_nl(code_response: str) -> list[str]:
    """从代码响应中提取动作序列"""
    try:
        # 构建提示来提取动作序列
        extraction_prompt = f"""请从以下自然语言输出中提取一个有序的动作序列列表。每个动作应该是一个具体的、可执行的步骤，动作列表中每一个动作要用自然语言表示出来。
        只返回动作列表，不要包含任何其他解释或格式。

        自然语言输出：
        {code_response}
        """
        
        messages = [
            {"role": "system", "content": "你是一个动作序列提取专家。你的任务是从自然语言输出中提取有序的动作序列。只返回动作列表，每行一个动作。"},
            {"role": "user", "content": extraction_prompt}
        ]
        
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
            stream=False
        )
        
        # 处理响应，将文本分割成动作列表
        actions = [action.strip() for action in response.choices[0].message.content.split('\n') if action.strip()]
        return actions
    except Exception as e:
        st.error(f"提取动作序列时出错: {str(e)}")
        return []
def NL_planning(messages):
    """
    通过NL进行提示
    """
    try:
        formatted_messages = [
            {"role": "system", "content": NL_sys_prompt},
            *messages
        ]

        return client.chat.completions.create(
            model=GPT_MODEL,
            messages=formatted_messages,
            stream=True,
            temperature=0.5
        )
    except Exception as e:
        return f"生成回复时出错: {str(e)}"

def code_planning(messages, task, use_stream=True, print_log=True):
    """
    通过Code进行提示
    """
    try:
        # 基于API进行检索设置
        custom_actions = CustomActionSet(retrievable_actions=True,use_API=True, print_log=print_log)
        api_tools = custom_actions.describe(
            with_long_description=True,
            with_examples=True,
            retrieval_query = task,
            num_retrieve = 5
        )
        if print_log:
            print(f"api_tools:\n{api_tools}\n{'='*50}")
        # 无检索设置
        # custom_actions = CustomActionSet(retrievable_actions=False)
        # api_tools = custom_actions.describe(
        #     with_long_description=True,
        #     with_examples=True
        # )
        # print(f"api_tools{api_tools}")
        # 使用本地模型进行检索设置
        # custom_actions = CustomActionSet(retrievable_actions=True,model_name="Alibaba-NLP/gte-Qwen2-1.5B-instruct")
        # api_tools = custom_actions.describe(
        #     with_long_description=True,
        #     with_examples=True,
        #     retrieval_query = task,
        #     num_retrieve = 7
        # )
        formatted_sys_prompt = code_sys_prompt.format(api_tools=api_tools, code_example=code_example)
        # print(formatted_sys_prompt)
        formatted_messages = [
            {"role": "system", "content": formatted_sys_prompt},
            *messages
        ]

        return client.chat.completions.create(
            model=GPT_MODEL,
            messages = formatted_messages,
            stream=use_stream,
            temperature=0.5
        )
    except Exception as e:
        return f"生成回复时出错: {str(e)}"
