import os
import gzip
import io
import pickle
import json
from tqdm import tqdm
import math
import csv
import re
# 收集成功与不成功的数据
# 使用step reward而不是traj-level reward
GUIDANCE = (
    'Here are some useful guidelines you need to follow:\n'
    'Action Related\n'
    '- Use the `open_app` action whenever you want to open an app'
    ' (nothing will happen if the app is not installed), do not use the'
    ' app drawer to open an app unless all other ways have failed.\n'
    '- Use the `input_text` action whenever you want to type'
    ' something (including password) instead of clicking characters on the'
    ' keyboard one by one. Sometimes there is some default text in the text'
    ' field you want to type in, remember to delete them before typing.\n'
    '- For `click`, `long_press` and `input_text`, the index parameter you'
    ' pick must be VISIBLE in the screenshot and also in the UI element'
    ' list given to you (some elements in the list may NOT be visible on'
    ' the screen so you can not interact with them).\n'
    '- Consider exploring the screen by using the `scroll`'
    ' action with different directions to reveal additional content.\n'
    '- The direction parameter for the `scroll` action can be confusing'
    " sometimes as it's opposite to swipe, for example, to view content at the"
    ' bottom, the `scroll` direction should be set to "down". It has been'
    ' observed that you have difficulties in choosing the correct direction, so'
    ' if one does not work, try the opposite as well.\n'
    '\n\nNow output an action from the above list in the correct JSON format,'
    ' following the reason why you do that. Your answer should look like:\n'
    'Reason: ...\nAction: {{"action_type":...}}\n\n'
    'Your Answer:\n'
)

ANSWER_FORMAT = (
    'Your answer should look like:\n'
    'Reason: ...\nAction: {{"action_type":...}}\n\n'
)

def remove_UI_property(text):
    # 定义要去除的字段
    fields_to_remove = ['bbox', 'bbox_pixels']

    # 构建正则表达式模式，包含特殊处理的bbox_pixels字段
    pattern = r',?\s*(%s)=(?:BoundingBox\([^)]*\)|[^,)]*)' % '|'.join(fields_to_remove)

    # 使用正则表达式去除匹配的字段
    cleaned_text = re.sub(pattern, '', text)

    return cleaned_text

def remove_guidelines(text):
    start_index = text.find("Here are some useful guidelines you need to follow:")

    # 保留目标字符串之前的所有内容
    if start_index != -1:
        text = text[:start_index]

    return text

def _unzip_and_read_pickle(file_path: str):
    with open(file_path, 'rb') as f:
        compressed = f.read()

    with gzip.open(io.BytesIO(compressed), 'rb') as f_in:
        return pickle.load(f_in)

def process_pkl_gz_files(folder_path):
    agent0_data = []
    agent1_data = []
    agent2_data = []
    #failed_data = []
    task_completed = []
    episode_num = 0
    query_len = []
    s = 0
    f = 0
    # 遍历文件夹中的每一个文件
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            current_task = 0
            dir_path = os.path.join(root, dir)
            for root1, dirs1, files1 in os.walk(dir_path):
                for file in tqdm(files1):
                    # 检查文件是否以.pkl.gz结尾
                    if file.endswith('.pkl.gz'):
                        file_path = os.path.join(root1, file)
                        try:
                            # 打开并读取pkl.gz文件
                            unzip_info = _unzip_and_read_pickle(file_path)
                            is_successful = unzip_info[0]['is_successful']
                            #if is_successful == 1.0:
                            # 信息分类
                            run_time = unzip_info[0]['run_time']
                            agent_name = unzip_info[0]['agent_name']
                            exception_info = unzip_info[0]['exception_info']
                            finish_dtime = unzip_info[0]['finish_dtime']
                            screen_config = unzip_info[0]['screen_config']
                            # useful info
                            goal = unzip_info[0]['goal']
                            task_template = unzip_info[0]['task_template']
                            #if task_template not in task_completed:
                            #    task_completed.append(task_template)
                            episode_length = unzip_info[0]['episode_length']
                            seed = unzip_info[0]['seed']
                            # details of episode
                            episode_data = unzip_info[0]['episode_data']
                            # before_screenshot = episode_data['before_screenshot']
                            # after_screenshot = episode_data['after_screenshot']
                            # before_element_list = episode_data['before_element_list']
                            # after_element_list = episode_data['after_element_list']
                            action_prompt = episode_data['action_prompt']
                            action_output_list = episode_data['action_output_list']
                            action_list = episode_data['action_list']
                            reason_list = episode_data['reason_list']
                            action_raw_response_list = episode_data['action_raw_response_list']
                            action_adapt = episode_data['action_adapt']
                            action_adapt_frequency = episode_data['action_adapt_frequency']
                            summary_prompt = episode_data['summary_prompt']
                            summary = episode_data['summary']
                            summary_raw_response = episode_data['summary_raw_response']
                            action_raw_response = episode_data['action_raw_response']
                            #summary_prompt = episode_data['summary_prompt']
                            
                            # 训练数据
                            #if is_successful == 1.0:
                            
                            current_task += 1
                            if task_template not in task_completed:
                                task_completed.append(task_template)
                            episode_num += episode_length
                            #agent_list = [{} for _ in range(3)]
                            #print('------len action_prompt:', len(action_prompt))
                            if is_successful:
                                s += len(action_prompt)
                            else:
                                f += len(action_prompt)
                            for idx, step_prompt in enumerate(action_prompt):
                                #print('------len action_output_list:', len(action_output_list))

                                action_outputs = action_output_list[idx]
                                #print(f'=========step {idx}, action_outputs: {action_outputs}')
                                #print('\n')
                                agent_list = [{} for _ in range(3)]
                                for index, agent_dict in enumerate(agent_list):
                                    agent_dict['goal'] = goal
                                    agent_dict['task_template'] = task_template
                                    
                                    # 直接使用
                                    agent_dict['query'] = step_prompt + 'Your Answer:\n'

                                    # 去除UI多余的属性
                                    # query = step_prompt
                                    # query = remove_UI_property(query) + 'Your Answer:\n'
                                    # agent_dict['query'] = query
                                    
                                    # 去除一些guidelines
                                    # query = step_prompt
                                    # query = remove_UI_property(query)
                                    # query_processed = remove_guidelines(query) 
                                    # agent_dict['query'] = query_processed + ANSWER_FORMAT + GUIDANCE
                                    # #query_len.append((len(query), len(query_processed)))

                                    if index < len(action_outputs): 
                                        agent_dict['response'] = action_outputs[index]
                                        #print(f"index {index}, response {agent_dict['response']}]")
                                        #print('\n')
                                    else:
                                        agent_dict['response'] = action_outputs[len(action_outputs)-1]
                                        #print(f"index {index}, response {agent_dict['response']}]")
                                        #print('\n')
                                    if is_successful == 1.0:
                                        agent_dict['rating'] = is_successful
                                    else:
                                        agent_dict['rating'] = 0


                                    if index == 0:
                                        agent0_data.append(agent_dict)
                                        #print(f'---agent {index}, action: {agent_dict["response"]}')
                                            
                                    if index == 1:
                                        agent1_data.append(agent_dict)
                                        #print(f'---agent {index}, action: {agent_dict["response"]}')

                                    if index == 2:
                                        agent2_data.append(agent_dict)
                                        #print(f'---agent {index}, action: {agent_dict["response"]}')                
                            else:
                                continue 
                        except Exception as e:
                            print(f"Error loading {file}: {e}")
            print(f'Now dir: {dir}, num of completed: {s}, num of failed: {f}') 
            
            # 写入任务信息到 JSON 文件
            # filename_agent0 = 'android_world/training_data/android_agent0.tsv'
            # filename_agent1 = 'android_world/training_data/android_agent1.tsv'
            # filename_agent2 = 'android_world/training_data/android_agent2.tsv'
            filename_agent0 = 'android_world/reward_model_train/UI_android_agent0.tsv'
            filename_agent1 = 'android_world/reward_model_train/UI_android_agent1.tsv'
            filename_agent2 = 'android_world/reward_model_train/UI_android_agent2.tsv'
            # filename_agent0 = 'android_world/training_data/UI_Gui_android_agent0.tsv'
            # filename_agent1 = 'android_world/training_data/UI_Gui_android_agent1.tsv'
            # filename_agent2 = 'android_world/training_data/UI_Gui_android_agent2.tsv'
            filenames = [filename_agent0, filename_agent1, filename_agent2]
            agent_data = [agent0_data, agent1_data, agent2_data]
            print('len agent_data:', len(agent0_data))
            for data, filename in zip(agent_data, filenames):
                print("===len(data):", len(data))
                with open(filename, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=["goal", "task_template", "query", "response", "rating"], delimiter='\t')
                    writer.writeheader()
                    for entry in data:
                        writer.writerow(entry)
                
                # 读取数据从文件，确认写入数据的完整性
                with open(filename, mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter='\t')
                    rows = list(reader)
                    print(f"=== len(rows) after writing to {filename}: {len(rows)}")
    print('---episode num:', episode_num)
    print('---query_len:', query_len)
    return task_completed

# 指定文件夹路径
folder_path = 'android_world/runs'
#folder_path = 'android_world/runs/run_20240628T144329'
task_completed = process_pkl_gz_files(folder_path)
#print('task_success:', task_completed)
print('\n')
print('num_task_success:', len(task_completed))
#print('\n')
#print('task_fail:', task_fail)
