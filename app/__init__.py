from flask import Flask, request, make_response, redirect, render_template, session
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    todos = ['Comprar cafe', 'Enviar solicitud', 'Entregar video a productor']

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

    @app.route("/hello")
    def hello():

        # user_ip = request.cookies.get('user_ip')
        user_ip = session.get('user_ip')
        context = {
            "user_ip": user_ip,
            "todos": todos
        }
        return render_template('hello.html', **context)

    return app
