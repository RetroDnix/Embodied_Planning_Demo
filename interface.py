from prompt_handler import code_planning
import json


def chat(self, task, use_stram=False):
        prompt = (
            "请根据任务信息制定一个任务计划:\n"
            f"{json.dumps(task, indent=4)}"
        )
        self.history.append(
            {
                "role": "user",
                "content": prompt
            }
        )
        response = code_planning(self.history, prompt, use_stram=use_stram, print_log=False)
        self.history.append(
            {
                "role": "assistant",
                "content": response
            }
        )
        return response.choices[0].message.content
if __name__ == "__main__":
    planner = CodePlanner()
    task_info = {
        "task":"制定一个五一出行规划",
        "sub_task":["寻找电梯", "进入电梯"]
    }
    print(planner.chat(task_info))