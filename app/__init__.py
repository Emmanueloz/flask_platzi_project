from flask import Flask, request, make_response, redirect


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        user_ip = request.remote_addr
        response = make_response(redirect('/hello'))
        response.set_cookie('user_ip', user_ip)
        return response

    @app.route("/hello")
    def hello():
        user_ip = request.cookies.get('user_ip')
        return f"<h1>Hello World Flask, your IP is {user_ip}<h1>"

    return app
