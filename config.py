import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey")
    S3_BUCKET = os.environ.get("S3_BUCKET", "medical-reports-summarizer")
    # Replace with actual API GATEWAY URL
    API_GATEWAY_WS_URL = os.environ.get("API_GATEWAY_WS_URL",
                                        "wss://abc123xyz.execute-api.ap-south-1.amazonaws.com/dev")
