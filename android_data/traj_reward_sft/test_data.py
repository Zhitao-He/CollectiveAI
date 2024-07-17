import os
import gzip
import io
import pickle
import json
from tqdm import tqdm
import math
import csv
import re

filename = 'android_world/training_data/android_agent0.tsv'
required_fields = ["goal", "task_template", "query", "response", "rating"]

# 读取数据从文件，确认写入数据的完整性
with open(filename, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter='\t')
    rows = list(reader)

#print('rows0:', rows[0])
# 检查每一行数据是否包含所有所需字段，且这些字段不为空
def check_row_integrity(row):
    return all(field in row and row[field].strip() != "" for field in required_fields)

all_rows_valid = all(check_row_integrity(row) for row in rows)

# 打印结果
if all_rows_valid:
    print("所有数据都包含所需的字段，并且这些字段都不为空。")
else:
    print("存在数据缺少所需的字段，或者这些字段为空。")

print('rows:', rows[900])