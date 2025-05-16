from custiom_action_set import CustomActionSet

custom_actions = CustomActionSet(
    retrievable_actions=True,
    use_API=True
)
# 1. 获取所有动作的描述
description = custom_actions.describe(
    retrieval_query = "下楼梯给我取一个快递",
    num_retrieve = 5
)
# #非检索
# custom_actions = CustomActionSet(retrievable_actions=False)
# description = custom_actions.describe(
#     with_long_description=True,
#     with_examples=True
# )
print(description)

