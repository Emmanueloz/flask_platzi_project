from flask import Blueprint, render_template
from app.forms import LoginForm


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login')
def login():
    context = {
        'login_form': LoginForm()
    }
    return render_template('login.html', **context)
