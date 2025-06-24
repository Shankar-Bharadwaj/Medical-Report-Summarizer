import boto3
from flask import current_app
from botocore.exceptions import ClientError
import json


def generate_presigned_url(request_id, operation="put_object", content_type="application/pdf", expires_in=600):
    s3 = boto3.client("s3")
    s3_key = f"path-documents/{request_id}.pdf"

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


def get_summary(request_id):
    s3 = boto3.client("s3")
    summary_key = f"path-summaries/{request_id}.json"

    try:
        response = s3.get_object(Bucket=current_app.config["S3_BUCKET"], Key=summary_key)
        summary_data = json.loads(response['Body'].read())
        summary_text = summary_data.get("summary", "No summary available.")
    except ClientError as e:
        current_app.logger.error(f"Failed to fetech summary for {request_id}: {e}")
        summary_text = "Sorry, we couldn't retrieve your summary at the moment."
    
    return summary_text