from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from . import db

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable = False)
    email = db.Column(db.String(150), unique=True, nullable = False)
    password_hash = db.Column(db.String(255), nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps(self.id)

    @staticmethod
    def verify_reset_password_token(token, expires=600):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires)
        except:
            return None
        return db.session.get(User, user_id)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))