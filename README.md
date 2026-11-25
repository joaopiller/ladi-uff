# LADI-UFF

Site e painel administrativo da **Liga Acadêmica de Direito Internacional da UFF**. A diretoria da Liga atualiza membros, artigos, eventos e inscrições pelo painel, sem mexer no código.

**Site:** https://joaopiller.pythonanywhere.com · **Código:** https://github.com/joaopiller/ladi-uff

Projeto da disciplina de Introdução ao Desenvolvimento Web (UFF), feito em duas etapas: o site estático (HTML, CSS, JavaScript e Bootstrap) e a aplicação Flask com banco de dados.

## Destaques

- **Painel administrativo** com login protegido: senha em hash, CSRF, bloqueio após 5 tentativas erradas e sessão de 8 horas.
- **CRUD completo** de membros, artigos, tags e eventos, com upload de imagens validado.
- **Artigos** com busca, filtro por tags, paginação e negrito no texto.
- **Linha do tempo de eventos** sempre em ordem cronológica, com destaques na página inicial.
- **Inscrições** do clube de leitura e das simulações da ONU abertas e fechadas pelo painel.
- **Responsivo**, testado de 320 px a 1440 px, com animações leves que respeitam a opção de reduzir movimento.
- **Logging** em arquivo com rotação e configuração por ambiente (`.env`).

**Tecnologias:** Python, Flask, Jinja2, Flask-WTF, Flask-SQLAlchemy (SQLite), python-dotenv, HTML, CSS, JavaScript e Bootstrap 5.

**Requisitos do trabalho:** 27 rotas, 7 models (`Diretoria`, `Membro`, `Administrador`, `Artigo`, `Tag`, `Evento` e `Inscricao`), 6 formulários Flask-WTF e log em `logs/app.log`.

## Grupo

**Nome:** LADI-UFF

| Integrante | Etapa 1 (site estático) | Etapa 2 (aplicação Flask) |
|---|---|---|
| João Vicente Piller | Página inicial | Estrutura inicial em Flask, login do administrador, front-end do painel e implantação |
| Lucas Silveira | Página Quem somos | Templates das páginas, back-end de membros e telas de membros no painel |
| Gabriela Bittencourt | Menu, rodapé e ajustes para telas pequenas | Configuração por ambiente, back-end de eventos e inscrições e telas deles no painel |
| Ana Laura Neuhaus | Página Eventos | Logging e back-end de artigos e tags |
| Isabella Motta | Página do Clube de leitura | Páginas de erro, visual das páginas de artigos, editor com negrito e desempenho |

## Estrutura

```
├── app.py              criação da aplicação, rotas e páginas de erro
├── autenticacao.py     login do painel e bloqueio de tentativas
├── models.py           tabelas do banco (SQLAlchemy)
├── forms.py            formulários e validações (Flask-WTF)
├── config.py           configurações de desenvolvimento e produção, lidas do .env
├── logs.py             log em arquivo com rotação
├── dados_iniciais.py   carga inicial do banco e primeiro administrador
├── imagens.py          upload e remoção de imagens
├── templates/          páginas Jinja2: base.html, partials/, artigos/, admin/ e páginas de erro
└── static/             css/, js/ e img/ (uploads/ é criada pelo painel e fica fora do Git)
```

O banco SQLite (`instance/`), os logs (`logs/`) e o `.env` são gerados localmente e não vão para o Git.

## Como rodar

```bash
python -m venv venv
source venv/bin/activate        # no Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # defina SECRET_KEY, ADMIN_USUARIO e ADMIN_SENHA
python app.py
```

Acesse http://127.0.0.1:5000. O banco é criado e preenchido na primeira execução.

## Guia de uso

**Visitantes:** naveguem pelas páginas Quem somos, Eventos, Clube de leitura e Artigos. Na página Artigos, dá para buscar por palavra ou clicar em uma tag para filtrar.

**Administradores:**
1. Clique em **Área restrita**, no rodapé, e entre com o usuário e a senha.
2. No menu do painel, escolha o que gerenciar:
   - **Membros:** nome, cargo, diretoria, posição na aba e foto.
   - **Artigos:** título, autor, data, capa, texto e tags. Separe os parágrafos com uma linha em branco e use o botão **Negrito** ou `**texto**`.
   - **Tags:** crie, renomeie ou exclua os temas usados nos artigos.
   - **Eventos:** a data define a posição na linha do tempo, e **Destacar** coloca o evento na página inicial.
   - **Inscrições:** abra ou feche as inscrições do clube e das simulações e troque o link do formulário.
3. Use **Sair**, no topo do painel, ao terminar.

As imagens aceitas são JPG, PNG ou WEBP, de até 5 MB.
