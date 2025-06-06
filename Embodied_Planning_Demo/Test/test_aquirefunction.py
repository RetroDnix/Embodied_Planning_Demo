import sys
sys.path.append('D:/25/em/Embodied_Planning_Demo-sqzhou/Embodied_Planning_Demo')
from custiom_action_set import CustomActionSet

function = '''
def solution():
    # Step 1: 准备并加载衣物进洗衣机
    prepare_and_load_clothes()
    
    # Step 2: 洗衣操作
    wash_clothes()

    # Step 3: 等待洗衣机完成工作
    while not check("washing_completed"):
        wait(1000)

    # Step 4: 取出衣物并晾晒或烘干
    remove_and_dry_clothes()
'''

action_set = CustomActionSet(
    retrievable_actions=True,
    use_API=True
)

functions = action_set.get_function_bodies_from_code(function)

for func in functions:
    print(func)