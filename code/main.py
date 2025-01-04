#!/usr/bin/env python
import subprocess
import json
import requests

def run_list_py():
    process = subprocess.Popen(['python', 'list.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f'Error: {stderr.decode()}')
        return
    
    # 处理标准输出
    for line in stdout.decode().split('\n'):
        if line.strip():
            process_json_line(line)

def process_json_line(json_line):
    # 将JSON行转换为Python对象
    data = json.loads(json_line)
    
    # 提取所需信息

    review_id = data['reviewId']

    device_name = data['comments'][0]['userComment']['deviceMetadata']['productName']
    comment_time_seconds = data['comments'][0]['userComment']['lastModified']['seconds']
    thumbs_up_count = data['comments'][0]['userComment']['thumbsUpCount']
    thumbs_down_count = data['comments'][0]['userComment']['thumbsDownCount']
    reviewer_language = data['comments'][0]['userComment']['reviewerLanguage']
    app_version_code = data['comments'][0]['userComment']['appVersionCode']
    app_version_name = data['comments'][0]['userComment']['appVersionName']
    android_os_version = data['comments'][0]['userComment']['androidOsVersion']
    star_rating = data['comments'][0]['userComment']['starRating']
    user_comment = data['comments'][0]['userComment']['text']
    developer_comment = data['comments'][1]['developerComment']['text']
    
    # 生成新的JSON对象
    simplified_data = {
        'review_id': review_id,
        'device_name': device_name,
        'comment_time_seconds': comment_time_seconds,
        'thumbs_up_count': thumbs_up_count,
        'thumbs_down_count': thumbs_down_count,
        'reviewer_language': reviewer_language,
        'app_version_code': app_version_code,
        'app_version_name': app_version_name,
        'android_os_version': android_os_version,
        'star_rating': star_rating,
        'user_comment': user_comment,
        'developer_comment': developer_comment
    }
    
    # 输出简化版JSON对象
    print(json.dumps(simplified_data, indent=2))

    # 将数据POST到指定接口
    url = 'http://10.10.10.10/api/ci/googleplay/review/record'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(simplified_data))
    
    if response.status_code == 200:
        print(f'Data sent successfully: {response.text}')
    else:
        print(f'Error sending data: {response.text}')

if __name__ == '__main__':
    run_list_py()

