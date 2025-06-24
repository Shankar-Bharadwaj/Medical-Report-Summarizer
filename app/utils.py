import boto3
from flask import current_app
from botocore.exceptions import ClientError, BotoCoreError
import json
import time


def generate_presigned_url(request_id, operation="put_object", content_type="application/pdf", expires_in=600):
    s3 = boto3.client("s3")
    s3_key = f"path-documents/{request_id}.pdf"

    try:
        url = s3.generate_presigned_url(
            ClientMethod=operation,
            Params={
                'Bucket': current_app.config["S3_BUCKET"], 
                'Key': s3_key, 
                'ContentType': content_type
            }, 
            ExpiresIn=expires_in
        )
        return url, s3_key
    
    except (ClientError, BotoCoreError) as e:
        current_app.logger.error(f"[S3] Failed to generate presigned S3 url: {e}")
        return None, None


def get_summary(request_id):
    s3 = boto3.client("s3")
    summary_key = f"path-summaries/{request_id}.json"

    try:
        response = s3.get_object(
            Bucket=current_app.config["S3_BUCKET"], 
            Key=summary_key
        )
        summary_data = json.loads(response['Body'].read())
        summary_text = summary_data.get("summary", "No summary available.")
    except (ClientError, BotoCoreError) as e:
        current_app.logger.error(f"[S3] Failed to fetch summary for {request_id}: {e}")
        summary_text = "Sorry, we couldn't retrieve your summary at the moment."
    
    return summary_text


def update_dynamo(request_id, status, input_s3_key, timestamp=None, ttl_seconds=3600):
    if timestamp is None:
        timestamp = int(time.time())
    expire_at = timestamp + ttl_seconds
    dynamodb = boto3.client("dynamodb")

    try:
        dynamodb.put_item(
            TableName=current_app.config["DYNAMO_TABLE"],
            Item={
                'request_id': {'S': request_id},
                'status': {'S': status},
                'input_s3_key': {'S': input_s3_key},
                'timestamp': {'N': str(timestamp)},
                'expire_at': {'N': str(expire_at)}
            }
        )
        current_app.logger.info(f"[DynamoDB] Item written for {request_id}")
        return True
    
    except (ClientError, BotoCoreError) as e:
        current_app.logger.error(f"[DynamoDB] Failed to write item to DynamoDB: {e}")
        return False