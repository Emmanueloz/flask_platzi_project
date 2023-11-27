from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    passwd = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Enviar")


class TodosForm(FlaskForm):
    id_user = HiddenField('Usuario', validators=[DataRequired()])
    description = TextAreaField("Descripción", validators=[DataRequired()])
    submit = SubmitField("Enviar")
