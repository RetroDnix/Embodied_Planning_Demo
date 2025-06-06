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

def move_to_floor(desired_floor: str):
    """确保在期望的楼层上

    Examples:
        move_to_floor("1")
    """
    # 如果不在期望的楼层，则移动到该楼层
    if not check(f"at_{desired_floor}_floor"):
        go_downstairs(desired_floor)  # 下到指定楼层


def find_and_go_to_location(location: str, area: str):
    """寻找并到达指定位置

    Examples:
        find_and_go_to_location("shop", "一楼")
    """
    # 探索区域以找到指定位置
    explore(area)
    # 如果找到位置，则前往该位置
    if find(location):
        go_to(location)


def purchase_item(item: str, purchase_location: str):
    """购买指定物品

    Examples:
        purchase_item("cola", "cashier")
    """
    # 如果找到物品，则进行购买流程
    if find(item):
        grab(item)  # 拿起物品
        if find(purchase_location):
            go_to(purchase_location)  # 前往购买位置
            place(item, "counter")  # 将物品放置在柜台
            execute(f"pay_for_{item}")  # 支付物品费用
    # 购买后，拿起该物品
    pick_up(item)

def navigate_and_purchase(location: str, item: str, delivery_point: str):
    """在指定位置购买物品，并返回交付点

    Examples:
        navigate_and_purchase("shop", "cola", "指定交付位置")
    """
    # Stage 1: 确保机器人移动到指定位置所在的楼层
    move_to_floor("1")  # 假设该位置在一楼
    
    # Stage 2: 找到并前往商店或其他指定地点
    find_and_go_to_location(location, "一楼")  # 设置目标位置和楼层
    
    # Stage 3: 购买指定物品
    purchase_item(item, "cashier")  # 在收银台购买物品
    
    # Stage 4: 返回到指定交付点
    go_downstairs(delivery_point)  # 返回起始楼层或交货位置

def visit_location_and_purchase(item: str, location: str, purchase_spot: str):
    """到指定位置购买物品然后返回初始位置

    Examples:
        visit_location_and_purchase("cola", "shop", "cashier")
    """
    # Step 1: 确认当前位置在期望的楼层
    move_to_floor(location)

    # Step 2: 寻找并到达指定地点
    find_and_go_to_location(item, location)
    
    # Step 3: 购买指定物品
    purchase_item(item, purchase_spot)

    # Step 4: 返回交付地点
    retrieve_delivery(location, "指定交付位置")