from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import datetime, os, json, logging
from pathlib import Path
from dotenv import load_dotenv
import logging
from flask_mail import Mail
from logging.handlers import RotatingFileHandler
from uuid import uuid4

load_dotenv()
db = SQLAlchemy()
cors = CORS()
jwt = JWTManager()
mail = Mail()

def create_token(length=6):
    return uuid4().hex[0:length]

ALLOWED_EXTENSTIONS = {"mp4", "mp3", "png", "jpeg", "jpg"}
UPLOAD_FOLDERS = os.path.join(os.getcwd(), "static", "uploads")
MAX_FILE_LENGTH = 16 * 1024 * 1024
os.makedirs(UPLOAD_FOLDERS, exist_ok=True)

def check_extenstions(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSTIONS

def json_ok(payload, code=200):
    if not payload:
        payload = {}
    payload['ok'] = "Success"
    payload['time_stamp'] =  datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    return jsonify(payload), code

def json_err(payload, code=400):
    if not payload:
        payload = {}
    payload['msg'] = "An error occur"
    return jsonify(payload), code

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI = os.getenv("SQLITE_DATABASE"),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SECRET_KEY = os.getenv("API_KEY"),
        JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY"),
        JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=5),
        JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30),
        UPLOAD_FOLDER=UPLOAD_FOLDERS,
        MAX_CONTENT_LENGTH = MAX_FILE_LENGTH
    )
    
    cors.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    
    from app_dir.routes import all_bps
    for bp in all_bps:
        app.register_blueprint(bp)
    
    return app
