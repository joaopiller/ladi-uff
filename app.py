import os

from flask import Flask, render_template, request

from config import config
from dados_iniciais import cria_administrador, popula_banco
from logs import configura_logging
from models import Diretoria, db

app = Flask(__name__)
ambiente = os.environ.get("APP_ENV", "development")
app.config.from_object(config[ambiente])

if not app.config["SECRET_KEY"]:
    raise RuntimeError("Defina a variável de ambiente SECRET_KEY.")

configura_logging(app)
db.init_app(app)

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


@app.errorhandler(404)
def nao_encontrado(erro):
    app.logger.warning("404: %s %s", request.method, request.path)
    return render_template("404.html"), 404


@app.errorhandler(500)
def erro_interno(erro):
    app.logger.exception("Erro 500 em %s", request.path)
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
