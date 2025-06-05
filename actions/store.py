from actions.base import *
# --------------------------------------------------
# High-Level Task API
# --------------------------------------------------

def go_downstairs(arrived_floor: str) -> None:
    """Navigate robot to specified floor

    Examples:
        go_downstairs("1")
        go_downstairs("basement")
    """
    while not check("at_" + arrived_floor + "_floor"):  # 检查是否在指定楼层
        move("downstairs")  # 向下走楼梯

def prepare_clothes_for_wash():
    """Prepare clothes for washing by sorting them
    
    Examples:
        prepare_clothes_for_wash()
    """
    if not check("clothes_sorted"):  # 检查衣物是否已整理
        pick_up("clothes")  # 拿起衣物
        place("clothes", "sorting_area")  # 将衣物放到整理区
        execute("sort_clothes_by_color_or_material")  # 对衣物进行分类

def retrieve_delivery(location: str, target_floor: str):
    """从指定的楼层接收外卖并放置到目标位置。

    Examples:
        retrieve_delivery("一楼", "指定交付位置")
    """
    # Step 1: 确认外卖是否到达
    if not check("外卖到达"):
        print("外卖尚未到达。")
        return
    
    # Step 2: 如果机器人不在目标楼层，则导航到该楼层
    if not check(f"机器人在{target_floor}"):
        go_downstairs(target_floor)  # 导航到目标楼层

    # Step 3: 确保门是打开的
    if not check("门已打开"):
        open("门")  # 如果门是关闭的，打开门

    # Step 4: 发现和收集外卖
    if not find("外卖"):
        explore(location)  # 在指定位置寻找外卖
        grab("外卖")  # 拿起外卖

    # Step 5: 导航到交付位置并放下外卖
    go_to("指定交付位置")
    put_down("外卖")  # 放下外卖