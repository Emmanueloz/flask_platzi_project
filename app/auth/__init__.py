from flask import Blueprint, flash, redirect, render_template, session, url_for
from flask_login import login_user, logout_user, current_user
from app.forms import LoginForm
from app.utils.db import db
from app.models.user import User, UserLogin

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('hello.index'))
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        passwd = login_form.passwd.data
        users: list = User.query.filter(
            User.username == username, User.passwd == passwd).all()

        if users is None or len(users) == 0:
            flash("Usuario o contraseña invalido")
            return redirect(url_for('auth.login'))

        user: User = users[0]

        user = UserLogin(user.id, user.username, user.passwd)
        login_user(user)
        return redirect(url_for('hello.index'))

    return render_template('login.html', **context)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        passwd = login_form.passwd.data
        flash("Nombre de usuario registrado con éxito")
        new_user = User(username, passwd)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('login.html', **context)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
