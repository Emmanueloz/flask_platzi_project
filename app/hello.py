from flask import Blueprint, render_template, session, request, make_response, redirect
from app.models.todos import Todos
from flask_login import login_required

bp = Blueprint("hello", __name__)


@bp.route("/")
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('hello'))
    session['user_ip'] = user_ip
    return response


@bp.route("/hello")
# @login_required
def hello():
    user_ip = session.get('user_ip')
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    print(user_id, user_name)
    list_todos = Todos.query.filter(Todos.id_user == user_id).all()
    context = {
        "user_ip": user_ip,
        "todos": list_todos,
    }
    return render_template('hello.html', **context)
