import sys
sys.path.append('D:/25/em/Embodied_Planning_Demo-sqzhou/Embodied_Planning_Demo')
from custiom_action_set import CustomActionSet

custom_actions = CustomActionSet(
    retrievable_actions=True,
    use_API=True
)
# 1. 获取所有动作的描述
description = custom_actions.describe(
    retrieval_query = "打扫用餐桌面",
    num_retrieve = 5
)

print(description)

