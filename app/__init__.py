from flask import Flask, request, make_response, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Enviar")


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
            session['username'] = username
            return redirect(url_for('hello'))

        return render_template('hello.html', **context)

    return app
