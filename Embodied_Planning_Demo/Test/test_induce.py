import sys
sys.path.append('D:/25/em/Embodied_Planning_Demo-sqzhou/Embodied_Planning_Demo')
from induce.induce_actions import induce
query = "帮我收拾一下用餐后的桌面"
response = """
```python
def solution():
    # Stage 1: Locate the dining table
    if not find("dining_table"):
        execute("search_for_table")
        wait(500)  # Wait to ensure table is located

    # Stage 2: Clear leftover food from the table
    while find("leftover_food"):
        execute("clear_leftover_food_from_table")

    # Stage 3: Remove plates and utensils from the table
    while find("plate") or find("utensil"):
        execute("remove_plate_from_table")
        execute("remove_utensils_from_table")

    # Stage 4: Wipe the table surface
    if find("dirty_surface"):
        execute("wipe_table_surface")

    # Stage 5: Arrange chairs if they are not well positioned
    if not check("chairs_are_well_positioned"):
        execute("arrange_chairs")

    # Stage 6: Inspect table to ensure cleanliness
    if not check("table_is_clean"):
        execute("repeat_cleaning_procedure")


solution()
```
"""
induce(query, response)