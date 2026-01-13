from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os

db = SQLAlchemy()
mail = Mail()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
    app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')

    app.config['SECURITY_TOTP_ISSUER'] = 'StepByStep'
    app.config['SECURITY_TOTP_SECRETS'] = {'default': 'JBSWY3DPEHPK3PXP'}

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config['SECURITY_TWO_FACTOR_ENABLED_METHODS'] = ['email', 'authenticator']
    app.config['SECURITY_TWO_FACTOR'] = True
    app.config['SECURITY_TWO_FACTOR_ALWAYS_VALIDATE'] = False
    app.config['SECURITY_TWO_FACTOR_LOGIN_VALIDITY'] = "1 week"

    db.init_app(app)
    mail.init_app(app)

    from .models import User, Role

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_database(app)
    return app

def create_database(app):
    with app.app_context():
        from . import models
        db.create_all()
        print("Database tables created")
