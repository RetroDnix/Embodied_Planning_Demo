# from tools import api_tools
# from custiom_action_set import CustomActionSet
# custom_actions = CustomActionSet(retrievable_actions=False)
# api_tools = custom_actions.describe(
#     with_long_description=True,
#     with_examples=True
# )

NL_sys_prompt = """
你是一个智能机器人的高级规划者，请将复杂的任务分解为简单且易于执行的子任务。
"""

code_example = """
# 任务：制作一杯加冰的雪碧，同时加入柠檬片和薄荷叶。

def solution():
    # Stage 1： 向杯子中加入冰块直到1/3的位置
    while not check("enough_ice_in_glass"): # 向杯子内加入冰块直到足够
        execute("fetch_ice_into_glass")

    # Stage 2： 向杯子中加入雪碧直到杯子几乎盛满
    while not check("glass_is_full"): # 杯子没有满
        try:
            if check("too_much_foam"): # 如果泡沫太多了就等泡沫消失
                wait(1000)
            else:
                execute("pour_cola_into_glass") # 否则继续倒可乐
        except ExcutingError as e:
            if e == "cola not open"
                execute("open_the_cola")

    # Stage 3：向杯子中放上柠檬片和薄荷
    if not find("Lemon Slice"): # 切柠檬
        execute("slice_the_lemon")

    excute("add_lemon_and_mint") # 加入柠檬片和薄荷

    # Stage 4： 将蓝色的吸管插入杯子中
    execute("put_straw_into_glass") # 放入吸管

"""

code_sys_prompt = """
你是一个智能机器人的高级规划者，你的任务是将复杂的任务分解为简单且易于执行的子任务。

为了让任务的分解更有可执行性，你需要使用Python代码来表示这些子任务。请确保代码是可运行的，并且在每个子任务之间添加注释，以便人类检查你的分解效果。

智能机器人提供以下API：

{api_tools}


以下是一个示例：
{code_example}

你只需要回答生成的Python代码，不需要解释或提供额外的上下文。注意:代码中的注释请使用中文。
"""


