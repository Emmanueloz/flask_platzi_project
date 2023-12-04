from flask import Blueprint, flash, redirect, render_template, session, url_for
from flask_login import login_user, logout_user, current_user
from app.forms import LoginForm
from app.utils.db import db
from app.models.user import User, UserLogin
from werkzeug.security import generate_password_hash, check_password_hash

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
            User.username == username).all()

        if users is None or len(users) == 0:
            flash("Usuario o contraseña invalido")
            return redirect(url_for('auth.login'))
        user: User = users[0]
        if not check_password_hash(user.passwd, passwd):
            flash("Contraseña invalido")
            return redirect(url_for('auth.login'))

        user = UserLogin(user.id, user.username, user.passwd)
        login_user(user)
        return redirect(url_for('hello.index'))

    return render_template('login.html', **context)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    login_form = LoginForm()
    context = {
        'is_signup': True,
        'login_form': login_form
    }
    if login_form.validate_on_submit():

        username = login_form.username.data
        passwd = login_form.passwd.data
        user = User.query.filter(User.username == username).all()

        if user == []:
            flash("Nombre de usuario registrado con éxito")
            passwd_hash = generate_password_hash(passwd)

            new_user = User(username, passwd_hash)
            db.session.add(new_user)
            db.session.commit()
            logout_user()
            return redirect(url_for('auth.login'))
        else:
            flash('El usuario ya existe')

    return render_template('login.html', **context)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
