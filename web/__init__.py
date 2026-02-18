from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    mail = Mail(app)
    mail.init_app(app)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.getenv('DEL_EMAIL')
    app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from .auth import auth
    from .views import views

    app.register_blueprint(auth)
    app.register_blueprint(views)

    from .models import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context():
        db.create_all()

    return app
