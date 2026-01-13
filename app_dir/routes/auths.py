from flask import Blueprint, request
from app_dir import json_err, json_ok, UPLOAD_FOLDERS, check_extenstions
from werkzeug.utils import secure_filename
import datetime, os
from app_dir.models import *
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from random import random, randint

auth_bp = Blueprint("auths", __name__, url_prefix="/auths")


# Register User
@auth_bp.route("/register", methods=['POST'])
def register():
    try:
        username = request.form.get("username")
        phone = request.form.get("phone")
        age = request.form.get("age")
        email = request.form.get("email")
        password = request.form.get("password")
        profile_photo = request.files.get("profile_photo")
    except Exception as e:
        return json_err({"error":str(e)})
    
    if not all([username, age, email, password, phone]):
        return json_err({"error":"All fields are Required"}, 400)

    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
        return json_err({"error":"User exist with this email"}, 400)
    
    if profile_photo and check_extenstions(profile_photo.filename):
        filename = secure_filename(profile_photo.filename)
        time_stamp = datetime.datetime.utcnow().strftime("%d%m%Y%H%M%S")

        filename = f"{time_stamp}_{filename}"

        upload_folder = os.path.join(UPLOAD_FOLDERS)
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)
        profile_photo.save(file_path)

        relative_path = f"/uploads/{filename}"
    else:
        relative_path = None

    new_user = User(
        username=username,
        phone=phone,
        age=age,
        email=email,
        profile_photo=relative_path
    )

    new_user.set_password(password)
    new_user.save()

    return json_ok({"user":new_user.to_dict()})

# Login User
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
        return json_err({"error":"Wrong Credentials"}, 400)
    
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    return json_ok({"user":user.to_dict(), "access_token":access_token, "refersh_token":refresh_token}, 200)

# forget password
@auth_bp.route("/forgot_password", methods=['POST'])
def forgot_password():
    email = request.json.get("email")

    if not email:
        return json_err({"error":"You must enter your email"}, 400)
    
    user = User.query.filter_by(email=email).first()

    if not user:
        return json_err({"error":"This Email is not register with any account"}, 400)
    
    reset_code = str(random())[5:11]
    
    user.reset_code = reset_code
    user.save()

    return json_ok({"reset_code":reset_code})

# Password reset code
@auth_bp.route("/check_reset_code", methods=['POST'])
def check_reset_code():
    try:
        reset_code = request.json.get("reset_code")
    except Exception as e:
        return json_err({"error":str(e)},400)
    
    if not reset_code:
        return json_err({"error":"You did'nt enter a code"})
    
    user = User.query.filter_by(reset_code=reset_code).first()

    if not user:
        return json_err({"error":"wrong code"}, 400)
    
    user.reset_code = None
    user.save()
    
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    return json_ok({"user":user.to_dict(),
                    "access_token":access_token,
                    "refresh_token":refresh_token
                    })

# Reset password route
@auth_bp.route("/reset_password", methods=['GET'])
@jwt_required()
def reset_password():
    try:
        user_id = int(get_jwt_identity())
        new_password = request.args.get("new_password", type=str)
    except Exception as e:
        return json_err({"error":str(e)})

    if not new_password:
        return json_err({"error":"You did't enter password"}, 404)
    
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return json_err({"error":"User Not found Please Login first"})
    
    user.set_password(new_password)
    user.save()

    return json_ok({"user":user.to_dict()})

@auth_bp.route("refresh_user", methods=['GET'])
@jwt_required()
def refresh_user():
    try:
        user_id = int(get_jwt_identity())
    except Exception as e:
        return json_err({"error":str(e)})
    
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return json_err({"error":"Please Login again"})

    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    return json_ok({
        "user":user.to_dict(),
        "access_token":access_token,
        "refresh_token":refresh_token
    })
