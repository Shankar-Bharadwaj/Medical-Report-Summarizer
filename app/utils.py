import boto3
from flask import current_app


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