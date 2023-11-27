from flask import Blueprint, flash, redirect, render_template, session, url_for
from app.forms import LoginForm
from app.utils.db import db
from app.models.user import User

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        passwd = login_form.passwd.data
        users = User.query.filter(
            User.username == username, User.passwd == passwd).all()
        print(len(users))
        if users is None or len(users) == 0:
            flash("Usuario o contraseña invalido")
            print("redirection")
            return redirect(url_for('auth.login'))

        session["user_id"] = users[0].id
        session["user_name"] = users[0].username
        flash("Nombre de usuario registrado con éxito")
        return redirect(url_for('index'))

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
        session['username'] = username
        flash("Nombre de usuario registrado con éxito")
        new_user = User(username, passwd)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('login.html', **context)
