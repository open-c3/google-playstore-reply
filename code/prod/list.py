#!/usr/bin/env python
import yaml
import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

with open("/conf/config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

try:
    app_package_name = os.environ['app_package_name']
except KeyError:
    print("Error: APP_PACKAGE_NAME environment variable is not set.")
    exit(1)

key_file = config["key_file"]

def get_last_week_reviews():
    credentials = service_account.Credentials.from_service_account_file(
        key_file, scopes=["https://www.googleapis.com/auth/androidpublisher"]
    )

    try:
        service = build("androidpublisher", "v3", credentials=credentials)
        response = (
            service.reviews()
            .list(
                packageName=app_package_name,
            )
            .execute()
        )
        all_reviews = response.get("reviews", [])

        return all_reviews

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


if __name__ == "__main__":
    try:
        last_x_reviews = get_last_week_reviews()
        for i, review in enumerate(last_x_reviews, 1):
            data = review.copy()

            print(json.dumps(data, indent=2))
            review_id = data['reviewId']
            authorName = data['authorName']
        
            device_name = data['comments'][0]['userComment']['deviceMetadata']['productName']
            comment_time_seconds = data['comments'][0]['userComment']['lastModified']['seconds']
            thumbs_up_count = data['comments'][0]['userComment'].get('thumbsUpCount', 'Unknown')
            thumbs_down_count = data['comments'][0]['userComment'].get('thumbsDownCount', 'Unknown')
            reviewer_language = data['comments'][0]['userComment']['reviewerLanguage']
            app_version_code = data['comments'][0]['userComment']['appVersionCode']
            app_version_name = data['comments'][0]['userComment']['appVersionName']
            android_os_version = data['comments'][0]['userComment']['androidOsVersion']
            star_rating = data['comments'][0]['userComment']['starRating']
            user_comment = data['comments'][0]['userComment']['text']
            developer_comment = data['comments'][1]['developerComment']['text'] if len(data['comments']) > 1 else ''
            
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
    except Exception as e:
        print(str(e))
