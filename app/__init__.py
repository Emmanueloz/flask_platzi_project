from flask import Flask, flash, request, make_response, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
import unittest

from app.forms import LoginForm
from app.config import Config


def create_app(test_config=None):
    app = Flask(__name__)
    Bootstrap(app)
    app.config.from_object(Config)

    if test_config is None:
        # cargar la configuración de instancia, si existe, cuando no se prueba
        app.config.from_pyfile('config.py', silent=True)
    else:
        # cargar la configuración de ensayo si se pasa en
        app.config.from_mapping(test_config)

    todos = ['Comprar cafe', 'Enviar solicitud', 'Entregar video a productor']

    @app.cli.command()
    def test():
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner().run(tests)

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html', error=error), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        # abort(500) provoca un error a
        return render_template('500.html', error=error), 500

    @app.route("/")
    def index():
        user_ip = request.remote_addr
        response = make_response(redirect('/hello'))
        # response.set_cookie('user_ip', user_ip)
        session['user_ip'] = user_ip
        return response

    @app.route("/hello", methods=['GET', 'POST'])
    def hello():
        # user_ip = request.cookies.get('user_ip')
        user_ip = session.get('user_ip')
        login_form = LoginForm()
        username = session.get('username')

        context = {
            "user_ip": user_ip,
            "todos": todos,
            'login_form': login_form,
            'username': username
        }

        if login_form.validate_on_submit():
            username = login_form.username.data
            password = login_form.password.data
            print(password)
            session['username'] = username
            flash("Nombre de usuario registrado con éxito")
            return redirect(url_for('hello'))

        return render_template('hello.html', **context)

    return app
