from datetime import date

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (BooleanField, DateField, IntegerField, PasswordField, SelectField,
                     SelectMultipleField, StringField, SubmitField, TextAreaField)
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Regexp, URL

FORMATOS_IMAGEM = ["jpg", "jpeg", "png", "webp"]


class FormularioBase(FlaskForm):
    class Meta:
        locales = ["pt"]


class CaixasDeSelecao(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


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
    tags_ids = CaixasDeSelecao("Tags", coerce=int)
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


class InscricaoForm(FormularioBase):
    aberta = BooleanField("Inscrições abertas")
    link = StringField("Link do formulário", validators=[
        Optional(), Length(max=300), URL(message="Informe um endereço válido."),
        Regexp(r"^https?://", message="O link deve começar com http:// ou https://.")])
    salvar = SubmitField("Salvar")


class TagForm(FormularioBase):
    nome = StringField("Nome da tag", validators=[DataRequired(), Length(max=40)])
    salvar = SubmitField("Criar tag")
