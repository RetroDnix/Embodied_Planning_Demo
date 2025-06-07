import os
import openai

from prompt import code_sys_prompt, code_example

current_dir = os.path.dirname(os.path.abspath(__file__))

GPT_MODEL = 'gpt-4o'

OPENAI_API_KEY = "sk-DRxEVD9NJPfTNZn9852f350063B249Dc9aD49503B1Ad70Ad"
OPENAI_API_BASE = "http://vip.ooo.cool/v1"

client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)


def code_planning(messages, task, use_stream=True):
    """
    通过Code进行提示
    """
    try:
        # import pdb; pdb.set_trace()
        with open(f"{current_dir}/base_action.py") as f:
            api_tools = f.read()
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
