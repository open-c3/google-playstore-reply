#!/usr/bin/env python
import yaml
import json
import sys
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

with open("/conf/config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

key_file = config["key_file"]

try:
    app_package_name = os.environ['app_package_name']
except KeyError as e:
    print(f"Error: {str(e)}. Environment variable is not set.")
    sys.exit(1)

json_data = sys.stdin.read()

data = json.loads(json_data)

review_id = data.get('reviewId')
reply_text = data.get('text')

if not review_id or not reply_text:
    print("Error: reviewId and text are required")
    sys.exit(1)

def reply_to_review(review_id, reply_text):
    print( review_id, reply_text )
    credentials = service_account.Credentials.from_service_account_file(
        key_file, scopes=["https://www.googleapis.com/auth/androidpublisher"]
    )

    try:
        service = build("androidpublisher", "v3", credentials=credentials)
        response = (
            service.reviews()
            .reply(packageName=app_package_name, reviewId=review_id, body={"replyText": reply_text})
            .execute()
        )
        print(f"Reply sent successfully: {response}")
    except HttpError as error:
        print(f"An error occurred: {error}")

reply_to_review(review_id, reply_text)

