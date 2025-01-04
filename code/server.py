#!/usr/bin/env python
from flask import Flask, request
import datetime
import subprocess
import json
import os

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

@app.route('/', methods=['POST'])
def reply():
    data = request.get_json()
    if 'reviewId' in data and 'text' in data:
        review_id = data['reviewId']
        text = data['text']
        json_data = json.dumps({'reviewId': review_id, 'text': text})
        run_reply_script(json_data)
        return 'Data received and processed'
    else:
        return 'Invalid JSON data'

def timed_job():
    now = datetime.datetime.now()
    print(f'{now} /code/sync.sh ...')
    subprocess.run(['/code/sync.sh'])

def run_reply_script(json_data):
    #TODO
    with open('/tmp/data.json', 'w') as f:
        f.write(json_data)
    subprocess.run(['/code/reply.py'], input=json_data.encode())

scheduler = BackgroundScheduler()

scheduler.add_job(timed_job, 'interval', minutes=5)

scheduler.start()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)

