
# 使用API接口:
```
from interface import CodePlanner
planner = CodePlanner()
task_info = {
    "task":"制定一个五一出行规划",
    "sub_task":["寻找电梯", "进入电梯"]
}
print(planner.chat(task_info))
```

