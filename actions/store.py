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

def cross_street_based_on_traffic():
    """选择合适的方式过马路

    根据交通灯状态选择过马路的方式。

    Args:
        None

    Returns:
        None

    Examples:
        cross_street_based_on_traffic()
    """
    # 根据交通灯状态选择过马路的方式
    if check("traffic_light_green"):
        execute("cross_street_at_crosswalk")
    else:
        execute("use_pedestrian_bridge")

def find_location(location: str, max_attempts: int = 5):
    """寻找指定位置，最大尝试次数限制

    Args:
        location (str): 要寻找的位置的名称。
        max_attempts (int): 最大尝试次数。

    Returns:
        bool: 若找到位置返回True，否则返回False。

    Examples:
        find_location("fruit_stand", 5)
    """
    # 寻找指定位置，并在最大尝试次数范围内寻找
    found = False
    attempts = 0

    while not found and attempts < max_attempts:
        if find(location):
            found = True
        else:
            execute(f"search_area_for_{location}")
        attempts += 1
    
    return found

def buy_items_and_return(item: str):
    """购买指定物品并返回实验室

    示例:
        buy_items_and_return("fruit")
    """
    # 购买指定物品
    execute(f"buy_{item}")
    
    # 返回实验室并在桌子上放置物品
    if check("traffic_light_green"):
        execute("cross_street_at_crosswalk")
    else:
        execute("use_pedestrian_bridge")
    
    execute(f"place_{item}_on_table")

def navigate_floor(action_down: str, action_up: str):
    """根据电梯的可用性选择上下楼方式。

    Args:
        action_down (str): 下楼时的执行操作，如 'elevator' 或 'stairs'
        action_up (str): 上楼时的执行操作，如 'elevator' 或 'stairs'

    Examples:
        navigate_floor("elevator", "stairs")
    """
    if check("elevator_available"):
        execute(f"take_{action_down}_down")  # 使用电梯
    else:
        execute(f"take_stairs_down")  # 使用楼梯

    if check("elevator_available"):
        execute(f"take_{action_up}_up")  # 使用电梯
    else:
        execute(f"take_stairs_up")  # 使用楼梯


def search_and_pick_item(item: str, max_attempts: int):
    """在指定地点查找并取回物品。

    Args:
        item (str): 需要查找的物品
        max_attempts (int): 最大查找次数

    Examples:
        search_and_pick_item("delivery_package", 5)
    """
    found = False
    attempts = 0

    while not found and attempts < max_attempts:
        if find(item):
            found = True
        else:
            execute(f"search_area_for_{item}")
        attempts += 1

    if found:
        execute(f"pick_up_{item}")
    else:
        execute("return_upstairs")  # 查找失败时返回


def place_item_on_surface(item: str, surface: str):
    """将物品放置于指定表面。

    Args:
        item (str): 要放置的物品
        surface (str): 要放置的表面，比如桌子

    Examples:
        place_item_on_surface("delivery_package", "table")
    """
    execute(f"place_{item}_on_{surface}")

def ensure_fridge_state(state: str):
    """确保冰箱处于期望状态（打开或关闭）。

    Args:
        state (str): 期望冰箱的状态，'open'或'closed'。

    Returns:
        None

    Examples:
        ensure_fridge_state("open")
    """
    desired_action = f"{state}_fridge"
    if (state == "open" and not check("fridge_open")) or (state == "closed" and check("fridge_open")):
        execute(desired_action)


def locate_or_find_item(item: str):
    """确保项在当前位置可用，或执行查找操作。

    Args:
        item (str): 要查找的项名称。

    Returns:
        bool: 如果项目可供使用，则返回True，否则执行查找操作并返回False。

    Examples:
        locate_or_find_item("strawberry")
    """
    if not find(item):
        execute(f"find_{item}")
        return False
    return True


def place_item_in_location(item: str, location: str):
    """将特定项放置到目标位置，并验证。

    Args:
        item (str): 要放置的项。
        location (str): 目标位置。

    Returns:
        bool: 如果项目成功放置并已在目标位置中，则返回True，否则返回False。

    Examples:
        place_item_in_location("strawberry", "fridge")
    """
    execute(f"place_{item}_into_{location}")
    if check(f"{item}_in_{location}"):
        return True
    else:
        return False

def plan_trip_stages():
    """为一次旅行制定计划，包括选定目的地、预订交通和住宿等

    示例:
        plan_trip_stages()
    """
    # 确保目的地已选择
    execute_stage("destination_selected", "select_destination")
    
    # 确保交通工具已预订
    execute_stage("transport_booked", "book_transport")
    
    # 确保住宿已预订
    execute_stage("accommodation_booked", "book_accommodation")
    
    # 制定行程
    execute_stage("itinerary_planned", "plan_itinerary")
    
    # 准备行李
    execute_stage("luggage_packed", "pack_luggage")

    # 检查所有预订已确认
    execute_stage("all_bookings_confirmed", "confirm_all_bookings")

    # 检查天气
    execute_stage("weather_checked", "check_weather")

def execute_stage(check_condition: str, action: str):
    """检查条件并执行相应动作

    Args:
        check_condition (str): 检查是否满足指定条件
        action (str): 如果条件不满足，执行的动作

    示例:
        execute_stage("destination_selected", "select_destination")
    """
    if not check(check_condition):
        execute(action)

def prepare_trip(stage_info: dict):
    """根据阶段信息准备旅行

    Args:
        stage_info (dict): 阶段信息字典，键为阶段ID，值为执行动作

    示例:
        prepare_trip({
            "destination_selected": "select_destination",
            "transportation_booked": "book_transportation",
            "accommodation_booked": "book_accommodation",
            "itinerary_planned": "plan_itinerary",
            "luggage_packed": "pack_luggage"
        })
    """
    # 遍历每个阶段并检查是否完成，如果未完成则执行相应操作
    for stage, action in stage_info.items():
        if not check(stage):
            execute_stage(stage, action)
    
    # 检查所有阶段是否完成
    if all(check(stage) for stage in stage_info):
        execute("ready_for_trip")
    else:
        execute("review_and_complete_preparations")

def ensure_trip_preparation():
    """确保旅行准备工作已经完成。

    确保出发前已选择目的地，预订交通与住宿，计划行程并打包行李。
    
    Returns:
        bool: 返回所有准备工作是否完成。
    
    Examples:
        if ensure_trip_preparation():
            execute("start_trip")
        else:
            execute("review_preparation")
    """
    # 检查目的地选择
    if not check("destination_selected"):
        execute("select_destination")
    
    # 检查交通预订
    if not check("transportation_booked"):
        execute("book_transportation")
    
    # 检查住宿预订
    if not check("accommodation_booked"):
        execute("book_accommodation")
    
    # 检查行程计划
    if not check("itinerary_planned"):
        execute("plan_itinerary")
    
    # 检查行李打包
    if not check("luggage_packed"):
        execute("pack_luggage")

    # 检查所有准备工作是否完成    
    return (
        check("destination_selected") and
        check("transportation_booked") and
        check("accommodation_booked") and
        check("itinerary_planned") and
        check("luggage_packed")
    )

def prepare_to_eat():
    """准备吃饭并从桌子上完成用餐。
    
    检查食物是否在桌上，寻找餐具，吃饭并在结束后离桌
    
    Args:
        无
    
    Returns:
        无
    
    Examples:
        prepare_to_eat()
    """
    # 检查是否有食物，并在返回后或确认桌上有食物时就座
    if vlm_check("is there food on the table"):
        execute("sit_at_table")
    else:
        buy_items_and_return("food")
        execute("sit_at_table")
    
    # 寻找并拿起餐具，否则使用手
    if find("cutlery"):
        execute("pick_up_cutlery")
    else:
        execute("search_area_for_cutlery")
        if find("cutlery"):
            execute("pick_up_cutlery")
        else:
            execute("use_hands_to_eat")
    
    # 开始吃饭，直到盘子空了才停止
    execute("start_eating")
    while not vlm_check("is the plate empty"):
        execute("continue_eating")
    
    # 结束用餐并离桌
    execute("put_down_cutlery")
    execute("leave_table")