# CollectiveAI
This is the official repository of CollectiveAI

## android_data
### runs
从android_world中直接收集的数据（第一版）
### traj_reward_sft
以traj-level的label（0/1）作为整个轨迹中所有step的reward
### reward_model_trian
训练reward model的数据（第一版）
### runs_step_reward
step-level的reward，从android_world中直接收集的数据，使用gpt4o对每一步的行为给出reward，数据格式（每个task）：['before_element_list', 'after_element_list', 'action_prompt', 'action_output_list', 'agent_step_scores'...]
### runs_step_reward_sft
tsv格式，数据格式：["goal", "task_template", "query", "response", "rating"]
## 

