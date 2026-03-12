import os
from datetime import timedelta
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()


class config:
    # Secret key is used to sign JWT tokens. Change this in production!
    SECRET_KEY = os.getenv("SECRET_KEY", "please-change-this-secret")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///stepbystep.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Turns off an unnecessary warning

    JWT_ACCESS_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_EXPIRES = timedelta(days=30)

    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "your-email@gmail.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "your-app-password")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME", "your-email@gmail.com")

    OTP_EXPIRES_MINUTES = 10
