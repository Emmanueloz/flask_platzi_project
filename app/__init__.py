from flask import Flask, flash, request, make_response, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
import unittest

from app.config import Config
from app.models.todos import Todos
from app.utils.db import db


def create_app(test_config=None):
    app = Flask(__name__)
    Bootstrap(app)
    app.config.from_object(Config)
    db.init_app(app)

    if test_config is None:
        # cargar la configuración de instancia, si existe, cuando no se prueba
        app.config.from_pyfile('config.py', silent=True)
    else:
        # cargar la configuración de ensayo si se pasa en
        app.config.from_mapping(test_config)

    todosList = ['Comprar cafe', 'Enviar solicitud',
                 'Entregar video a productor']

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

    from app import auth

    app.register_blueprint(auth.auth)

    from app import todos
    app.register_blueprint(todos.todos)

    @app.route("/")
    def index():
        user_ip = request.remote_addr
        response = make_response(redirect('/hello'))
        session['user_ip'] = user_ip
        return response

    @app.route("/hello")
    def hello():
        user_ip = session.get('user_ip')
        user_id = session.get('user_id')
        user_name = session.get('user_name')
        print(user_id, user_name)
        list_todos = Todos.query.filter(Todos.id_user == user_id).all()
        context = {
            "user_ip": user_ip,
            "todos": list_todos,
            'user_name': user_name
        }

        return render_template('hello.html', **context)

    with app.app_context():
        db.create_all()

    return app
