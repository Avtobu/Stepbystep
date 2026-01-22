from flask import Blueprint, render_template_string, app
from flask_login import login_required
from flask import render_template

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("index.html")