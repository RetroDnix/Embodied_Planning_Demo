prompt_eval = """
An agent has divived a task into subtasks. The devision may be delivered using Natural Language or Python Codes.

Your task is to score the completeness of the division.

When we say a division is "complete", we mean that if all subtasks are executed correctly, the original task can be solved.

The scores can be 0,1,2,3, the description of the scores are as follows:
0: The division doesn't make sense, it is not related to the original task.
1: The division is incomplete, and lacks major part to solve the original task(e.g. forget to add water when making tea).
2: The division is mostly complete, but there are some detail parts missing(e.g. forget to unplag fuel gun when refueling the car).
3: The division is complete, all parts are included and can solve the original task.

Now, give the real division and the original task, your task is to score the completeness of the division. Only return a single number, which is the score of the division.
"""

prompt_compare = """
An agent has divived a task into subtasks. The devision may be delivered using Natural Language or Python Codes.

Your task is to compare the completeness of 2 divisions of a same task, and give each division a score.

When we say a division is "complete", we mean that if all subtasks are executed correctly, the original task can be solved.

To calc the score, you need to consider the following 2 aspects:

1. [Details]The division which focus on more detailed actions gets 1 score.
2. [Possibilities]The division which considers more possibilities gets 1 score.

For each aspect, choose a division(division A or division B) which best follows the description.

The output format is as follows:
1. [Details] Division _(A/B)
2. [Possibilities] Division _(A/B)

Don't return any other information.
"""

import openai
GPT_MODEL = 'gpt-4o'

OPENAI_API_KEY = "sk-DRxEVD9NJPfTNZn9852f350063B249Dc9aD49503B1Ad70Ad"
OPENAI_API_BASE = "http://vip.ooo.cool/v1"

client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

def evaluate(task, division):
    try:
        formatted_messages = [
            {"role": "system", "content": prompt_eval},
            {"role": "user", "content": f"Task: {task}\nDivision: {division}"}
        ]

        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages = formatted_messages,
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"生成回复时出错: {str(e)}"

def compare(task, division_a, division_b):
    try:
        formatted_messages = [
            {"role": "system", "content": prompt_compare},
            {"role": "user", "content": f"Task: {task}\nDivision A: {division_a}\nDivision B: {division_b}"}
        ]
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages = formatted_messages,
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"生成回复时出错: {str(e)}"

example_task = "任务：给汽车加油"
example_divisionA = """
def refuel_car():
    # Stage 1：检查是否在加油站
    if not check("at_gas_station"):
        execute("drive_to_nearest_gas_station")  # 如果不在加油站，则开车到最近的加油站

    # Stage 2：找到加油机
    found_pump = False
    max_attempts = 3  # 限制最多尝试3次
    attempts = 0

    while not found_pump and attempts < max_attempts:
        if find("fuel_pump"):
            found_pump = True
        else:
            execute("search_area_for_fuel_pump")
        attempts += 1

    if not found_pump:
        execute("notify_user_no_fuel_pump_found")  # 如果未找到加油机，通知用户
        return  # 退出方案

    # Stage 3：检查汽车油箱是否已打开
    if not check("fuel_tank_open"):
        execute("open_fuel_tank")  # 如果油箱未打开，则打开油箱

    # Stage 4：加油
    execute("start_refueling")

    # Stage 5：检查加油是否完成
    while not check("refueling_complete"):
        execute("continue_refueling")  # 继续加油直到完成

    # Stage 6：关闭油箱
    execute("close_fuel_tank")

    # Stage 7：支付费用
    if check("payment_required"):
        execute("pay_for_fuel")  # 如果需要支付费用，则支付

    # Stage 8：离开加油站
    execute("drive_away_from_gas_station")
"""

example_divisionB = """
确定当前油量和需要加的油量。
找到最近的加油站。
驶向加油站。
找到合适的加油泵。
停车并熄火。
打开油箱盖。
选择油品类型。
插入加油枪到油箱口。
开始加油。
监控加油过程直到达到所需油量。
完成加油后，取出加油枪。
关闭油箱盖。
支付加油费用。
收集收据（如果需要）。
"""

from argparse import ArgumentParser
if __name__ == "__main__":
    parser = ArgumentParser(description="Evaluate the completeness of a task division.")
    parser.add_argument("--task", type=str, default=example_task, help="The original task to be evaluated.")
    parser.add_argument("--divisionA", type=str, default=example_divisionA, help="The division of the task to be evaluated.")
    parser.add_argument("--divisionB", type=str, default=example_divisionB, help="The division of the task to be evaluated.")
    
    scoreA = 0
    scoreB = 0
    args = parser.parse_args()
    print("Evaluating the task division...")

    response1 = evaluate(args.task, args.divisionA)
    response2 = evaluate(args.task, args.divisionB)
    response3 = compare(args.task, args.divisionA, args.divisionB)

    scoreA = int(response1.strip())
    scoreB = int(response2.strip())
    print("BaseScoreA:", scoreA)
    print("BaseScoreB:", scoreB)

    print("")
    print("Addtional scores...")
    result = response3.splitlines()
    aspect = ["Details", "Possibilities"]
    for idx,line in enumerate(result):
        if "Division A" in line:
            scoreA += 1
            print("Division A gets 1 score for", aspect[idx])
        elif "Division B" in line:
            scoreB += 1
            print("Division B gets 1 score for", aspect[idx])
    
    print("")
    print("Final Score A:", scoreA)
    print("Final Score B:", scoreB)
    print("")

    print("-" * 25 + " Debug Info " + "-" * 25)
    print(response1, response2, response3, sep="\n\n")
    print("-" * 62)