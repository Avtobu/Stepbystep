import mail
from flask import Blueprint, render_template, request, redirect, url_for, flash
from web.models import User
from . import db
from flask_mail import Mail, Message
import os
import dotenv
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('user')
        password = request.form.get('password')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email is taken", category="error")
            return render_template("signup.html")

        strong, message = User().check_strongpassword(password)
        if not strong:
            flash(message, category="error")
            return render_template("signup.html")

        new_user = User(email=email, user=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('views.home'))
    return render_template("signup.html")


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('views.home'))

        flash("Wrong credentials", category="error")

    return "Login page"


@auth.route("/")

def index():
    return render_template("index.html")

@auth.route("/submit", methods=["POST"])   #is will be changed when i will get front
def submit():
    if request.method== "POST":
        name= request.form["name"]
        #subject request.form["subject"]
        message=  request.form["message"]
        msg = Message("Hello", sender=  os.getenv("EMAIL"), recipients  = [os.getenv('REC_EMAIL')])
        msg.body = "Hello "+name+",\n\n"+message
        mail.send(msg)
    return redirect(url_for("index"))