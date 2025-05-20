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




def prepare_coffee(item: str):
    """准备并泡一杯指定类型的咖啡。

    Args:
        item (str): 咖啡类型

    Returns:
        bool: 成功则返回True，否则返回False

    Examples:
        prepare_coffee("black_coffee")
    """
    # 检查咖啡机是否准备就绪
    if not check("coffee_machine_ready"):
        execute("prepare_coffee_machine")
    
    # 确保咖啡杯已放入
    if not check("cup_in_place"):
        execute("place_cup_in_coffee_machine")

    # 选择咖啡类型
    if not check("coffee_type_selected"):
        execute(f"select_{item}")

    # 开始冲泡过程
    execute("start_brewing_coffee")

    # 一直检查直到冲泡完成
    while not check("brewing_complete"):
        wait(1000)  # 等待一段时间再检查

    # 移除咖啡杯
    execute("remove_cup_from_coffee_machine")

    return True


def customize_coffee():
    """根据用户的偏好对咖啡进行自定义。
    
    Examples:
        customize_coffee()
    """
    # 检查是否用户需要糖或牛奶
    if vlm_check("do you want sugar or milk"):
        # 检索用户偏好
        preference = vla("get user preference for sugar or milk")
        # 根据偏好来添加糖或牛奶
        if preference == "sugar":
            execute("add_sugar")
        elif preference == "milk":
            execute("add_milk")
        elif preference == "both":
            execute("add_sugar")
            execute("add_milk")

def make_coffee():
    # 步骤 1：准备黑咖啡
    if prepare_coffee("black_coffee"):
        # 步骤 2：根据用户偏好自定义咖啡
        customize_coffee()

    # 完成泡咖啡过程
    print("您的咖啡已准备好享用!")

def prepare_iced_coffee(coffee_type: str):
    """准备一种类型的冰咖啡

    Args:
        coffee_type (str): 热咖啡的类型，例如"americano"或"espresso"
        
    Returns:
        bool: 如果成功准备冰咖啡返回True，否则返回False

    Examples:
        prepare_iced_coffee("americano")
    """
    # 准备热咖啡
    coffee_prepared = prepare_coffee(coffee_type)
    if not coffee_prepared:
        print(f"无法准备{coffee_type}咖啡")
        return False

    # 加入冰块直到杯子约满1/3
    while not check("enough_ice_in_glass"):
        execute("fetch_ice_into_glass")

    # 将热咖啡倒入装有冰的杯子中
    execute(f"pour_{coffee_type}_into_glass")

    # 加入冷水直到杯子满
    while not check("glass_is_full"):
        execute("pour_cold_water_into_glass")

    print(f"{coffee_type.capitalize()}冰咖啡准备完成")
    return True

def brew_iced_americano():
    # Stage 1：准备一杯冰美式咖啡
    if not prepare_iced_coffee("americano"):
        raise Exception("无法准备美式咖啡")
    

def prepare_and_load_clothes():
    """整理衣物并放入洗衣机
    
    Examples:
        prepare_and_load_clothes()
    """
    # Sorting clothes if not already sorted
    if not check("clothes_sorted"):
        execute("sort_clothes_by_color_or_material")

    # Locate washing machine if not found
    if not find("washing_machine"):
        execute("locate_washing_machine")

    # Open washing machine and add clothes
    if not check("washing_machine_open"):
        execute("open_washing_machine")
    execute("add_clothes_to_washing_machine")

def wash_clothes():
    """添加洗涤剂，选择洗涤模式，启动洗衣机

    Examples:
        wash_clothes()
    """
    # Add detergent if not added
    if not check("detergent_added"):
        execute("add_detergent_to_washing_machine")
    
    # Select wash mode if not selected
    if not check("wash_mode_selected"):
        execute("select_wash_mode")
    
    # Start the washing machine
    execute("start_washing_machine")

def remove_and_dry_clothes():
    """把衣服从洗衣机里拿出来晾干

    Examples:
        remove_and_dry_clothes()
    """
    # Remove clothes from washing machine
    execute("remove_clothes_from_washing_machine")

    # Find drying place if needed
    if not find("clothes_drying_place"):
        execute("locate_clothes_drying_place")
    
    # Dry clothes using suitable method
    if check("has_drying_machine"):
        execute("use_drying_machine_to_dry_clothes")
    else:
        execute("hang_clothes_to_air_dry")



def wash_and_dry_clothes():
    """整理、洗涤和晾干衣物的流程

    This function handles the process of washing and drying clothes.

    Args:
        None

    Returns:
        None

    Examples:
        wash_and_dry_clothes()
    """
    # 整理衣物
    execute("prepare_clothes_for_wash")
    
    # 准备并装载衣物到洗衣机
    execute("prepare_and_load_clothes")
    
    # 启动洗衣程序
    execute("wash_clothes")
    
    # 洗完后进行衣物晾干
    execute("remove_and_dry_clothes")

def make_coffee_process(coffee_type: str):
    """进行咖啡的制作和自定义工作流程

    Args:
        coffee_type (str): 需要准备的咖啡种类

    Returns:
        str: 制作完成后的通知信息

    Examples:
        make_coffee_process("americano")
    """
    # 检查并准备热咖啡
    if not prepare_coffee(coffee_type):
        raise Exception(f"Failed to prepare hot {coffee_type}")

    # 检查并准备冰咖啡
    if not prepare_iced_coffee(coffee_type):
        raise Exception(f"Failed to prepare iced {coffee_type}")

    # 根据用户的偏好自定义咖啡
    customize_coffee()
    
    return f"Iced {coffee_type.capitalize()} is ready!"

def prepare_coffee_drink(drink_type: str):
    """准备特定类型的咖啡饮品并根据情况进行定制

    Args:
        drink_type (str): 需要准备的饮品类型

    Examples:
        prepare_coffee_drink("cappuccino")
    """
    # 检查是否有咖啡豆
    if not find("coffee_beans"):
        execute("get_coffee_beans")
    
    # 制作咖啡饮品
    execute(f"make_{drink_type}")
    
    # 根据情况进行定制
    execute(f"customize_{drink_type}")
    
    # 检查咖啡饮品是否准备好
    if check(f"{drink_type}_ready"):
        execute(f"serve_{drink_type}")
    else:
        print(f"无法制作 {drink_type}。")  # 记录失败日志

def prepare_and_wash_clothes():
    """准备、分类并进行洗涤流程

    Args:
        None

    Returns:
        None

    Examples:
        prepare_and_wash_clothes()
    """
    # 准备要洗的衣物（分类）
    execute("prepare_clothes_for_wash")

    # 整理衣物并放入洗衣机
    execute("prepare_and_load_clothes")

    # 启动洗涤流程
    execute("wash_clothes")

    # 取出并晾干衣物
    execute("remove_and_dry_clothes")

def prepare_and_customize_coffee(drink_type: str, preferences: list):
    """准备咖啡并根据用户偏好定制

    Args:
        drink_type (str): 要准备的咖啡类型
        preferences (list): 用户偏好设置列表

    Returns:
        str: 操作完成的消息

    Examples:
        prepare_and_customize_coffee("cappuccino", ["extra_hot", "no_sugar"])
    """
    # 第一步：准备指定类型的咖啡饮品
    execute(f"prepare_{drink_type}_drink")

    # 第二步：根据偏好定制咖啡
    for preference in preferences:
        execute(f"customize_coffee_{preference}")

    return "咖啡已准备并根据用户偏好定制。"

def setup_and_prepare_coffee(coffee_type: str):
    """配置必要设备并开始准备特定类型的咖啡饮品

    Args:
        coffee_type (str): 要准备的咖啡饮品类型
    
    Examples:
        setup_and_prepare_coffee("cappuccino")
    """
    # 确保咖啡机是可用的
    if not check("coffee_machine_available"):
        execute("setup_coffee_machine")

    # 开始准备指定类型的咖啡
    execute(f"prepare_{coffee_type}")

def customize_coffee(coffee_type: str):
    """根据用户需求定制特定类型的咖啡饮品

    Args:
        coffee_type (str): 要定制的咖啡饮品类型
        
    Examples:
        customize_coffee("cappuccino")
    """
    # 开始为该咖啡饮品定制
    execute(f"customize_{coffee_type}")

def place_coffee(coffee_type: str):
    """将准备好的咖啡饮品放到合适的位置

    Args:
        coffee_type (str): 要摆放的咖啡饮品类型
        
    Examples:
        place_coffee("cappuccino")
    """
    # 放置指定位置的咖啡
    execute(f"place_{coffee_type}_at_designated_area")

def prepare_cappuccino():
    # Stage 1：准备并定制卡布奇诺咖啡
    prepare_coffee("cappuccino")

# 调用函数来执行任务
prepare_cappuccino()

def ensure_item_ready_and_place(item: str, preparation_func: str, retry_cmd: str):
    """确保某样物品准备好并放置到合适的位置

    Examples:
        ensure_item_ready_and_place("cappuccino", "prepare_cappuccino", "retry_prepare_cappuccino")
    """
    # 制作物品
    execute(preparation_func)
    
    # 检查物品是否准备好
    if check(f"{item}_ready"):
        # 将准备好的物品进行放置
        execute(f"place_{item}")
    else:
        # 若物品未准备好，则重试
        execute(retry_cmd)

def order_cappuccino():
    # 确保卡布奇诺已准备好并放置
    ensure_item_ready_and_place("cappuccino", "prepare_cappuccino", "retry_prepare_cappuccino")

order_cappuccino()

def prepare_feeding_area_for_dog():
    """确保喂食区域准备就绪，包括找到狗、将碗放在旁边和填充狗食

    Examples:
        prepare_feeding_area_for_dog()
    """
    # 检查狗是否在附近
    if not find("dog"):
        execute("locate_dog")
    
    # 检查狗碗是否在狗附近
    if not find("dog_bowl_near_dog"):
        execute("move_dog_bowl_near_dog")

    # 检查狗碗中是否有食物
    if not check("food_in_dog_bowl"):
        execute("fetch_dog_food")
        execute("fill_dog_bowl_with_food")

def feed_dog():
    # 确保喂食区域准备就绪
    prepare_feeding_area_for_dog()
    
    # 确保狗开始进食
    if not check("dog_is_eating"):
        execute("call_dog_to_bowl")

def prepare_and_feed_pet(pet: str):
    """准备好喂食区域并喂宠物

    Examples:
        prepare_and_feed_pet("dog")
        prepare_and_feed_pet("cat")
    """
    # 确保喂食区域准备好
    if not check(f"{pet}_feeding_area_ready"):
        execute(f"prepare_feeding_area_for_{pet}")
    
    # 喂宠物
    execute(f"feed_{pet}")

def navigate_and_handle_package(target_floor: str):
    """导航到目标楼层并处理包裹的获取和返回

    Examples:
        navigate_and_handle_package("package_floor")
    """
    # 确保我们当前在目标楼层
    if not check(f"at_{target_floor}"):
        execute(f"navigate_to_{target_floor}")
    
    # 在快递柜中导航并检索包裹
    execute("navigate_and_retrieve_package")
    
    # 确保包裹已经成功取出
    if not check("package_retrieved"):
        print("没有找到快递柜或者快递不在快递柜中。")  # 记录失败日志
    
    # 返回到原来的楼层
    execute("navigate_to_original_floor")
    
    # 确保已回到原始楼层
    if not check("at_original_floor"):
        print("没有成功返回原始楼层。")  # 记录失败日志