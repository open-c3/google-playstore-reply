#!/usr/bin/env python

import json
import random
import string

# 读取demo.json文件
with open('/code/prod/demo.json', 'r') as f:
    data = json.load(f)

# 生成随机的reviewId
def generate_review_id(length=32):
    characters = string.ascii_letters + string.digits
    return 'gp:AOqpTO' + ''.join(random.choice(characters) for _ in range(length))

# 修改reviewId并输出
for _ in range(2):  # 输出10个对象
    data['reviewId'] = generate_review_id()
    print(json.dumps(data, separators=(',', ':')))  # 压缩成一行

