from openai import OpenAI

# 以openai api形式部署模型

openai_api_key = "EMPTY"  # 填 EMPTY
openai_api_base = "http://localhost:18081/v1"  # 这里在本地 mac 上远程请求部署的推理服务，所以端口是 8989

client = OpenAI(api_key=openai_api_key, base_url=openai_api_base)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Give me a short introduction to large language model."}
]

llm_response = client.chat.completions.create(
    messages=messages,
    model="Qwen2-7B-Instruct",  # 这里填的就是 vLLM 启动的时候的服务名
    max_tokens=2048,
    temperature=0.1,
    stream=False  # 控制是否是流式请求
)

print(llm_response.choices[0].message.content)