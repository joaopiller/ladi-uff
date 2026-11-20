from datetime import date

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (DateField, IntegerField, PasswordField, SelectField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Length, NumberRange, Optional

FORMATOS_IMAGEM = ["jpg", "jpeg", "png", "webp"]


class LoginForm(FlaskForm):
    usuario = StringField("Usuário", validators=[DataRequired(), Length(max=40)])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(max=128)])
    entrar = SubmitField("Entrar")


class MembroForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(max=80)])
    cargo = StringField("Cargo", validators=[DataRequired(), Length(max=60)])
    diretoria_id = SelectField("Diretoria", coerce=int)
    ordem = IntegerField("Posição na aba", validators=[Optional(), NumberRange(min=1, max=99)],
                         description="Deixe em branco para colocar no fim da aba.")
    arquivo = FileField("Foto", validators=[
        FileAllowed(FORMATOS_IMAGEM, "Envie uma imagem JPG, PNG ou WEBP.")])
    salvar = SubmitField("Salvar")


class ArtigoForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(max=150)])
    autor = StringField("Autor", validators=[DataRequired(), Length(max=80)])
    data_publicacao = DateField("Data de publicação", default=date.today,
                                validators=[DataRequired()])
    arquivo = FileField("Imagem de capa", validators=[
        FileAllowed(FORMATOS_IMAGEM, "Envie uma imagem JPG, PNG ou WEBP.")])
    conteudo = TextAreaField("Texto", validators=[DataRequired()],
                             description="Separe os parágrafos com uma linha em branco. "
                                         "Para deixar um trecho em negrito, escreva **assim**.")
    salvar = SubmitField("Publicar")
