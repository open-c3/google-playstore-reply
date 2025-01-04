#!/usr/bin/env python
import json
import sys
import os

# 从标准输入读取 JSON 数据
json_data = sys.stdin.read()

# 将 JSON 数据转换为 Python 字典
data = json.loads(json_data)

# 获取 reviewId
review_id = data.get('reviewId')

# 如果没有提供 reviewId,则退出
if not review_id:
    print("Error: reviewId is required")
    sys.exit(1)

# 构造文件名
filename = f"/tmp/reply-data-{review_id}.json"

# 将数据写入文件
with open(filename, 'w') as f:
    json.dump(data, f)

print(f"Data saved to {filename}: {data}")

