import os

from flask import Flask, render_template

from config import config

app = Flask(__name__)
ambiente = os.environ.get("APP_ENV", "development")
app.config.from_object(config[ambiente])

if not app.config["SECRET_KEY"]:
    raise RuntimeError("Defina a variável de ambiente SECRET_KEY.")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/quem-somos")
def quem_somos():
    return render_template("quem_somos.html")


@app.route("/eventos")
def eventos():
    return render_template("eventos.html")


@app.route("/clube-de-leitura")
def clube():
    return render_template("clube.html")


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
