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
    episode_num = 0
    # 遍历文件夹中的每一个文件
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            for root1, dirs1, files1 in os.walk(dir_path):
                current_success = 0
                for file in tqdm(files1):
                    # 检查文件是否以.pkl.gz结尾
                    if file.endswith('.pkl.gz'):
                        file_path = os.path.join(root1, file)
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
                                episode_num += episode_length
                                current_success += 1
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
            
            print(f'Now dir:{dir}, num of completed task: {current_success}')

            # 写入任务信息到 JSON 文件
            # output_file = 'android_world/4task_complete_info.json'
            # #print('e_length:', e)
            # with open(output_file, 'w', encoding='utf-8') as f:
            #     json.dump(task_info_dict, f, ensure_ascii=False, indent=4)
    print('total episode length:', episode_num)
    return task_success, set(task_fail)

# 指定文件夹路径
#folder_path = 'android_world/runs/run_20240625T162748'
#folder_path = 'android_world/runs/run_20240701T163045'
#folder_path = 'android_world/runs/run_20240702T103617'
folder_path = 'android_world/runs'
#folder_path = 'android_world/runs/run_20240628T144329'
task_success, task_fail = process_pkl_gz_files(folder_path)
print(f'all_task_success: {task_success}\nnum: {len(task_success)}' )
print('\n')
print(f'task_fail: {task_fail}\nnum: {len(task_fail)}')
