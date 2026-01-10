from flask import Blueprint, request
from app_dir import json_err, json_ok, UPLOAD_FOLDERS, check_extenstions
from werkzeug.utils import secure_filename
import datetime, os
from app_dir.models import *
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from uuid import uuid4




auth_bp = Blueprint("auths", __name__, url_prefix="/auths")


@auth_bp.route("/register", methods=['POST'])
def register():
    try:
        username = request.form.get("username")
        age = request.form.get("age")
        email = request.form.get("email")
        password = request.form.get("password")
        profile_photo = request.files.get("profile_photo")
    except Exception as e:
        return json_err({"error":str(e)})
    
    if not all([username, age, email, password]):
        return json_err({"error":"All fields are Required"}, 400)

    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
        return json_err({"error":"User exist with this email"}, 400)
    
    if profile_photo and check_extenstions(profile_photo.filename):
        filename = secure_filename(profile_photo.filename)
        time_stamp = datetime.datetime.utcnow().strftime("%d%m%Y%H%M%S")

        filename = f"{time_stamp}_{filename}"

        upload_folder = os.path.join(UPLOAD_FOLDERS, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)
        profile_photo.save(file_path)

        relative_path = f"/uploads/{filename}"
    else:
        relative_path = None

    new_user = User(
        username=username,
        age=age,
        email=email,
        profile_photo=relative_path
    )

    new_user.set_password(password)
    new_user.save()

    return json_ok({"user":new_user.to_dict()})

@auth_bp.route("/login", methods=['POST'])
def login():
    try:
        email = request.json.get("email")
        password = request.json.get("password")
    except Exception as e:
        return json_err({"error":str(e)})
    
    if not all([email, password]):
        return json_err({"error":"All Fields Required"}, 400)
    
    user = User.query.filter_by(email=email).first()

    if not user or not  user.check_password(password):
        return json_err({"error":"Wrong Credentials"}, 404)
    
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    return json_ok({"user":user.to_dict(), "access_token":access_token, "refersh_token":refresh_token}, 200)

@auth_bp.route("/forgot_password", methods=['POST'])
def forgot_password():
    pass

