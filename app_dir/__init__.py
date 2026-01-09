from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import datetime, os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()
db = SQLAlchemy()
cors = CORS()

ALLOWED_EXTENSTIONS = {"mp4", "mp3", "png", "jpeg", "jpg"}
UPLOAD_FOLDERS = os.path.join(os.getcwd(), "static", "uploads")
MAX_FILE_LENGTH = 16 * 1024 * 1024
os.makedirs(UPLOAD_FOLDERS, exist_ok=True)

def check_extenstions(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSTIONS


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCMEHY_DATABASE_URI = os.getenv("SQLITE_DATABASE"),
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

    return app