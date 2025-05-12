import os
import openai
from dotenv import load_dotenv

from prompt import NL_sys_prompt, code_sys_prompt


load_dotenv()
GPT_MODEL = 'gpt-4o'

OPENAI_API_KEY = "sk-BSGfDjcXdNgB1JUF92448fB22442442aAbC07646F4D2CcE7"
OPENAI_API_BASE = "https://one.ooo.cool/v1"

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
            temperature=0.5
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
            temperature=0.5
        )
    except Exception as e:
        return f"生成回复时出错: {str(e)}"