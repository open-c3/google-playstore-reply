#!/usr/bin/env python
import subprocess
import json
import requests
import yaml
import os
import sys
import hashlib

def load_config():
    with open('/conf/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    with open('/config.yaml', 'r') as f:
        config.update(yaml.safe_load(f))

    app_package_name = os.environ.get('app_package_name')
    if not app_package_name:
        print("Error: app_package_name environment variable is not set.")
        sys.exit(1)
    config['app_package_name'] = app_package_name

    return config


def run_list_py(config, list_py_path):
    process = subprocess.Popen(['python', list_py_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f'Error: {stderr.decode()}')
        return
    
    for line in stdout.decode().split('\n'):
        if line.strip():
            process_json_line(line, config)

def process_json_line(json_line, config):
    data = json.loads(json_line)
    
    simplified_data = data.copy()
    
    simplified_data.update({
        'package_name': config['package_name'],
        'app_package_name': config['app_package_name'],
        'callback': f"http://{config['ip']}:{config['port']}"
    })
    
    # 对数据进行排序和压缩
    sorted_data = dict(sorted(simplified_data.items()))
    compressed_str = json.dumps(sorted_data, separators=(',', ':'))

    # 计算 MD5
    md5_hash = hashlib.md5(compressed_str.encode()).hexdigest()

    # 检查是否已经处理过这个 MD5
    if os.path.exists(f'/tmp/post.md5.{md5_hash}'):
        print(f'Skipping post for MD5: {md5_hash} (already processed)')
        return


    print(json.dumps(simplified_data, indent=2))

    url = config['openc3_url']
    headers = {'Content-Type': 'application/json'}
    headers.update(config['openc3_header'])
    response = requests.post(url, headers=headers, data=json.dumps(simplified_data))
    
    if response.status_code == 200:
        print(f'Data sent successfully: {response.text}')
        open(f'/tmp/post.md5.{md5_hash}', 'w').close()
    else:
        print(f'Error sending data: {response.text}')

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Usage: python task.py <list_py_path>")
        sys.exit(1)

    list_py_path = sys.argv[1]

    config = load_config()
    run_list_py(config, list_py_path)

