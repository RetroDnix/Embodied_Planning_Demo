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
    while not check("at_" + arrived_floor + "_floor"):  # 检查是否在一楼
        execute("take_stairs_down")

def prepare_clothes_for_wash():
    """Prepare clothes for washing by sorting them
    
    Examples:
        prepare_clothes_for_wash()
    """
    if not check("clothes_sorted"):
        execute("sort_clothes_by_color_or_material")

def prepare_washing_machine():
    """Prepare the washing machine by locating and opening it
    
    Examples:
        prepare_washing_machine()
    """
    if not find("washing_machine"):
        execute("locate_washing_machine")

    if not check("washing_machine_open"):
        execute("open_washing_machine")



def navigate_and_retrieve_package():
    """在快递柜中导航并检索包裹

    确保在快递柜处，打开它，检索包裹，并返回到原来的楼层。

    调用示例:
        navigate_and_retrieve_package()

    Raises:
        Exception: 如果没有找到快递柜或者快递不在快递柜中。
    """
    # 找到快递柜
    if not find("delivery box"):
        raise Exception("无法找到快递柜")
    
    # 到达快递柜所在楼层
    if not check("at_delivery_box_floor"):
        go_downstairs("delivery_box_floor_name_or_number")
    
    # 移动到快递柜前
    while not check("at_delivery_box"):
        execute("move_towards_delivery_box")
    
    # 打开快递柜
    execute("open_delivery_box")
    
    # 检查并取出快递包裹
    if not find("package"):
        raise Exception("快递不在快递柜中")
    execute("take_package_from_delivery_box")
    
    # 返回原来的楼层
    go_downstairs("original_floor_name_or_number")

def navigate_to_target_floor(current_status: str, target_floor: str):
    """确保到达目标楼层

    Args:
        current_status (str): 当前状态标识符，例如‘at_delivery_box_floor’
        target_floor (str): 目标楼层标识符，例如‘delivery_box_floor’

    Examples:
        navigate_to_target_floor("at_delivery_box_floor", "delivery_box_floor")
    """
    if not check(current_status):
        execute(f"go_downstairs({target_floor})")


def find_and_retrieve_item(item_location: str, item: str, search_action: str, retrieve_action: str):
    """找到指定位置的物品并取出

    Args:
        item_location (str): 物品所在位置的识别符，例如‘at_delivery_box’
        item (str): 要检索的物品，例如‘package’
        search_action (str): 寻找物品的动作，例如‘search_for_delivery_box’
        retrieve_action (str): 取出物品的动作，例如‘take_package_from_delivery_box’

    Examples:
        find_and_retrieve_item("at_delivery_box", "package", "search_for_delivery_box", "take_package_from_delivery_box")
    """
    while not check(item_location):
        if not find(item_location):
            execute(search_action)
        execute(f"move_towards_{item_location}")
    
    if not find(item):
        raise Exception(f"{item} 不在当前位置")
    
    execute(retrieve_action)
    

def return_to_original_floor(target_floor: str):
    """返回到初始楼层

    Args:
        target_floor (str): 返回的目标楼层，例如‘original_floor’

    Examples:
        return_to_original_floor("original_floor")
    """
    execute(f"go_downstairs({target_floor})")

def retrieve_package_from_box(target_floor: str, original_floor: str):
    """从快递柜中检索包裹，并返回到原来的楼层

    Args:
        target_floor (str): 快递柜所在楼层（名称或编号）
        original_floor (str): 返回的原始楼层（名称或编号）

    Examples:
        retrieve_package_from_box("1F", "3F")
    """
    # 确定快递柜所在楼层并前往
    go_downstairs(target_floor)

    # 在目标楼层寻找快递柜的位置
    while not find("delivery box"):
        execute("search_for_delivery_box")

    # 在快递柜前面检测
    while not check("at_delivery_box"):
        execute("move_towards_delivery_box")

    # 打开快递柜
    execute("open_delivery_box")

    # 检测包裹是否在快递柜中
    if not find("package"):
        raise Exception("快递不在快递柜中")

    # 从快递柜中取出包裹
    execute("take_package_from_delivery_box")

    # 返回到原来的楼层
    go_downstairs(original_floor)




def find_and_prepare_item(item_location: str, item: str, search_action: str, retrieve_action: str):
    """找到物品并准备它，比如清洗或设置。

    Examples:
        find_and_prepare_item("on_kitchen_counter", "grapes", "search_for_grapes", "take_grapes")
    """
    # 找到和获取物品
    if not find(item_location):
        execute(search_action)
    execute(retrieve_action)
    
def ensure_sufficient_condition_for_cleaning(water_source: str):
    """确保洗涤物品所需的条件足够好。

    Examples:
        ensure_sufficient_condition_for_cleaning("sink_has_water")
    """
    # 检查水槽是否有水
    if not check(water_source):
        execute("turn_on_sink_water")
    
def clean_item_until_done(item_clean_status: str, clean_action: str):
    """清洗物品直到干净

    Examples:
        clean_item_until_done("grapes_are_clean", "wash_grapes")
    """
    # 清洗物品直到状态变为清洗干净
    while not check(item_clean_status):
        execute(clean_action)

def setup_table_and_place_item(item: str, search_table_action: str, place_item_action: str):
    """找到桌子并摆放

    Examples:
        setup_table_and_place_item("table", "search_for_table", "place_plate_on_table")
    """
    # 找到并摆放桌子
    if not find(item):
        execute(search_table_action)
    execute(place_item_action)

def process_clothes():
    """处理衣服：检索、检查褶皱并叠好后放入衣柜。

    Examples:
        process_clothes()
    """
    # 找到和检索衣服
    find("clothes")
    execute("retrieve_clothes")

    # 检查衣服是否有褶皱并进行处理
    if find("wrinkled_clothes"):
        while check("clothes_still_wrinkled"):
            execute("iron_clothes")

    # 叠衣服并放入衣柜
    execute("fold_clothes")
    execute("place_clothes_into_wardrobe")

def organize_clothes(item_type: str):
    """对指定类型的衣物进行分类、检查、并执行适当操作以放入衣柜

    Examples:
        organize_clothes("pants")
        organize_clothes("shirt")
    """
    # 检查是否有衣物需要分类
    if not find("clothes"):
        execute("retrieve_clothes")

    # 检查衣物是否有褶皱，并熨平褶皱
    if find("wrinkled_clothes"):
        while check("clothes_still_wrinkled"):
            execute("iron_clothes")

    # 根据衣物类型进行叠衣操作
    if item_type == "pants":
        execute("fold_pants")
    else:
        execute("fold_shirt")

    # 将叠好的衣物放入衣柜
    execute("place_clothes_into_wardrobe")