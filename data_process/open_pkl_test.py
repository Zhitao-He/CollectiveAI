
import gzip
import os
import io
import pickle

# 打开android world环境收集的数据 

# 从文件加载词典
def _unzip_and_read_pickle(file_path):
  with open(file_path, 'rb') as f:
    compressed = f.read()

  with gzip.open(io.BytesIO(compressed), 'rb') as f_in:
    return pickle.load(f_in)

file_name = 'runs_step_reward/run_20240715T164115/AudioRecorderRecordAudio.pkl.gz'

unzip_info = _unzip_and_read_pickle(file_name)
#info = unzip_info[0]['task_template']

#print('info:', unzip_info)

""" goal = unzip_info[0]['goal']
task_template = unzip_info[0]['task_template']
is_successful = unzip_info[0]['is_successful']
run_time = unzip_info[0]['run_time']
agent_name = unzip_info[0]['agent_name']
episode_length = unzip_info[0]['episode_length']
exception_info = unzip_info[0]['exception_info']
seed = unzip_info[0]['seed']
finish_dtime = unzip_info[0]['finish_dtime']
screen_config = unzip_info[0]['screen_config'] """
episode_data = unzip_info[0]['episode_data'] 

info_list = ['goal', 'task_template','is_successful','run_time','agent_name','episode_length','exception_info','seed','finish_dtime','screen_config']

#for info_name in info_list:

#    print("---{}:{}\n".format(info_name, unzip_info[0][info_name]))

print("---{}:{}\n".format('episode_data', len(unzip_info[0]['episode_data'])))
print("---{}:{}\n".format('agent_step_scores', len(unzip_info[0]['episode_data']['agent_step_scores'])))

# print(type(episode_data))
print(episode_data.keys())
# print('\n')
# print(episode_data['action_prompt'][5])
# print('---action_output_list', episode_data['action_output_list'][5])
# print('----action_adapt', episode_data['action_adapt'][5])
# print('----action_score_prompt', episode_data['step_scores_prompt'][5])

for idx, scores in enumerate(episode_data['agent_step_scores']):
  print("=======Step{}: {}\n======".format(idx, scores))

#print('====agent_step_scores', episode_data['agent_step_scores'])

# for k in episode_data['action_output_list']:
#     print(k)
#     print('\n')