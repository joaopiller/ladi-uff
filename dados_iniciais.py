import os

from models import Administrador, Diretoria, Membro, db

DIRETORIAS = [
    ("Direção executiva", "executiva", [
        ("Victória Lyra", "Presidência", "victoria-lyra.jpg"),
        ("Nina Macedo", "Vice-presidência", "nina-macedo.jpg"),
        ("Pietra Moura", "Coordenação", "pietra-moura.jpg"),
    ]),
    ("Ensino & Pesquisa", "ensino", [
        ("Felipe Coelho", "Direção", "felipe-coelho.jpg"),
        ("Brayan Alexander de Mello", "Integrante", "brayan-alexander.jpg"),
        ("Mariane Pio", "Integrante", "mariane-pio.jpg"),
        ("Júlia Valente", "Integrante", "julia-valente.jpg"),
        ("Lucas Presotto Moreira", "Integrante", "lucas-presotto.jpg"),
    ]),
    ("Comunicação", "comunicacao", [
        ("Andressa Farias", "Integrante", "andressa-farias.jpg"),
        ("Yasmin Trino", "Integrante", "yasmin-trino.jpg"),
        ("Arthur Lebelein", "Integrante", "arthur-lebelein.jpg"),
        ("Clarissa Lemos", "Integrante", "clarissa-lemos.jpg"),
    ]),
    ("Eventos", "eventos", [
        ("Ian Abicalil", "Direção", "ian-abicalil.jpg"),
        ("Luiza Lody", "Integrante", "luiza-lody.jpg"),
        ("João Bonjardim", "Integrante", "joao-bonjardim.jpg"),
        ("Beatriz Coutinho", "Integrante", "beatriz-coutinho.jpg"),
        ("Maria Clara Capua Sana", "Integrante", "maria-clara-sana.jpg"),
        ("Luísa Valentina Costa", "Integrante", "luiza-valentina.jpg"),
    ]),
]


def popula_banco():
    if Diretoria.query.count() > 0:
        return False

    for ordem, (nome, slug, membros) in enumerate(DIRETORIAS):
        diretoria = Diretoria(nome=nome, slug=slug, ordem=ordem)
        db.session.add(diretoria)
        for posicao, (nome_membro, cargo, foto) in enumerate(membros, start=1):
            db.session.add(Membro(nome=nome_membro, cargo=cargo, ordem=posicao,
                                  foto="img/diretoria/" + foto, diretoria=diretoria))
    db.session.commit()
    return True


def cria_administrador():
    if Administrador.query.count() > 0:
        return None

    usuario = os.environ.get("ADMIN_USUARIO")
    senha = os.environ.get("ADMIN_SENHA")
    if not usuario or not senha:
        return None

    admin = Administrador(usuario=usuario)
    admin.define_senha(senha)
    db.session.add(admin)
    db.session.commit()
    return admin
