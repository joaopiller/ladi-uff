from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    usuario = StringField("Usuário", validators=[DataRequired(), Length(max=40)])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(max=128)])
    entrar = SubmitField("Entrar")
