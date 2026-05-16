from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()   
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()


@login_manager.unauthorized_handler
def unauthorized():
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Unauthorized. Please log in."}), 401