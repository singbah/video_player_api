from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import datetime, os
from pathlib import Path

db = SQLAlchemy()
cors = CORS()

ALLOWED_EXTENSTIONS = {"mp4", "mp3", "png", "jpeg", "jpg"}
UPLOAD_FOLDERS = os.path.join(os.getcwd(), "static", "uploads")
os.makedirs(UPLOAD_FOLDERS, exist_ok=True)

print(str(UPLOAD_FOLDERS))


