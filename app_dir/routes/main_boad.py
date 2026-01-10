from flask import Blueprint, request
from app_dir import json_err, json_ok, UPLOAD_FOLDERS, check_extenstions
from werkzeug.utils import secure_filename
import datetime, os
from app_dir.models import *
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token


main_bp = Blueprint("main_bp", __name__, url_prefix="/main_board")

@main_bp.route("/main_dashboard", methods=['GET'])
def main_dashboard():
    media = [m.to_dict() for m in Media.query.all()]
    return json_ok({"media":media})

@main_bp.route("/add_media", methods=['POST'])
@jwt_required()
def add_media():
    try:
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.form.get("photo")
        video = request.files.get("video")
    except Exception as e:
        return json_err({"error":str(e)})
    
    if not all([title, photo, video]):
        return json_err({"error":"These Are Required"}, 400)
    
    if video and check_extenstions(video.filename):
        filename = secure_filename(video.filename)
        time_stamp = datetime.datetime.utcnow().strftime("%d%m%Y%H%M%S")

        filename = f"{time_stamp}_{filename}"

        upload_folder = os.path.join(UPLOAD_FOLDERS, "videos")
        os.makedirs(upload_folder, exist_ok=True)

    
