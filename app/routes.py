from flask import Blueprint, render_template, request, redirect, url_for, current_app, jsonify
import boto3
from .utils import generate_presigned_url

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
    url, s3_key = generate_presigned_url(request_id)
    return jsonify({"presigned_url": url, "s3_key": s3_key})


# Not required
# @main.route("/get-ws-url")
# def get_ws_url():
#     return jsonify({"ws_url": current_app.config["API_GATEWAY_WS_URL"]})