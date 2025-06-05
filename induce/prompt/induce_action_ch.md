## Task: 帮我把草莓放进冰箱

### Original solution:
```python
def solution():
    # Stage 1: 检查冰箱是否打开
    if not check("fridge_open"):
        open("fridge")  # 使用 open 动作打开冰箱

    # Stage 2: 检查是否找到草莓
    if not find("strawberry"):
        explore("kitchen")  # 使用 explore 动作搜寻草莓
        pick_up("strawberry")  # 使用 pick_up 动作拿起草莓

    # Stage 3: 将草莓放入冰箱
    place("strawberry", "fridge")  # 使用 place 动作将草莓放入冰箱

    # Stage 4: 检查草莓是否已经在冰箱
    if check("strawberry_in_fridge"):
        close("fridge")  # 使用 close 动作关上冰箱门
```

## Reusable Functions
```python
def store_item_in_fridge(item: str):
    """如果物品尚未放入冰箱，则将其存放进去

    Examples:
        store_item_in_fridge("strawberry")
    """
    # Stage 1: 确保冰箱是打开的
    if not check("fridge_open"):
        open("fridge")  # 使用 open 动作打开冰箱
    
    # Stage 2: 如果找不到该物品，则先寻找
    if not find(item):
        explore("kitchen")  # 搜索厨房（或其他适当区域）以找到该物品
        pick_up(item)  # 拿起物品
    
    # Stage 3: 将该物品放入冰箱
    place(item, "fridge")  # 将物品放入冰箱
    
    # Stage 4: 检查物品是否已经在冰箱中，若是，则关闭冰箱
    if check(f"{item}_in_fridge"):
        close("fridge")  # 使用 close 动作关闭冰箱
    else:
        print(f"无法将 {item} 存放进冰箱。")  # 记录失败日志



```

## Rewritten Trajectories
```
def solution():
    # Stage 1: 把草莓放进冰箱
    store_item_in_fridge("strawberry")
```
