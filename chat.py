import os

from dotenv import load_dotenv
from openai import OpenAI
import json

print("start to run")

# 加载 .env 文件
load_dotenv()
api_key = os.getenv("API_KEY")



# 初始化OpenAI客户端
client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# Round 1

messages = [{"role": "user", "content": "What's the highest mountain in the world?"}]
response = client.chat.completions.create(
    model="deepseek-r1",
    messages=messages
)

messages.append(response.choices[0].message)

# 将 response 对象及其嵌套对象转换为字典
def convert_to_dict(obj):
    if isinstance(obj, list):
        return [convert_to_dict(i) for i in obj]
    elif hasattr(obj, "__dict__"):
        obj_dict = obj.__dict__.copy()
        for key, value in obj_dict.items():
            obj_dict[key] = convert_to_dict(value)
        return obj_dict
    else:
        return obj

response_dict = convert_to_dict(response)

# 格式化输出字典
formatted_response = json.dumps(response_dict, indent=4, ensure_ascii=False)
print(formatted_response)


messages.append(response.choices[0].message)
print(f"Messages Round 1: {messages}")

# Round 2
messages.append({"role": "user", "content": "What is the second?"})
response = client.chat.completions.create(
    model="deepseek-r1",
    messages=messages
)

messages.append(response.choices[0].message)
print(f"Messages Round 2: {messages}")


# 请你实现 多轮对话功能，但是需求是
# 1 最多只保留5轮对话
# 2 每轮对话的输入和输出使用中文
