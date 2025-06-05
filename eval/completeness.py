prompt = """
An agent has divived a task into subtasks. Your task is to evaluate if the division is a complete one.

When we say a division is "complete", we mean that if all subtasks are executed correctly, the original task can be solved.

For example, if the original task is "fuel charging", a complete division could be:
1. Get the fuel charging cable.
2. Plug the cable into the fuel port.
3. Wait for the fuel to charge.
4. Unplug the cable from the fuel port.

and a non-complete division could be:
1. Get the fuel charging cable.
2. Plug the cable into the fuel port.
3. Wait for the fuel to charge.
This division forget to unplug the cable from the fuel port, which is necessary to solve the original task.

Note that a division can also be presented using python code,for example:

```python
# 任务：下楼找到红色包装外卖并取回

def solution():
    # Stage 1：选择下楼方式
    if check("elevator_available"):
        execute("take_elevator_down")  # 如果电梯可用，则使用电梯
    else:
        execute("take_stairs_down")  # 否则使用楼梯
    
    # Stage 2：在一楼寻找红色包装的外卖
    found = False
    max_attempts = 5  # 限制最多尝试5次
    attempts = 0
    
    while not found and attempts < max_attempts:
        if find("red_package"):
            found = True
        else:
            execute("search_area_for_red_package")
        attempts += 1
    
    if not found:
        execute("return_home")  # 如果未找到，返回楼上
        return  # 退出方案

    # Stage 3：取回外卖
    execute("pick_up_red_package")
    
    # Stage 4：返回楼上
    if check("elevator_available"):
        execute("take_elevator_up")  # 如果电梯可用，则使用电梯
    else:
        execute("take_stairs_up")  # 否则使用楼梯
    
    # Stage 5：将外卖放到桌子上
    execute("place_package_on_table")
```

Using python code, an incomplete division could be:
```python
def solution():
    # Stage 1：选择下楼方式
    if check("elevator_available"):
        execute("take_elevator_down")  # 如果电梯可用，则使用电梯
    else:
        execute("take_stairs_down")  # 否则使用楼梯
    
    # Stage 2：在一楼寻找红色包装的外卖
    found = False
    max_attempts = 5  # 限制最多尝试5次
    attempts = 0
    
    while not found and attempts < max_attempts:
        if find("red_package"):
            found = True
        else:
            execute("search_area_for_red_package")
        attempts += 1
    
    if not found:
        execute("return_home")  # 如果未找到，返回楼上
        return  # 退出方案

    # Stage 3：取回外卖
    execute("pick_up_red_package")
    
    # Stage 4：将外卖放到桌子上
    execute("place_package_on_table")
```

This division forget to return to the upstairs, which is necessary to solve the original task.

Now, give the real division and the original task, your task is to evaluate if the division is a complete one. Just output "complete" or "incomplete" without any other text.
"""

import openai
GPT_MODEL = 'gpt-4o'

OPENAI_API_KEY = "sk-DRxEVD9NJPfTNZn9852f350063B249Dc9aD49503B1Ad70Ad"
OPENAI_API_BASE = "http://vip.ooo.cool/v1"

client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

def evaluate(task, division):
    try:

        formatted_messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Task: {task}\nDivision: {division}"}
        ]

        return client.chat.completions.create(
            model=GPT_MODEL,
            messages = formatted_messages,
            temperature=0.0
        )
    except Exception as e:
        return f"生成回复时出错: {str(e)}"

example_task = "任务：给汽车加油"
example_division = """
def check_fuel_level():
    # Stage 1：检查汽车的燃油水平
    if check("fuel_level_full"):
        execute("notify_user_fuel_full")  # 如果燃油已满，通知用户并退出方案
        return False
    return True

def locate_gas_station():
    # Stage 2：寻找最近的加油站
    if not find("gas_station"):
        execute("search_for_gas_station")  # 如果未找到加油站，开始寻找
    while not check("gas_station_found"):
        execute("wait")  # 等待直到找到加油站

def refuel_car():
    # Stage 3：给汽车加油
    execute("park_car_at_gas_pump")  # 将汽车停在加油泵旁
    execute("start_refueling")  # 开始加油
    while not check("refueling_complete"):
        execute("wait")  # 等待直到加油完成

def pay_for_fuel():
    # Stage 4：支付加油费用
    execute("pay_for_fuel")  # 支付加油费用

def solution():
    if not check_fuel_level():
        return  # 如果燃油已满，退出方案

    locate_gas_station()  # 寻找加油站
    refuel_car()  # 给汽车加油
    pay_for_fuel()  # 支付加油费用

solution()
"""

from argparse import ArgumentParser
if __name__ == "__main__":
    parser = ArgumentParser(description="Evaluate the completeness of a task division.")
    parser.add_argument("--task", type=str, default=example_task, help="The original task to be evaluated.")
    parser.add_argument("--division", type=str, default=example_division, help="The division of the task to be evaluated.")
    
    args = parser.parse_args()
    
    response = evaluate(args.task, args.division)

    print("Evaluating the task division...")
    print("Task:\n", args.task)
    print("Division:\n", args.division)
    
    print("Response:", response.choices[0].message.content.strip())