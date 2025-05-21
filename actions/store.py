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



def play_show_on_website(website_url: str, show_name: str, season: int, episode: int):
    """打开指定网站，搜索并播放特定节目的一集

    Examples:
        play_show_on_website("https://www.iqiyi.com", "奔跑吧兄弟", 1, 2)
    """
    # 打开浏览器
    execute("open_browser")
    
    # 导航到指定网站
    execute(f"navigate_to_url {website_url}")
    
    # 搜索指定节目
    execute(f"search_for_show {show_name}")
    
    # 定位到特定的季和集
    execute(f"locate_season {season}")
    execute(f"locate_episode {episode}")
    
    # 播放该集
    execute("play_video")

def prepare_coffee_drink(drink_type: str):
    """准备指定类型的咖啡饮品，如果咖啡机未准备好则进行准备

    Examples:
        prepare_coffee_drink("cappuccino")
    """
    # 验证咖啡机是否准备好了
    if not check("coffee_machine_ready"):
        execute("prepare_coffee_machine")
    
    # 制作饮品
    execute(f"brew_{drink_type}")
    
    # 根据用户的偏好进行调整
    customize_coffee()

def clear_sink():
    """清理洗菜池及其周边

    Examples:
        clear_sink()
    """
    # 移除洗菜池中的所有餐具或杂物
    while find("dish_in_sink"):
        execute("remove_dish_from_sink")

    # 移除洗菜池中的食物残渣
    while find("food_debris_in_sink"):
        execute("remove_food_debris_from_sink")
    
    # 清洁洗菜池表面
    if not check("sink_surface_clean"):
        execute("clean_sink_surface")
    
    # 确保排水口通畅
    if not check("drain_clear"):
        execute("clear_drain")

    # 清理洗菜池周边区域
    if find("water_splotch_near_sink") or find("debris_near_sink"):
        execute("clean_area_around_sink")

def prepare_to_wash(item: str):
    """准备清洗，清理水槽中的杂物并确保有水

    Examples:
        prepare_to_wash("fruit")
    """
    # 确保水槽没有杂物
    if find("debris_in_sink"):
        execute("clear_sink")
    
    # 确保有足够的水
    if not check("enough_water"):
        execute("open_water_tap")
    
    # 如果物品未在水下，则将其放入
    if not check(f"{item}_under_water"):
        execute(f"put_{item}_under_water")

def wash_thoroughly(item: str):
    """彻底清洗物品并关闭水源

    Examples:
        wash_thoroughly("fruit")
    """
    # 完全清洗物品
    execute(f"wash_{item}_thoroughly")
    
    # 检查水龙头是否打开，如果是则关闭
    if check("water_tap_open"):
        execute("close_water_tap")

def wash_fruit():
    # Stage 1: 准备清洗水果
    prepare_to_wash("fruit")
    
    # Stage 2: 完全清洗水果并关闭水源
    wash_thoroughly("fruit")

wash_fruit()

def open_and_search_in_app(app: str, search_item: str) -> bool:
    """打开给定的应用并搜索指定的项目

    Examples:
        open_and_search_in_app("meituan", "霸王茶姬")
    """
    # 打开应用
    execute(f"open_{app}_app")
    
    # 搜索项目
    execute(f"search '{search_item}'")
    
    # 确认搜索结果中是否存在该项目
    return find(f"{search_item}_shop")

def select_and_add_item_to_cart(item: str, with_customization: bool = False) -> bool:
    """选择商品并将其添加到购物车中，必要时进行自定义

    Examples:
        select_and_add_item_to_cart("霸王茶姬_milk_tea", with_customization=True)
    """
    # 浏览菜单并选择商品
    if find(item):
        execute(f"select_product '{item}'")
        
        # 查看是否需要自定义商品
        if with_customization and check("customize_option_available"):
            customize_coffee()  # 调整口味
        
        # 将商品加入购物车
        execute("add_to_cart")
        return True
    else:
        return False

def proceed_with_checkout():
    """检查购物车并进行结账操作

    Examples:
        proceed_with_checkout()
    """
    # 检查购物车确认情况
    if check("in_cart_confirmation"):
        # 进行结账
        execute("proceed_to_checkout")
        
        # 选择支付方式并支付
        execute("select_payment_method")
        execute("confirm_payment")

def purchase_item_on_meituan(item: str, with_customization: bool = False):
    """在美团上购买指定的物品，并处理选择逻辑

    Examples:
        purchase_item_on_meituan("沪上阿姨_milk_tea")
        purchase_item_on_meituan("奶茶", with_customization=True)
    """
    # 查找物品并添加至购物车
    item_found = select_and_add_item_to_cart(item, with_customization)
    
    # 检查物品是否成功添加到购物车
    if item_found:
        # 从购物车核实，假设不需要额外定制，如果设置为True，则自定义
        if with_customization:
            execute("customize_item", item)
    else:
        print(f"无法找到物品 {item}，请检查商品是否存在。")  # 记录失败日志