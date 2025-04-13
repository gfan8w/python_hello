import os

from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr  

print("start to run")

# 加载 .env 文件
load_dotenv()
api_key = os.getenv("API_KEY")



# 初始化OpenAI客户端
client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

def predict(message, history):
    try:
        history_openai_format = []
        # 将历史对话转换为OpenAI格式
        for human, ai in history:
            history_openai_format.append({"role": "user", "content": human})
            history_openai_format.append({"role": "assistant", "content": ai})
        history_openai_format.append({"role": "user", "content": message})
        # 调试
        print(history_openai_format)
        
        try:
            # 调用OpenAI的聊天完成API
            response = client.chat.completions.create(
                model='deepseek-r1',
                messages=history_openai_format,
                temperature=1.0,
                stream=True
            )

            partial_message = "结论"
            reasoing_partial_message = "思考过程："
            for chunk in response:
                delta = chunk.choices[0].delta
                # 打印思考过程
                if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
                    print(delta.reasoning_content, end='', flush=True)
                    reasoing_partial_message += delta.reasoning_content
                    yield reasoing_partial_message
                else:
                    if chunk.choices[0].delta.content is not None:
                        partial_message += chunk.choices[0].delta.content
                        yield partial_message
        except Exception as api_error:
            yield f"API错误: {str(api_error)}"
    except Exception as format_error:
        yield f"格式错误: {str(format_error)}"

# 创建Gradio界面
iface = gr.ChatInterface(
    predict,
    chatbot=gr.Chatbot(height=500),
    title="DeepSeek Chat - 多轮对话",
    description="与DeepSeek AI模型聊天。您的对话历史将被保留。",
    theme="soft",
    examples=["你好，你好吗？", "今天天气怎么样？"],
    css=".gradio-container .chatbot { width: 400px; }"
)

# 启动界面
iface.launch()
