import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret"

    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME ="lifeivanna2007@gmail.com"
    MAIL_PASSWORD = "vmsw jzbr tuqd aaix "

