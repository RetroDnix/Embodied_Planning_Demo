# 示例：调用 code_planning 函数
from prompt_handler import code_planning
# 假设这是你要传入的对话消息列表
messages = [
    {"role": "user", "content": "帮我下楼去一个快递"},
]

# 调用函数得到一个生成结果（通常是一个生成的流对象，这里简单打印返回的内容或提示）
response_stream = code_planning(messages)

# 假设response_stream是一个可迭代的流式响应，你可以这样处理（示例）：
all_text = ""

for chunk in response_stream:
    # 这里根据你用的API具体字段结构调整，这里假设是类似OpenAI的结构：
    # chunk.choices[0].delta.content
    content = getattr(chunk.choices[0].delta, "content", None)  # 取文本内容
    if content:
        all_text += content
        print(content, end="")  # 也可以边打印边输出，不换行

print("\n")  # 最后换行

# 如果函数返回的是字符串（异常时），直接打印
if isinstance(response_stream, str):
    print(response_stream)