import csv
import json
from tqdm import tqdm 

def tsv_to_json(tsv_filepath, json_filepath):
    # 读取TSV文件
    with open(tsv_filepath, 'r', encoding='utf-8') as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter='\t')
        
        # 初始化结果列表
        data = []
        
        # 遍历每一行，将其转换为所需格式
        for row in tqdm(reader):
            conversation = {
                "conversations": [
                    {
                        "from": "human",
                        "value": row["query"]
                    },
                    {
                        "from": "gpt",
                        "value": row["response"]
                    }
                ]
            }
            data.append(conversation)
    
    # 将结果写入JSON文件
    with open(json_filepath, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

# 指定TSV文件路径和输出的JSON文件路径
tsv_filepath = 'android_data/android_training_data/UI_Gui_android_agent2.tsv'
json_filepath = 'android_data/android_training_data/UI_Gui_android_share_agent2.json'

# 调用函数进行转换
tsv_to_json(tsv_filepath, json_filepath)
