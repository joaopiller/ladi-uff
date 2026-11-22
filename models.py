import re
from datetime import date, datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho",
         "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]


class Diretoria(db.Model):
    __tablename__ = "diretoria"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False, unique=True)
    slug = db.Column(db.String(40), nullable=False, unique=True)
    ordem = db.Column(db.Integer, nullable=False, default=0)
    membros = db.relationship("Membro", back_populates="diretoria",
                              order_by="(Membro.ordem, Membro.nome)")

    def __repr__(self):
        return f"<Diretoria {self.id}: {self.nome}>"


class Membro(db.Model):
    __tablename__ = "membro"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    cargo = db.Column(db.String(60), nullable=False)
    foto = db.Column(db.String(200), nullable=False)
    ordem = db.Column(db.Integer, nullable=False, default=0)
    diretoria_id = db.Column(db.Integer, db.ForeignKey("diretoria.id"), nullable=False)
    diretoria = db.relationship("Diretoria", back_populates="membros")

    def __repr__(self):
        return f"<Membro {self.id}: {self.nome}>"


class Administrador(db.Model):
    __tablename__ = "administrador"
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(40), nullable=False, unique=True)
    senha_hash = db.Column(db.String(256), nullable=False)

    def define_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def confere_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<Administrador {self.id}: {self.usuario}>"


class Artigo(db.Model):
    __tablename__ = "artigo"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    autor = db.Column(db.String(80), nullable=False)
    data_publicacao = db.Column(db.Date, nullable=False, default=date.today)
    imagem = db.Column(db.String(200), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @property
    def paragrafos(self):
        blocos = re.split(r"\n\s*\n", self.conteudo.replace("\r\n", "\n").strip())
        return [" ".join(b.split()) for b in blocos if b.strip()]

    @property
    def resumo(self):
        primeiro = self.paragrafos[0].replace("**", "") if self.paragrafos else ""
        if len(primeiro) <= 160:
            return primeiro
        return primeiro[:160].rsplit(" ", 1)[0] + "..."

    @classmethod
    def recentes(cls):
        return cls.query.order_by(cls.data_publicacao.desc(), cls.id.desc())

    def __repr__(self):
        return f"<Artigo {self.id}: {self.titulo}>"


class Evento(db.Model):
    __tablename__ = "evento"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.String(200), nullable=False)
    data = db.Column(db.Date, nullable=False)
    periodo = db.Column(db.String(60))
    destaque = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def quando(self):
        if self.periodo:
            return self.periodo
        return f"{MESES[self.data.month - 1]} de {self.data.year}"

    @classmethod
    def linha_do_tempo(cls):
        return cls.query.order_by(cls.data, cls.id).all()

    @classmethod
    def destaques(cls):
        return cls.query.filter_by(destaque=True).order_by(cls.data.desc()).limit(4).all()

    def __repr__(self):
        return f"<Evento {self.id}: {self.titulo}>"


class Inscricao(db.Model):
    __tablename__ = "inscricao"
    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(30), nullable=False, unique=True)
    nome = db.Column(db.String(60), nullable=False)
    aberta = db.Column(db.Boolean, nullable=False, default=False)
    link = db.Column(db.String(300))

    @property
    def disponivel(self):
        return self.aberta and bool(self.link)

    @classmethod
    def da_pagina(cls, chave):
        return cls.query.filter_by(chave=chave).first()

    def __repr__(self):
        return f"<Inscricao {self.chave}: {'aberta' if self.aberta else 'fechada'}>"
