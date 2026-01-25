from app_dir import db
import datetime, os
from werkzeug.security import check_password_hash, generate_password_hash


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    is_deleted = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def soft_delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()
    
    def hard_delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self, exclude=None):
        exclude = exclude or []
        data = {}
        for column in self.__table__.columns:
            if column.name in exclude:
                continue
            value = getattr(self, column.name)
            if isinstance(value, datetime.datetime):
                value = value.isoformat()
            data[column.name] = value
        return data
        

class User(BaseModel):
    __tablename__ = 'users'

    username = db.Column(db.String(200), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profile_photo = db.Column(db.String(250), default=None)
    password_try = db.Column(db.Integer, default=0)
    try_start_time = db.Column(db.DateTime, default=None)
    try_end_time = db.Column(db.DateTime, default=None)

    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Media(BaseModel):
    __tablename__ = "medias"
    title = db.Column(db.String(100), nullable=False)
    video = db.Column(db.String(200), default=None)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    otp_code = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_time_stamp())
    expired_at = db.Column(db.DateTime, default=None)
    