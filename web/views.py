from flask import Blueprint, render_template_string, app
from flask_login import login_required

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template_string("Hello {{ current_user.email }}")
