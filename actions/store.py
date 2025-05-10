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

def complete_washing_cycle():
    """Complete the washing cycle, including adding detergent and selecting mode
    
    Examples:
        complete_washing_cycle()
    """
    if not check("detergent_added"):
        execute("add_detergent_to_washing_machine")

    if not check("wash_mode_selected"):
        execute("select_wash_mode")

    execute("start_washing_machine")

    while not check("washing_completed"):
        wait(1000)  # Wait for washing to complete

def dry_clothes():
    """Dry clothes after washing using drying machine or air drying
    
    Examples:
        dry_clothes()
    """
    if not find("clothes_drying_place"):
        execute("locate_clothes_drying_place")

    if check("has_drying_machine"):
        execute("use_drying_machine_to_dry_clothes")
    else:
        execute("hang_clothes_to_air_dry")
