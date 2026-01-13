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
        user_id = int(get_jwt_identity())
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files.get("photo")
        video = request.files.get("video")
    except Exception as e:
        return json_err({"error":str(e)})
    
    if not all([title, video]):
        return json_err({"error":"These Are Required"}, 400)
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json_err({"error":"User Id Error"}, 400)
    
    if not check_extenstions(video.filename) or not secure_filename(video.filename):
        return json_err({"error":"Extension not allow"})
    
    if video and check_extenstions(video.filename):
        filename = secure_filename(video.filename)
        time_stamp = datetime.datetime.utcnow().strftime("%d%m%Y%H%M%S")

        filename = f"{time_stamp}_{filename}"

        upload_folder = os.path.join(UPLOAD_FOLDERS)
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)
        video.save(file_path)

        relative_path = f"/uploads/{filename}"
    else:
        relative_path = None

    if photo and check_extenstions(photo.filename):
        filename = secure_filename(photo.filename)
        time_stamp = datetime.datetime.utcnow().strftime("%d%m%Y%H%M%S")

        filename = f"{time_stamp}_{filename}"

        upload_folder = os.path.join(UPLOAD_FOLDERS)
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)
        photo.save(file_path)

        photo_path = f"/uploads/{filename}"
    else:
        photo_path = None
    
    new_media = Media(
        user_id=user.id,
        title=title,
        content=content,
        video=relative_path,
        photo=photo_path
        )

    new_media.save()
    return json_ok({"media":new_media.to_dict()})

@main_bp.route("/find_videos", methods=['GET'])
def find_videos():
    try:
        title = request.args.get("title")
    except Exception as e:
        return json_err({"error":str(e)})
    
    videos = Media.query.all()

    all_videos = [video.to_dict() for video in videos]
    results = [v for v in all_videos if v.get("title") == title]

    return json_ok({"result":results}, 200)

