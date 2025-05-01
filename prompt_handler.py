import os
import openai
from dotenv import load_dotenv

from prompt_plan import NL_sys_prompt, code_sys_prompt

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
        formatted_messages = [
            {"role": "system", "content": code_sys_prompt},
            *messages
        ]

        return client.chat.completions.create(
            model=GPT_MODEL,
            messages = formatted_messages,
            stream=True,
        )
    except Exception as e:
        return f"生成回复时出错: {str(e)}"
