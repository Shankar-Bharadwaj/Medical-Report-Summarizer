from flask import Blueprint, render_template, request, redirect, url_for, current_app, jsonify
from .utils import generate_presigned_url, get_summary

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template('home.html')


@main.route("/get-presigned-url")
def get_presigned_url():
    request_id = request.args.get("request_id")
    url, s3_key = generate_presigned_url(request_id)
    return jsonify({"presigned_url": url, "s3_key": s3_key})


@main.route("/loading/<request_id>")
def loading(request_id):
    return render_template("loading.html", request_id=request_id, ws_url=current_app.config["API_GATEWAY_WS_URL"])


@main.route("/result/<request_id>")
def result(request_id):
    summary = get_summary(request_id)
    return render_template("result.html", request_id=request_id, summary=summary)


# Not required
# @main.route("/get-ws-url")
# def get_ws_url():
#     return jsonify({"ws_url": current_app.config["API_GATEWAY_WS_URL"]})