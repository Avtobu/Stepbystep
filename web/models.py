from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(255))
