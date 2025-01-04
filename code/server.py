#!/usr/bin/env python
from flask import Flask, request
import datetime
import subprocess
import json
import os
import yaml

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

def load_config():
    with open('/conf/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return config

config = load_config()

@app.route('/', methods=['POST'])
def reply():
    data = request.get_json()
    if 'reviewId' in data and 'text' in data:
        review_id = data['reviewId']
        text = data['text']
        json_data = json.dumps({'reviewId': review_id, 'text': text})
        run_reply_script(json_data, config)
        return 'Data received and processed'
    else:
        return 'Invalid JSON data'

def timed_job(config):
    now = datetime.datetime.now()
    sync_script = '/code/sync.sh'
    if config.get('debug', False):
        sync_script = '/code/debug/sync.sh'
    print(f'{now} {sync_script} ...')
    subprocess.run([sync_script])


def run_reply_script(json_data, config):
    with open('/tmp/data.json', 'w') as f:
        f.write(json_data)
    reply_script = '/code/reply.py'
    if config.get('debug', False):
        reply_script = '/code/debug/reply.py'
    subprocess.run([reply_script], input=json_data.encode())


scheduler = BackgroundScheduler()

scheduler.add_job(timed_job, 'interval', minutes=5, args=[config])

scheduler.start()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)

