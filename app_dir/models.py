from app_dir import db
import datetime, os

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

def to_dict(self):
    data = {}
    for column in self.__table__.columns:
        value = getattr(self, column.name)
    if isinstance(value, datetime):
        value = value.isoformat()
        data[column.name] = value
    return data
        

class AddUser(BaseModel):

    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
