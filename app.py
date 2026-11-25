import os
import re

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_wtf.csrf import CSRFError, CSRFProtect
from markupsafe import Markup, escape
from sqlalchemy import or_
from werkzeug.middleware.proxy_fix import ProxyFix

from autenticacao import (admin_logado, limpa_falhas_login, login_bloqueado, login_obrigatorio,
                          registra_falha_login)
from config import config
from dados_iniciais import cria_administrador, popula_banco
from forms import ArtigoForm, EventoForm, InscricaoForm, LoginForm, MembroForm, TagForm
from imagens import remover_imagem, salvar_imagem
from logs import configura_logging
from models import Administrador, Artigo, Diretoria, Evento, Inscricao, Membro, Tag, db

app = Flask(__name__)
ambiente = os.environ.get("APP_ENV", "development")
app.config.from_object(config[ambiente])

if not app.config["SECRET_KEY"]:
    raise RuntimeError("Defina a variável de ambiente SECRET_KEY.")

configura_logging(app)
db.init_app(app)
CSRFProtect(app)

if not app.config["DEBUG"]:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

with app.app_context():
    db.create_all()
    if popula_banco():
        app.logger.info("Banco populado com os dados iniciais")
    admin = cria_administrador()
    if admin:
        app.logger.info("Administrador criado: %s", admin.usuario)
    elif Administrador.query.count() == 0:
        app.logger.warning("Nenhum administrador cadastrado: defina ADMIN_USUARIO e ADMIN_SENHA no .env")

app.logger.info("Aplicação iniciada (ambiente=%s, debug=%s)", ambiente, app.config["DEBUG"])


@app.after_request
def cabecalhos_seguranca(resposta):
    resposta.headers["X-Frame-Options"] = "SAMEORIGIN"
    resposta.headers["X-Content-Type-Options"] = "nosniff"
    resposta.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return resposta


@app.before_request
def registra_requisicao():
    if not request.path.startswith("/static/"):
        app.logger.debug("%s %s", request.method, request.path)


@app.template_filter("negrito")
def negrito(texto):
    texto = str(escape(texto))
    return Markup(re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", texto))


@app.context_processor
def variaveis_globais():
    return {"admin_logado": admin_logado()}


@app.route("/")
def index():
    artigos = Artigo.recentes().limit(3).all()
    return render_template("index.html", artigos=artigos, destaques=Evento.destaques())


@app.route("/quem-somos")
def quem_somos():
    diretorias = Diretoria.query.order_by(Diretoria.ordem).all()
    diretorias = [d for d in diretorias if d.membros]
    return render_template("quem_somos.html", diretorias=diretorias)


@app.route("/eventos")
def eventos():
    return render_template("eventos.html", eventos=Evento.linha_do_tempo(),
                           inscricao=Inscricao.da_pagina("simulacoes"))


@app.route("/clube-de-leitura")
def clube():
    return render_template("clube.html", inscricao=Inscricao.da_pagina("clube"))


ARTIGOS_POR_PAGINA = 12


@app.route("/artigos")
def artigos():
    busca = request.args.get("q", "").strip()
    tag_ativa = None
    consulta = Artigo.recentes()

    slug = request.args.get("tag", "").strip()
    if slug:
        tag_ativa = Tag.query.filter_by(slug=slug).first_or_404()
        consulta = consulta.filter(Artigo.tags.any(Tag.id == tag_ativa.id))

    if busca:
        app.logger.debug("Busca de artigos: %r", busca)
        consulta = consulta.filter(or_(
            Artigo.titulo.contains(busca),
            Artigo.autor.contains(busca),
            Artigo.conteudo.contains(busca),
            Artigo.tags.any(Tag.nome.contains(busca)),
        ))

    pagina = request.args.get("pagina", 1, type=int)
    paginacao = consulta.paginate(page=pagina, per_page=ARTIGOS_POR_PAGINA, error_out=False)
    if paginacao.pages and pagina > paginacao.pages:
        return redirect(url_for("artigos", pagina=paginacao.pages, q=busca or None,
                                tag=tag_ativa.slug if tag_ativa else None))
    tags = Tag.query.filter(Tag.artigos.any()).order_by(Tag.nome).all()
    return render_template("artigos/lista.html", artigos=paginacao.items, paginacao=paginacao,
                           busca=busca, tags=tags, tag_ativa=tag_ativa)


@app.route("/artigos/<int:id>")
def artigo(id):
    artigo = db.get_or_404(Artigo, id)
    return render_template("artigos/artigo.html", artigo=artigo)


@app.route("/admin/login", methods=["GET", "POST"])
def entrar():
    if admin_logado():
        return redirect(url_for("painel"))

    form = LoginForm()
    ip = request.remote_addr
    if form.validate_on_submit():
        if login_bloqueado(ip):
            app.logger.warning("Login bloqueado por excesso de tentativas: ip=%s", ip)
            flash("Muitas tentativas seguidas. Aguarde alguns minutos e tente de novo.", "danger")
            return render_template("admin/login.html", form=form), 429

        admin = Administrador.query.filter_by(usuario=form.usuario.data).first()
        if admin and admin.confere_senha(form.senha.data):
            limpa_falhas_login(ip)
            session.clear()
            session.permanent = True
            session["admin_id"] = admin.id
            app.logger.info("Login do administrador: %s", admin.usuario)
            return redirect(url_for("painel"))

        registra_falha_login(ip)
        app.logger.warning("Tentativa de login inválida para o usuário %r (ip=%s)", form.usuario.data, ip)
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
    return render_template("admin/painel.html", total_membros=Membro.query.count(),
                           total_artigos=Artigo.query.count(),
                           total_tags=Tag.query.count(),
                           total_eventos=Evento.query.count(),
                           inscricoes=Inscricao.query.order_by(Inscricao.id).all())


@app.route("/admin/membros")
@login_obrigatorio
def admin_membros():
    diretorias = Diretoria.query.order_by(Diretoria.ordem).all()
    return render_template("admin/membros.html", diretorias=diretorias)


def opcoes_diretorias():
    return [(d.id, d.nome) for d in Diretoria.query.order_by(Diretoria.ordem).all()]


def proxima_posicao(diretoria_id):
    ultimo = (Membro.query.filter_by(diretoria_id=diretoria_id)
              .order_by(Membro.ordem.desc()).first())
    return ultimo.ordem + 1 if ultimo else 1


@app.route("/admin/membros/novo", methods=["GET", "POST"])
@login_obrigatorio
def novo_membro():
    form = MembroForm()
    form.diretoria_id.choices = opcoes_diretorias()
    valido = form.validate_on_submit()
    if request.method == "POST" and not form.arquivo.data:
        form.arquivo.errors.append("Envie uma foto do membro.")
        valido = False
    if valido:
        membro = Membro(
            nome=form.nome.data,
            cargo=form.cargo.data,
            diretoria_id=form.diretoria_id.data,
            ordem=form.ordem.data or proxima_posicao(form.diretoria_id.data),
            foto=salvar_imagem(form.arquivo.data, "membros"),
        )
        db.session.add(membro)
        db.session.commit()
        app.logger.info("Membro criado: id=%s nome=%r", membro.id, membro.nome)
        flash(f"{membro.nome} foi adicionado(a).", "success")
        return redirect(url_for("admin_membros"))
    return render_template("admin/membro_form.html", form=form, membro=None,
                           titulo="Novo membro")


@app.route("/admin/membros/<int:id>/editar", methods=["GET", "POST"])
@login_obrigatorio
def editar_membro(id):
    membro = db.get_or_404(Membro, id)
    form = MembroForm(obj=membro)
    form.diretoria_id.choices = opcoes_diretorias()
    if form.validate_on_submit():
        membro.nome = form.nome.data
        membro.cargo = form.cargo.data
        if form.ordem.data:
            membro.ordem = form.ordem.data
        elif form.diretoria_id.data != membro.diretoria_id:
            membro.ordem = proxima_posicao(form.diretoria_id.data)
        membro.diretoria_id = form.diretoria_id.data
        if form.arquivo.data:
            remover_imagem(membro.foto)
            membro.foto = salvar_imagem(form.arquivo.data, "membros")
        db.session.commit()
        app.logger.info("Membro atualizado: id=%s nome=%r", membro.id, membro.nome)
        flash(f"Dados de {membro.nome} atualizados.", "success")
        return redirect(url_for("admin_membros"))
    return render_template("admin/membro_form.html", form=form, membro=membro,
                           titulo="Editar membro")


@app.route("/admin/membros/<int:id>/excluir", methods=["POST"])
@login_obrigatorio
def excluir_membro(id):
    membro = db.get_or_404(Membro, id)
    remover_imagem(membro.foto)
    db.session.delete(membro)
    db.session.commit()
    app.logger.warning("Membro removido: id=%s nome=%r", id, membro.nome)
    flash(f"{membro.nome} foi removido(a).", "warning")
    return redirect(url_for("admin_membros"))


@app.route("/admin/artigos")
@login_obrigatorio
def admin_artigos():
    return render_template("admin/artigos.html", artigos=Artigo.recentes().all())


def opcoes_tags():
    return [(t.id, t.nome) for t in Tag.query.order_by(Tag.nome).all()]


def tags_escolhidas(form):
    if not form.tags_ids.data:
        return []
    return Tag.query.filter(Tag.id.in_(form.tags_ids.data)).all()


@app.route("/admin/artigos/novo", methods=["GET", "POST"])
@login_obrigatorio
def novo_artigo():
    form = ArtigoForm()
    form.tags_ids.choices = opcoes_tags()
    valido = form.validate_on_submit()
    if request.method == "POST" and not form.arquivo.data:
        form.arquivo.errors.append("Envie uma imagem de capa.")
        valido = False
    if valido:
        artigo = Artigo(
            titulo=form.titulo.data,
            autor=form.autor.data,
            data_publicacao=form.data_publicacao.data,
            conteudo=form.conteudo.data,
            imagem=salvar_imagem(form.arquivo.data, "artigos"),
            tags=tags_escolhidas(form),
        )
        db.session.add(artigo)
        db.session.commit()
        app.logger.info("Artigo publicado: id=%s titulo=%r", artigo.id, artigo.titulo)
        flash("Artigo publicado.", "success")
        return redirect(url_for("admin_artigos"))
    return render_template("admin/artigo_form.html", form=form, artigo=None,
                           titulo="Novo artigo")


@app.route("/admin/artigos/<int:id>/editar", methods=["GET", "POST"])
@login_obrigatorio
def editar_artigo(id):
    artigo = db.get_or_404(Artigo, id)
    form = ArtigoForm(obj=artigo)
    form.tags_ids.choices = opcoes_tags()
    if request.method == "GET":
        form.tags_ids.data = [t.id for t in artigo.tags]
    form.salvar.label.text = "Salvar alterações"
    if form.validate_on_submit():
        artigo.titulo = form.titulo.data
        artigo.autor = form.autor.data
        artigo.data_publicacao = form.data_publicacao.data
        artigo.conteudo = form.conteudo.data
        artigo.tags = tags_escolhidas(form)
        if form.arquivo.data:
            remover_imagem(artigo.imagem)
            artigo.imagem = salvar_imagem(form.arquivo.data, "artigos")
        db.session.commit()
        app.logger.info("Artigo atualizado: id=%s titulo=%r", artigo.id, artigo.titulo)
        flash("Artigo atualizado.", "success")
        return redirect(url_for("admin_artigos"))
    return render_template("admin/artigo_form.html", form=form, artigo=artigo,
                           titulo="Editar artigo")


@app.route("/admin/artigos/<int:id>/excluir", methods=["POST"])
@login_obrigatorio
def excluir_artigo(id):
    artigo = db.get_or_404(Artigo, id)
    remover_imagem(artigo.imagem)
    db.session.delete(artigo)
    db.session.commit()
    app.logger.warning("Artigo removido: id=%s titulo=%r", id, artigo.titulo)
    flash(f"O artigo \"{artigo.titulo}\" foi removido.", "warning")
    return redirect(url_for("admin_artigos"))


def tag_repetida(nome, ignorar_id=None):
    slug = Tag.gera_slug(nome)
    consulta = Tag.query.filter(or_(Tag.nome == nome, Tag.slug == slug))
    if ignorar_id is not None:
        consulta = consulta.filter(Tag.id != ignorar_id)
    return consulta.first() is not None


@app.route("/admin/tags", methods=["GET", "POST"])
@login_obrigatorio
def admin_tags():
    form = TagForm()
    if form.validate_on_submit():
        nome = form.nome.data.strip()
        if not Tag.gera_slug(nome):
            form.nome.errors.append("Use pelo menos uma letra ou número.")
        elif tag_repetida(nome):
            form.nome.errors.append("Já existe uma tag com esse nome.")
        else:
            tag = Tag(nome=nome, slug=Tag.gera_slug(nome))
            db.session.add(tag)
            db.session.commit()
            app.logger.info("Tag criada: id=%s nome=%r", tag.id, tag.nome)
            flash(f"Tag \"{tag.nome}\" criada.", "success")
            return redirect(url_for("admin_tags"))
    tags = Tag.query.order_by(Tag.nome).all()
    return render_template("admin/tags.html", form=form, tags=tags)


@app.route("/admin/tags/<int:id>/editar", methods=["GET", "POST"])
@login_obrigatorio
def editar_tag(id):
    tag = db.get_or_404(Tag, id)
    form = TagForm(obj=tag)
    form.salvar.label.text = "Salvar"
    if form.validate_on_submit():
        nome = form.nome.data.strip()
        if not Tag.gera_slug(nome):
            form.nome.errors.append("Use pelo menos uma letra ou número.")
        elif tag_repetida(nome, ignorar_id=tag.id):
            form.nome.errors.append("Já existe uma tag com esse nome.")
        else:
            tag.nome = nome
            tag.slug = Tag.gera_slug(nome)
            db.session.commit()
            app.logger.info("Tag atualizada: id=%s nome=%r", tag.id, tag.nome)
            flash("Tag atualizada.", "success")
            return redirect(url_for("admin_tags"))
    return render_template("admin/tag_form.html", form=form, tag=tag)


@app.route("/admin/tags/<int:id>/excluir", methods=["POST"])
@login_obrigatorio
def excluir_tag(id):
    tag = db.get_or_404(Tag, id)
    tag.artigos = []
    db.session.delete(tag)
    db.session.commit()
    app.logger.warning("Tag removida: id=%s nome=%r", id, tag.nome)
    flash(f"A tag \"{tag.nome}\" foi removida dos artigos e excluída.", "warning")
    return redirect(url_for("admin_tags"))


@app.route("/admin/eventos")
@login_obrigatorio
def admin_eventos():
    return render_template("admin/eventos.html", eventos=Evento.linha_do_tempo())


def preenche_evento(evento, form):
    evento.titulo = form.titulo.data
    evento.categoria = form.categoria.data
    evento.data = form.data.data
    evento.periodo = form.periodo.data or None
    evento.descricao = form.descricao.data
    evento.destaque = form.destaque.data


@app.route("/admin/eventos/novo", methods=["GET", "POST"])
@login_obrigatorio
def novo_evento():
    form = EventoForm()
    valido = form.validate_on_submit()
    if request.method == "POST" and not form.arquivo.data:
        form.arquivo.errors.append("Envie uma foto do evento.")
        valido = False
    if valido:
        evento = Evento()
        preenche_evento(evento, form)
        evento.imagem = salvar_imagem(form.arquivo.data, "eventos")
        db.session.add(evento)
        db.session.commit()
        app.logger.info("Evento criado: id=%s titulo=%r", evento.id, evento.titulo)
        flash("Evento adicionado à linha do tempo.", "success")
        return redirect(url_for("admin_eventos"))
    return render_template("admin/evento_form.html", form=form, evento=None,
                           titulo="Novo evento")


@app.route("/admin/eventos/<int:id>/editar", methods=["GET", "POST"])
@login_obrigatorio
def editar_evento(id):
    evento = db.get_or_404(Evento, id)
    form = EventoForm(obj=evento)
    if form.validate_on_submit():
        preenche_evento(evento, form)
        if form.arquivo.data:
            remover_imagem(evento.imagem)
            evento.imagem = salvar_imagem(form.arquivo.data, "eventos")
        db.session.commit()
        app.logger.info("Evento atualizado: id=%s titulo=%r", evento.id, evento.titulo)
        flash("Evento atualizado.", "success")
        return redirect(url_for("admin_eventos"))
    return render_template("admin/evento_form.html", form=form, evento=evento,
                           titulo="Editar evento")


@app.route("/admin/eventos/<int:id>/excluir", methods=["POST"])
@login_obrigatorio
def excluir_evento(id):
    evento = db.get_or_404(Evento, id)
    remover_imagem(evento.imagem)
    db.session.delete(evento)
    db.session.commit()
    app.logger.warning("Evento removido: id=%s titulo=%r", id, evento.titulo)
    flash(f"O evento \"{evento.titulo}\" foi removido.", "warning")
    return redirect(url_for("admin_eventos"))


def formularios_inscricao(inscricao_com_erro=None, form_com_erro=None):
    formularios = []
    for inscricao in Inscricao.query.order_by(Inscricao.id).all():
        if inscricao_com_erro is not None and inscricao.id == inscricao_com_erro.id:
            form = form_com_erro
        else:
            form = InscricaoForm(obj=inscricao, prefix=f"inscricao{inscricao.id}")
        formularios.append((inscricao, form))
    return formularios


@app.route("/admin/inscricoes")
@login_obrigatorio
def admin_inscricoes():
    return render_template("admin/inscricoes.html", formularios=formularios_inscricao())


@app.route("/admin/inscricoes/<int:id>", methods=["POST"])
@login_obrigatorio
def salvar_inscricao(id):
    inscricao = db.get_or_404(Inscricao, id)
    form = InscricaoForm(prefix=f"inscricao{inscricao.id}")
    valido = form.validate_on_submit()
    if form.aberta.data and not form.link.data:
        form.link.errors.append("Para abrir as inscrições, informe o link do formulário.")
        valido = False
    if valido:
        inscricao.aberta = form.aberta.data
        inscricao.link = form.link.data or None
        db.session.commit()
        situacao = "abertas" if inscricao.aberta else "fechadas"
        app.logger.info("Inscrições de %s %s (link=%s)", inscricao.chave, situacao, inscricao.link)
        flash(f"Inscrições de {inscricao.nome}: {situacao}.", "success")
        return redirect(url_for("admin_inscricoes"))
    return render_template("admin/inscricoes.html",
                           formularios=formularios_inscricao(inscricao, form))


@app.errorhandler(404)
def nao_encontrado(erro):
    app.logger.warning("404: %s %s", request.method, request.path)
    return render_template("404.html"), 404


@app.errorhandler(CSRFError)
def formulario_expirado(erro):
    app.logger.warning("CSRF inválido em %s %s: %s", request.method, request.path, erro.description)
    return render_template("400.html"), 400


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
