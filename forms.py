from datetime import date

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (BooleanField, DateField, IntegerField, PasswordField, SelectField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Length, NumberRange, Optional

FORMATOS_IMAGEM = ["jpg", "jpeg", "png", "webp"]


class FormularioBase(FlaskForm):
    class Meta:
        locales = ["pt"]


class LoginForm(FormularioBase):
    usuario = StringField("Usuário", validators=[DataRequired(), Length(max=40)])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(max=128)])
    entrar = SubmitField("Entrar")


class MembroForm(FormularioBase):
    nome = StringField("Nome", validators=[DataRequired(), Length(max=80)])
    cargo = StringField("Cargo", validators=[DataRequired(), Length(max=60)])
    diretoria_id = SelectField("Diretoria", coerce=int)
    ordem = IntegerField("Posição na aba", validators=[Optional(), NumberRange(min=1, max=99)],
                         description="Deixe em branco para colocar no fim da aba.")
    arquivo = FileField("Foto", validators=[
        FileAllowed(FORMATOS_IMAGEM, "Envie uma imagem JPG, PNG ou WEBP.")])
    salvar = SubmitField("Salvar")


class ArtigoForm(FormularioBase):
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


class EventoForm(FormularioBase):
    titulo = StringField("Nome do evento", validators=[DataRequired(), Length(max=120)])
    categoria = StringField("Categoria", validators=[DataRequired(), Length(max=40)],
                            description="Aparece na etiqueta do card. Ex.: Simulação, Curso, Extensão.")
    data = DateField("Data", validators=[DataRequired()],
                     description="Define a posição do evento na linha do tempo.")
    periodo = StringField("Texto da data", validators=[Optional(), Length(max=60)],
                          description="Opcional. Ex.: 1º semestre de 2026. Em branco, aparece o mês e o ano.")
    descricao = TextAreaField("Descrição", validators=[DataRequired(), Length(max=600)])
    arquivo = FileField("Foto", validators=[
        FileAllowed(FORMATOS_IMAGEM, "Envie uma imagem JPG, PNG ou WEBP.")])
    destaque = BooleanField("Destacar na página inicial")
    salvar = SubmitField("Salvar")
