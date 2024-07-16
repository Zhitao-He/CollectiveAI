import os
import gzip
import io
import pickle
import json
from tqdm import tqdm
import math


def _unzip_and_read_pickle(file_path: str):
    with open(file_path, 'rb') as f:
        compressed = f.read()

    with gzip.open(io.BytesIO(compressed), 'rb') as f_in:
        return pickle.load(f_in)

def process_pkl_gz_files(folder_path):
    task_success = []
    task_info_dict = {}
    task_fail = []
    e = 0
    # 遍历文件夹中的每一个文件
    for root, dirs, files in os.walk(folder_path):
        for file in tqdm(files):
            # 检查文件是否以.pkl.gz结尾
            
            if file.endswith('.pkl.gz'):
                file_path = os.path.join(root, file)
                try:
                    # 打开并读取pkl.gz文件
                    unzip_info = _unzip_and_read_pickle(file_path)
                    task_dict = {}

                    goal = unzip_info[0]['goal']
                    task_template = unzip_info[0]['task_template']
                    is_successful = unzip_info[0]['is_successful']
                    episode_length = unzip_info[0]['episode_length']
                    
                    if is_successful == 1.0:
                        task_success.append(task_template)
                        e += episode_length
                    else:
                        task_fail.append(task_template)

                    # 替换 NaN 值为 0
                    if isinstance(is_successful, float) and math.isnan(is_successful):
                        is_successful = 0
                    if isinstance(episode_length, float) and math.isnan(episode_length):
                        episode_length = 0

                    task_dict['goal'] = goal
                    task_dict['task_template'] = task_template
                    task_dict['is_successful'] = is_successful
                    task_dict['episode_length'] = episode_length
                    
                        
                    task_info_dict[task_template] = task_dict
                    
                except Exception as e:
                    print(f"Error loading {file}: {e}")
    print('Now file:', root)
    print('num of task_success:', len(task_success))
    

    # 写入任务信息到 JSON 文件
    output_file = 'android_world/2task_complete_info.json'
    print('e_length:', e)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(task_info_dict, f, ensure_ascii=False, indent=4)
    
    return task_success, task_fail

# 指定文件夹路径
#folder_path = 'android_world/runs/run_20240625T141458' # num of task_success: 1
#folder_path = 'android_world/runs/run_20240625T162748' # num of task_success: 28
#folder_path = 'android_world/runs/run_20240628T142400' # num of task_success: 1
#folder_path = 'android_world/runs/run_20240628T144329' # num of task_success: 3
#folder_path = 'android_world/runs/run_20240701T163045' # num of task_success: 24
#folder_path = 'android_world/runs/run_20240701T234154' # num of task_success: 42
#folder_path = 'android_world/runs/run_20240702T103617' # num of task_success: 13
task_success, task_fail = process_pkl_gz_files(folder_path)
#print('task_success:', task_success)
#print('\n')
#print('task_fail:', task_fail)
