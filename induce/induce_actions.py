import os
import openai
import shutil
from dotenv import load_dotenv
from typing import Optional, List, Tuple
from induce.utils import count_function_calls, get_function_names, extract_code_pieces
from custiom_action_set import CustomActionSet
import subprocess
# 加载环境变量
load_dotenv()

GPT_MODEL = 'gpt-4o'

OPENAI_API_KEY = "sk-DRxEVD9NJPfTNZn9852f350063B249Dc9aD49503B1Ad70Ad"
OPENAI_API_BASE = "http://vip.ooo.cool/v1"

client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)


def load_file_content(file_path: str) -> str:
    """从指定路径加载文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def test_query(task: str, origin_solution: str) -> str:
    """Transform past examples into a test query."""
    query = f"## Task: {task}\n### Original solution:\n{origin_solution}\n"
    return query

def induce_actions(
    sys_msg_path: str,
    instruction_path: str,
    few_shot_path: str,
    test_query: str,
    output_path: str = "output/action.txt"
) -> Optional[List[str]]:
    """组合 prompt 信息并请求 OpenAI API 返回动作建议"""
    messages = [
        {"role": "system", "content": load_file_content(sys_msg_path)},
        {"role": "user", "content": load_file_content(instruction_path)},
        {"role": "user", "content": load_file_content(few_shot_path)},
        {"role": "user", "content": test_query + "\n\n## Reusable Functions"}
    ]

    # 调用 OpenAI 接口
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        stream=False
    )
    response = response.choices[0].message.content
    with open(output_path, 'w') as fw:
         fw.write(test_query + '\n\n\n' + response)

    return response

def extract_and_write_actions(
        response: str, 
        write_action_path: str,
        code_path: str = "output/action.txt") -> Optional[List[str]]:
    """提取代码段并写入文件，如果成功则返回路径和函数名列表"""
    print("** Start Evaluating Response **")
    with open(write_action_path, 'r', encoding='utf-8', errors='ignore') as f:
        existing_action_names = get_function_names(f.read())
    actions = extract_code_pieces(response, start="```python", end="```", do_split=False)
    new_actions, action_names = [], []
    traj_names = get_function_names(actions[-1])
    for a in actions:
        if ("def " in a) and (traj_names[0] not in a) and count_function_calls(a, 1):
            a_names = get_function_names(a, existing_action_names)
            if len(a_names) > 0:
                action_names.extend(a_names)
                new_actions.append(a)
    # TODO: 判断语义重复行为，如果行为重复则不写入文件
    print(
        f"Induced #{len(new_actions)}|{len(action_names)} Actions, ",
        [a.split("\n")[0] for a in new_actions],
        action_names
    )
    if len(new_actions) == 0: return None, None

    custom_actions = CustomActionSet()
    code = ""
    if len(traj_names) == 1:
        program = "\n\n".join(new_actions + [actions[-1]])
        code = custom_actions.to_python_code(program, traj_names[0])

    if code != "":
        with open(code_path, 'w', encoding='utf-8') as f:
            f.write(code)
    else:
        return None

    try:
        print("="*15, " executing code", "="*15)
        # 假设你想模拟多次输入，每个输入值后加上 "\n" 表示回车确认。
        # 根据需要调整重复次数和输入内容。
        mock_inputs = "dummy_input\n" * 3  # 提供10次任意输入

        result = subprocess.run(
            ['python', code_path],
            check=True,
            capture_output=True,
            text=True,
            input=mock_inputs  # 提供足够多的假输入
        )
        print(result.stdout)
        print("="*50)
    except Exception as e:
        print("代码执行出错:", e)
        return None
    
    custom_actions.add_functions_from_strings(
        func_str_list = new_actions,
        action_name_list = action_names,
        rebuild_index = True
    )
    return action_names



def induce(query: str, response: str):
    """主流程入口：触发生成、提取并保存动作函数"""
    sys_msg_path = "induce/prompt/system_message_ch.txt"
    instruction_path = "induce/prompt/instruction_ch.txt"
    few_shot_path = "induce/prompt/induce_action_ch.md"
    write_action_path = "actions/store.py"
    query = test_query(query, response)

    # 创建响应输出目录
    output_dir = os.path.join("outputs")  # Create the base outputs directory
    os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists
    output_file = os.path.join(output_dir, "action.txt")  # Full file path
    code_path = os.path.join(output_dir, "action.py") 

    # 调用 API 获取响应
    responses = induce_actions(
        sys_msg_path=sys_msg_path, 
        instruction_path=instruction_path, 
        few_shot_path=few_shot_path, 
        test_query=query,
        output_path=output_file
    )

    extract_and_write_actions(
        response=responses, 
        write_action_path = write_action_path,
        code_path = code_path
    )
