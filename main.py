from flask import Flask
from config import config
from database import db
from mail import mail

# from routes.auth import auth_routes
# from routes.user import user_routes
# from routes.decks import deck_routes
# from routes.cards import card_routes
# from routes.progress import progress_routes


def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    mail.init_app(app)

    # app.register_blueprint(auth_routes, url_prefix="/api/auth")
    # app.register_blueprint(user_routes, url_prefix="/api/user")
    # app.register_blueprint(deck_routes, url_prefix="/api/decks")
    # app.register_blueprint(card_routes, url_prefix="/api/cards")
    # app.register_blueprint(progress_routes, url_prefix="/api/progress")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
