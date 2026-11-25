from datetime import datetime, timedelta
from functools import wraps

from flask import redirect, session, url_for

from models import Administrador, db

TENTATIVAS_MAXIMAS = 5
TEMPO_BLOQUEIO = timedelta(minutes=15)
tentativas_login = {}


def login_bloqueado(ip):
    registro = tentativas_login.get(ip)
    if registro is None:
        return False
    quantidade, inicio = registro
    if datetime.now() - inicio > TEMPO_BLOQUEIO:
        del tentativas_login[ip]
        return False
    return quantidade >= TENTATIVAS_MAXIMAS


def registra_falha_login(ip):
    quantidade, inicio = tentativas_login.get(ip, (0, datetime.now()))
    tentativas_login[ip] = (quantidade + 1, inicio)


def limpa_falhas_login(ip):
    tentativas_login.pop(ip, None)


def admin_logado():
    admin_id = session.get("admin_id")
    if admin_id is None:
        return None
    return db.session.get(Administrador, admin_id)


def login_obrigatorio(view):
    @wraps(view)
    def protegida(*args, **kwargs):
        if admin_logado() is None:
            return redirect(url_for("entrar"))
        return view(*args, **kwargs)
    return protegida
