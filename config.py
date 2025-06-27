import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    S3_BUCKET = os.environ.get("S3_BUCKET")
    API_GATEWAY_WS_URL = os.environ.get("API_GATEWAY_WS_URL")
    DYNAMO_TABLE = os.environ.get("DYNAMO_TABLE")
