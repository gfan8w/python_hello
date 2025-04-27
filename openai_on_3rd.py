import os

from dotenv import load_dotenv
from openai import OpenAI

print("start to run")

# 加载 .env 文件
load_dotenv()
api_key = os.getenv("API_KEY")

SYS_PROMPT = """
You are an AI Assistant that tells people what activities they can do based on the weather.
When responding, you don't need to provide the weather information in the response.
Just depending on the overall weather, suggest the activities.
"""

# 初始化OpenAI客户端
# client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

client = OpenAI(base_url="https://aiyjg.lol/v1",
    api_key='sk-rF9sNrGfZgOOcE549OkAJCZT3JsyDvAwOMtlLAMoswteseII',
    timeout=120)

mode = "o1"  # deepseek-r1

assistant = client.beta.assistants.create(
    name="aaa",
    instructions=SYS_PROMPT,
    model=mode,
    temperature=1.0,
)
print("Assistant created successfully!", assistant.id)

completion = client.chat.completions.create(
    model="o1",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
    messages=[
        {'role': 'user', 'content': '9.9和9.11谁大'}
    ]
)

# 通过reasoning_content字段打印思考过程
# print("思考过程：")
# print(completion.choices[0].message.reasoning_content)

# 通过content字段打印最终答案
print("最终答案：")
print(completion.choices[0].message.content)