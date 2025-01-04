#!/usr/bin/env python
import subprocess
import json
import requests
import yaml
import os

def load_config():
    with open('/conf/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    with open('/config.yaml', 'r') as f:
        config.update(yaml.safe_load(f))

    # 从环境变量中获取 app_package_name 并添加到 config 字典中
    app_package_name = os.environ.get('app_package_name')
    if not app_package_name:
        print("Error: app_package_name environment variable is not set.")
        sys.exit(1)
    config['app_package_name'] = app_package_name

    return config


def run_list_py(config):
    process = subprocess.Popen(['python', 'list.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f'Error: {stderr.decode()}')
        return
    
    # 处理标准输出
    for line in stdout.decode().split('\n'):
        if line.strip():
            process_json_line(line, config)

def process_json_line(json_line, config):
    # 将JSON行转换为Python对象
    data = json.loads(json_line)
    
    # 提取所需信息

    review_id = data['reviewId']
    authorName = data['authorName']

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
        'author_name': authorName,
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
        'developer_comment': developer_comment,
        'package_name': config['package_name'],  # 添加 package_name
        'app_package_name': config['app_package_name'],
        'callback': f"http://{config['ip']}:{config['port']}"
    }
    
    # 输出简化版JSON对象
    print(json.dumps(simplified_data, indent=2))

    # 将数据POST到指定接口
    url = config['openc3_url']
    headers = {'Content-Type': 'application/json'}
    headers.update(config['openc3_header'])
    response = requests.post(url, headers=headers, data=json.dumps(simplified_data))
    
    if response.status_code == 200:
        print(f'Data sent successfully: {response.text}')
    else:
        print(f'Error sending data: {response.text}')

if __name__ == '__main__':
    config = load_config()
    run_list_py(config)

