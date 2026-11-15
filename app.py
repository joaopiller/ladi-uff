import os
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_wtf.csrf import CSRFProtect

from config import config
from dados_iniciais import cria_administrador, popula_banco
from logs import configura_logging
from forms import LoginForm, MembroForm
from imagens import remover_imagem, salvar_imagem
from models import Administrador, Diretoria, Membro, db

app = Flask(__name__)
ambiente = os.environ.get("APP_ENV", "development")
app.config.from_object(config[ambiente])

if not app.config["SECRET_KEY"]:
    raise RuntimeError("Defina a variável de ambiente SECRET_KEY.")

configura_logging(app)
db.init_app(app)
CSRFProtect(app)

with app.app_context():
    db.create_all()
    if popula_banco():
        app.logger.info("Banco populado com os dados iniciais")
    admin = cria_administrador()
    if admin:
        app.logger.info("Administrador criado: %s", admin.usuario)

app.logger.info("Aplicação iniciada (ambiente=%s, debug=%s)", ambiente, app.config["DEBUG"])


@app.before_request
def registra_requisicao():
    if not request.path.startswith("/static/"):
        app.logger.debug("%s %s", request.method, request.path)


def admin_logado():
    admin_id = session.get("admin_id")
    if admin_id is None:
        return None
    return db.session.get(Administrador, admin_id)


def login_obrigatorio(view):
    @wraps(view)
    def protegida(*args, **kwargs):
        if admin_logado() is None:
            flash("Faça login para acessar o painel.", "warning")
            return redirect(url_for("entrar"))
        return view(*args, **kwargs)
    return protegida


@app.context_processor
def variaveis_globais():
    return {"admin_logado": admin_logado()}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/quem-somos")
def quem_somos():
    diretorias = Diretoria.query.order_by(Diretoria.ordem).all()
    diretorias = [d for d in diretorias if d.membros]
    return render_template("quem_somos.html", diretorias=diretorias)


@app.route("/eventos")
def eventos():
    return render_template("eventos.html")


@app.route("/clube-de-leitura")
def clube():
    return render_template("clube.html")


@app.route("/admin/login", methods=["GET", "POST"])
def entrar():
    if admin_logado():
        return redirect(url_for("painel"))

    form = LoginForm()
    if form.validate_on_submit():
        admin = Administrador.query.filter_by(usuario=form.usuario.data).first()
        if admin and admin.confere_senha(form.senha.data):
            session.clear()
            session["admin_id"] = admin.id
            app.logger.info("Login do administrador: %s", admin.usuario)
            return redirect(url_for("painel"))
        app.logger.warning("Tentativa de login inválida para o usuário %r", form.usuario.data)
        flash("Usuário ou senha inválidos.", "danger")
    return render_template("admin/login.html", form=form)


@app.route("/admin/sair", methods=["POST"])
def sair():
    session.clear()
    flash("Você saiu do painel.", "info")
    return redirect(url_for("entrar"))


@app.route("/admin")
@login_obrigatorio
def painel():
    return render_template("admin/painel.html", total_membros=Membro.query.count())


@app.route("/admin/membros")
@login_obrigatorio
def admin_membros():
    diretorias = Diretoria.query.order_by(Diretoria.ordem).all()
    return render_template("admin/membros.html", diretorias=diretorias)


def opcoes_diretorias():
    return [(d.id, d.nome) for d in Diretoria.query.order_by(Diretoria.ordem).all()]


@app.route("/admin/membros/novo", methods=["GET", "POST"])
@login_obrigatorio
def novo_membro():
    form = MembroForm()
    form.diretoria_id.choices = opcoes_diretorias()
    if form.validate_on_submit():
        if not form.foto.data:
            form.foto.errors.append("Envie uma foto do membro.")
        else:
            membro = Membro(
                nome=form.nome.data,
                cargo=form.cargo.data,
                diretoria_id=form.diretoria_id.data,
                ordem=form.ordem.data or 0,
                foto=salvar_imagem(form.foto.data, "membros"),
            )
            db.session.add(membro)
            db.session.commit()
            app.logger.info("Membro criado: id=%s nome=%r", membro.id, membro.nome)
            flash(f"{membro.nome} foi adicionado(a).", "success")
            return redirect(url_for("admin_membros"))
    return render_template("admin/membro_form.html", form=form, membro=None,
                           titulo="Novo membro")


@app.errorhandler(404)
def nao_encontrado(erro):
    app.logger.warning("404: %s %s", request.method, request.path)
    return render_template("404.html"), 404


@app.errorhandler(413)
def arquivo_grande(erro):
    app.logger.warning("Upload acima do limite em %s", request.path)
    flash("A imagem é grande demais. O limite é de 5 MB.", "danger")
    return redirect(request.url)


@app.errorhandler(500)
def erro_interno(erro):
    app.logger.exception("Erro 500 em %s", request.path)
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
