from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


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
