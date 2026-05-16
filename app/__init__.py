from flask import Flask
from app.config import Config
from app.extensions import db, login_manager, mail, migrate, csrf

def create_app(config_class=Config):
    app = Flask(__name__, static_folder="../dist", static_url_path="")
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        if path.startswith("api/"):
            return {"error": "Not found"}, 404
        dist_dir = os.path.join(app.root_path, "../dist")
        if path and os.path.exists(os.path.join(dist_dir, path)):
            return send_from_directory(dist_dir, path)
        return send_from_directory(dist_dir, "index.html")

    return app