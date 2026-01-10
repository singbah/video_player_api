from app_dir import db, create_app, UPLOAD_FOLDERS, json_ok
from flask import send_file
import os, datetime

app = create_app()

@app.route("/uploads/<filename>")
def get_file(filename):
    return send_file(f"/{UPLOAD_FOLDERS}/{filename}")


if __name__=="__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(debug=True, port=8080)

