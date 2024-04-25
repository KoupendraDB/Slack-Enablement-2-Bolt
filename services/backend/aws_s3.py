import boto3, requests, os

s3 = boto3.resource('s3')

def store_files(files):
    bucket = s3.Bucket('koupendra-task-managment-slack-app')
    for filename, fileUrl in files.items():
        file_response = requests.get(fileUrl, headers={'Authorization': f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"})
        file = file_response.content
        bucket.put_object(Key=filename, Body=file)