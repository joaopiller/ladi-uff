import os
import uuid

from werkzeug.utils import secure_filename

PASTA_STATIC = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static")


def salvar_imagem(arquivo, pasta):
    extensao = os.path.splitext(secure_filename(arquivo.filename))[1].lower()
    nome = uuid.uuid4().hex + extensao
    destino = os.path.join(PASTA_STATIC, "uploads", pasta)
    os.makedirs(destino, exist_ok=True)
    arquivo.save(os.path.join(destino, nome))
    return f"uploads/{pasta}/{nome}"


def remover_imagem(caminho):
    if not caminho or not caminho.startswith("uploads/"):
        return
    arquivo = os.path.join(PASTA_STATIC, caminho)
    if os.path.exists(arquivo):
        os.remove(arquivo)
