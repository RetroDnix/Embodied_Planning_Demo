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
        )
    except Exception as e:
        return f"生成回复时出错: {str(e)}"

def code_planning(messages):
    """
    通过Code进行提示
    """
    try:
        # 基于API进行检索设置
        custom_actions = CustomActionSet(retrievable_actions=True,use_API=True)
        api_tools = custom_actions.describe(
            with_long_description=True,
            with_examples=True,
            retrieval_query = messages[-1]["content"],
            num_retrieve = 5
        )
        # print(f"api_tools{api_tools}")
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
        #     retrieval_query = messages[-1]["content"],
        #     num_retrieve = 7
        # )
        formatted_sys_prompt = code_sys_prompt.format(api_tools=api_tools, code_example=code_example)
        formatted_messages = [
            {"role": "system", "content": formatted_sys_prompt},
            *messages
        ]

        return client.chat.completions.create(
            model=GPT_MODEL,
            messages = formatted_messages,
            stream=True,
        )
    except Exception as e:
        return f"生成回复时出错: {str(e)}"