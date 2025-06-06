api_tools = """
# 基础的机器人api，用于完成一些简单动作

def check(condition: str)->bool:
    # 检查环境是否满足某个条件
    # True：满足 False：不满足
    return vlm_check(conditon)
    
def find(obj: str)->bool:
    # 在环境中寻找某个物体
    # True：找到 False：没找到
    return vlm_find(conditon)
    
def execute(command: str)->None:
    # 使用下层VLA模型执行任意简单动作
    vla(command)

# 上层api，用于调用基础api完成较复杂动作

def go_downstairs(arrived_floor: str)->None:
    # 执行下楼动作，到达楼层为arrived_floor
    while not check("at_" + arrived_floor + "_floor"):  # 检查是否在一楼
        execute("take_stairs_down")
"""