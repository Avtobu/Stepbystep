from flask_mail import Message
from app import mail
from flask import render_template

def send_password_reset_email(user):

    token = user.get_reset_password_token()

    msg = Message(
        "Reset Your Password",
        sender="noreply@example.com",
        recipients=[user.email]
    )

    msg.body = render_template(
        "reset_password.txt",
        user=user,
        token=token
    )

    mail.send(msg)