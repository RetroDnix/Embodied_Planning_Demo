import sys
sys.path.append('D:/25/em/Embodied_Planning_Demo-sqzhou/Embodied_Planning_Demo')
from custiom_action_set import CustomActionSet
from actions import store



function_list = [
    '''def clean_dining_table():
    """执行用餐后的完整清洁过程，包括找到桌子、清理食物、移除盘子和餐具、擦拭表面、以及整理座椅。

    Args:
        None
    
    Returns:
        None
    
    Examples:
        clean_dining_table()
    """
    # 确保找到餐桌
    if not find("dining_table"):
        execute("search_for_table")
        wait(500)  # 等待确保找到桌子

    # 清理剩余食物
    while find("leftover_food"):
        execute("clear_leftover_food_from_table")

    # 移除盘子和餐具
    while find("plate") or find("utensil"):
        execute("remove_plate_from_table")
        execute("remove_utensils_from_table")

    # 擦拭桌面
    if find("dirty_surface"):
        execute("wipe_table_surface")

    # 整理椅子
    if not check("chairs_are_well_positioned"):
        execute("arrange_chairs")

    # 检查桌子是否干净，否则重复清理程序
    if not check("table_is_clean"):
        execute("repeat_cleaning_procedure")''',
        
    '''def prepare_dining_table():
    """准备用餐前的桌子布置
    
    Examples:
        prepare_dining_table()
    """
    execute("arrange_chairs")
    execute("place_tableware")
    execute("check_table_cleanliness")'''
]

action_name = [
    "clean_dining_table",
    "prepare_dining_table"

]
# 初始化动作集

action_set = CustomActionSet(
    retrievable_actions=True,
    use_API=True
)

# 批量添加函数
action_set.add_functions_from_strings(
    func_str_list = function_list,
    action_name_list = action_name,
    rebuild_index = True
    )

description = action_set.describe(
    retrieval_query = "帮我打扫用餐桌面",
    num_retrieve = 5
)

print(description)


