import unittest
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from app.config import Config
from app.models.user import UserLogin
from app.utils.db import db

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_name):
    return UserLogin.query(user_name)


def create_app(test_config=None):
    app = Flask(__name__)
    Bootstrap(app)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)

    if test_config is None:
        # cargar la configuración de instancia, si existe, cuando no se prueba
        app.config.from_pyfile('config.py', silent=True)
    else:
        # cargar la configuración de ensayo si se pasa en
        app.config.from_mapping(test_config)

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

    from app import hello
    app.register_blueprint(hello.bp)

    with app.app_context():
        db.create_all()

    return app
