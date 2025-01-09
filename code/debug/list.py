#!/usr/bin/env python

import json
import random
import string

with open('/code/debug/demo.json', 'r') as f:
    data = json.load(f)

def generate_review_id(length=32):
    characters = string.ascii_letters + string.digits
    return 'gp:AOqpTO' + ''.join(random.choice(characters) for _ in range(length))

for _ in range(2):
    data['reviewId'] = generate_review_id()
    json_line = json.dumps(data, separators=(',', ':')) 
    data = json.loads(json_line)

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
    }
    
    print(json.dumps(simplified_data, separators=(',', ':')))
