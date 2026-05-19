from flask import Flask, send_from_directory
from app.config import Config
from app.extensions import db, login_manager, mail, migrate, csrf
import os


def create_app(config_class=Config):
    app = Flask(__name__, static_folder=None)  # ← вимикаємо вбудований static
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    DIST_DIR = "/app/client/dist"  # абсолютний шлях

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        if path.startswith("api/"):
            return {"error": "Not found"}, 404

        full_path = os.path.join(DIST_DIR, path)

        if path and os.path.exists(full_path) and os.path.isfile(full_path):
            return send_from_directory(DIST_DIR, path)

        return send_from_directory(DIST_DIR, "index.html")

    return app