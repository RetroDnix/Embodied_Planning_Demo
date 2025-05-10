## Task: 帮我把草莓放进冰箱

### Original solution:
```python
def solution():
    # Stage 1: 检查冰箱是否打开
    if not check("fridge_open"):
        # 如果冰箱没有打开，则打开冰箱
        execute("open_fridge")

    # Stage 2: 检查是否找到草莓
    if not find("strawberry"):
        # 如果没有找到草莓，搜寻草莓
        execute("find_strawberry")

    # Stage 3: 将草莓放入冰箱
    execute("place_strawberry_into_fridge")

    # Stage 4: 检查草莓是否已经在冰箱
    if check("strawberry_in_fridge"):
        # 如果草莓已经在冰箱中，关上冰箱门
        execute("close_fridge")
```

## Reusable Functions
```python
def store_item_in_fridge(item: str):
    """Store an item in the fridge if it's not already inside
    
    Examples:
        store_item_in_fridge("strawberry")
    """
    # Ensure the fridge is open
    if not check("fridge_open"):
        execute("open_fridge")
    
    # Find the item if it's not present
    if not find(item):
        execute(f"find_{item}")
    
    # Place the item into the fridge
    execute(f"place_{item}_into_fridge")
    
    # Verify the item is inside and close the fridge
    if check(f"{item}_in_fridge"):
        execute("close_fridge")
    else:
        print(f"Failed to store {item} in the fridge.")  # Logging failure

```

## Rewritten Trajectories
```
def solution():
    # Stage 1: 把草莓放进冰箱
    store_item_in_fridge*("strawberry")
```
