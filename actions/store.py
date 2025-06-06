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

def ensure_resource_availability(resource: str, check_interval: int = 300):
    """在资源可用之前，持续检查。

    Examples:
        ensure_resource_availability("package_arrived", 300)
    """
    while not check(resource):  # 检查资源是否可用
        wait(check_interval)  # 如果不可用，等待指定的时间间隔

def find_resource_location(resource: str, area: str):
    """寻找资源的位置并返回位置标识符。

    Examples:
        location = find_resource_location("package", "floor")
    """
    if find(resource):  # 检查是否能找到资源区域
        return f"{resource}_area"
    else:
        explore(area)  # 探索指定区域以找到资源
        return f"found_{resource}_area"

def retrieve_item(item: str, area: str, location: str):
    """从指定位置检索物品

    Examples:
        retrieve_item("package", "1st_floor", "package_area")
    """
    # 在指定的位置接收物品
    retrieve_item_from_location(item, area, location)