import os
from flask import send_from_directory
from app.main import main_bp

DIST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "client", "dist")

@main_bp.route("/", defaults={"path": ""})
@main_bp.route("/<path:path>")
def serve_vue(path):
    file_path = os.path.join(DIST_DIR, path)
    if path and os.path.exists(file_path):
        return send_from_directory(DIST_DIR, path)
    return send_from_directory(DIST_DIR, "index.html")