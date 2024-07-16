import os
#from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoModelForCausalLM, LlamaTokenizer

# 检查环境变量是否设置正确
print("HF_HOME:", os.getenv('HF_HOME'))
os.environ['HUGGINGFACE_HUB_TOKEN'] = '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'
# 测试下载模型
#model_name = "Qwen/Qwen2-7B-Instruct"  
model_name = "THUDM/cogagent-chat-hf"  

# 下载模型和分词器
# tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-7B-Instruct")
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2-7B-Instruct")
tokenizer = LlamaTokenizer.from_pretrained("lmsys/vicuna-7b-v1.5", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
# 测试模型是否加载成功
print(f"Model {model_name} and tokenizer loaded successfully!")
