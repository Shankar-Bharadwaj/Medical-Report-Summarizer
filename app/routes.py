from flask import Blueprint, render_template, request, redirect, url_for, current_app, jsonify
import boto3

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template('home.html')


@main.route("/loading/<request_id>")
def loading(request_id):
    return render_template("loading.html", request_id=request_id, ws_url=current_app.config["API_GATEWAY_WS_URL"])


@main.route("/get-presigned-url")
def get_presigned_url():
    request_id = request.args.get("request_id")
    s3_key = f"path-documents/{request_id}.pdf"

    s3 = boto3.client("s3")
    url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': current_app.config["S3_BUCKET"], 
            'Key': s3_key, 
            'ContentType': "application/pdf"
        }, 
        ExpiresIn=600
    )

    return jsonify({"presigned_url": url, "s3_key": s3_key})


# Not required
# @main.route("/get-ws-url")
# def get_ws_url():
#     return jsonify({"ws_url": current_app.config["API_GATEWAY_WS_URL"]})