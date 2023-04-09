# this script forked from https://github.com/FallenChromium/tilda-static-page-exporter
# and distributed under GNU GPL-3.0 license

import os
import requests
from flask import Flask, request, Response
from pathlib import Path

app = Flask(__name__)

TILDA_PUBLIC_KEY = os.environ.get("TILDA_PUBLIC_KEY")
TILDA_SECRET_KEY = os.environ.get("TILDA_SECRET_KEY")
TILDA_STATIC_PATH_PREFIX = os.environ.get("TILDA_STATIC_PATH_PREFIX")


def get_local_path(export_path, target_path):
    if export_path:
        return Path(TILDA_STATIC_PATH_PREFIX) / Path(export_path) / Path(target_path)
    else:
        return Path(TILDA_STATIC_PATH_PREFIX) / Path(target_path)


def extract_project(project_id):
    project_info = requests.get(
        f"https://api.tildacdn.info/v1/getprojectinfo/?projectid={project_id}&publickey={TILDA_PUBLIC_KEY}&secretkey={TILDA_SECRET_KEY}"
    )
    project_info_json = project_info.json()["result"]
    index_page_id = project_info_json.get("indexpageid", None)
    project_main_images = project_info_json.get("images", None)
    for image in project_main_images:
        source_url = image["from"]
        local_path = Path(TILDA_STATIC_PATH_PREFIX) / Path(image["to"])
        local_path.parent.mkdir(parents=True, exist_ok=True)
        save_file(source_url, local_path)

    pages_list = requests.get(
        f"https://api.tildacdn.info/v1/getpageslist/?projectid={project_id}&publickey={TILDA_PUBLIC_KEY}&secretkey={TILDA_SECRET_KEY}"
    )
    pages_list_json = pages_list.json()["result"]
    for page in pages_list_json:
        page_info = requests.get(
            f'https://api.tildacdn.info/v1/getpagefullexport/?projectid={project_id}&pageid={page["id"]}&publickey={TILDA_PUBLIC_KEY}&secretkey={TILDA_SECRET_KEY}'
        )
        page_info_json = page_info.json()["result"]
        export_csspath = page_info_json.get("export_csspath", None)
        export_jspath = page_info_json.get("export_jspath", None)
        export_imgpath = page_info_json.get("export_imgpath", None)
        for image in page_info_json["images"]:
            source_url = image["from"]
            local_path = get_local_path(export_imgpath, image["to"])
            local_path.parent.mkdir(parents=True, exist_ok=True)
            save_file(source_url, local_path)

        for script in page_info.json()["result"]["js"]:
            source_url = script["from"]
            local_path = get_local_path(export_jspath, script["to"])
            local_path.parent.mkdir(parents=True, exist_ok=True)
            save_file(source_url, local_path)

        for style in page_info.json()["result"]["css"]:
            source_url = style["from"]
            local_path = get_local_path(export_csspath, style["to"])
            local_path.parent.mkdir(parents=True, exist_ok=True)
            save_file(source_url, local_path)

        filename = page_info.json()["result"]["filename"]
        if filename == f"page{index_page_id}.html":
            filename = "index.html"
        html_content = page_info.json()["result"]["html"]
        with open(Path(TILDA_STATIC_PATH_PREFIX) / filename, "w") as f:
            f.write(html_content)
        app.logger.warning(f"Finished extraction for project {project_id}")


def save_file(source_url, local_path):
    response = requests.get(source_url, stream=True)
    with open(local_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


@app.route("/webhook", methods=["GET"])
def handle_webhook():
    project_id = request.args.get("projectid")
    webhook_public_key = request.args.get("publickey")
    response = Response("ok")

    @response.call_on_close
    def process_after_request():
        if webhook_public_key == TILDA_PUBLIC_KEY:
            app.logger.warning(
                f"Starting extraction for project {project_id} to prefix {TILDA_STATIC_PATH_PREFIX}"
            )
            extract_project(project_id)
        else:
            app.logger.error(
                "Public key did't match!"
            )

    return response