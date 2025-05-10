from custiom_action_set import CustomActionSet

custom_actions = CustomActionSet(
    retrievable_actions=True
)
# 1. 获取所有动作的描述
description = custom_actions.describe(
    retrieval_query = "下楼梯给我取一个快递",
    num_retrieve = 3
)
print(description)

