# Site da LADI-UFF

Aplicação web da **Liga Acadêmica de Direito Internacional da Universidade Federal Fluminense (LADI-UFF)**, desenvolvida para a disciplina de Introdução ao Desenvolvimento Web.

Na etapa 1, o grupo construiu o site institucional com HTML, CSS, JavaScript e Bootstrap. Na etapa 2, o site virou uma aplicação Flask com banco de dados e um painel administrativo, para que a própria diretoria da Liga atualize membros, artigos, eventos e inscrições sem mexer no código.

- **Aplicação publicada:** https://joaopiller.pythonanywhere.com
- **Código:** https://github.com/joaopiller/ladi

## Grupo

**Nome do grupo:** LADI-UFF

**Integrantes:** João Vicente Piller, Gabriela Bittencourt, Ana Laura Neuhaus, Lucas Silveira e Isabella Motta

### Divisão de tarefas

| Etapa | Integrante | Responsabilidade |
|---|---|---|
| 1 | João Vicente Piller | Página inicial (banner, quem somos, eventos, clube de leitura e professores) |
| 1 | Gabriela Bittencourt | Menu de navegação com submenus, rodapé e ajustes para telas pequenas |
| 1 | Lucas Silveira | Página Quem somos (história, missão e visão, diretorias, membros e perguntas frequentes) |
| 1 | Ana Laura Neuhaus | Página Eventos (linha do tempo e simulações da ONU) |
| 1 | Isabella Motta | Página do Clube de leitura |
| 2 | João Vicente Piller | Estrutura inicial em Flask, login do administrador (back-end), front-end do painel e implantação |
| 2 | Lucas Silveira | Templates das páginas, models e back-end de membros e telas de membros no painel |
| 2 | Gabriela Bittencourt | Configuração por ambiente, back-end de eventos e inscrições, telas de eventos e inscrições no painel e botão da área restrita |
| 2 | Ana Laura Neuhaus | Logging, model e back-end de artigos, páginas de artigos e formulários |
| 2 | Isabella Motta | Páginas de erro, estilo das páginas de artigos, editor com negrito, artigos na página inicial e desempenho |

## Requisitos do trabalho

| Requisito | Mínimo | No projeto |
|---|---|---|
| Rotas | 5 | 23 rotas (6 públicas e 17 do painel), listadas em [Rotas](#rotas) |
| Models | 3 | 6 models: `Diretoria`, `Membro`, `Administrador`, `Artigo`, `Evento` e `Inscricao` |
| Forms | 2 | 5 formulários Flask-WTF: `LoginForm`, `MembroForm`, `ArtigoForm`, `EventoForm` e `InscricaoForm` |
| Log | sim | `logs.py` grava `logs/app.log` com rotação; as rotas registram acessos, logins, criações, edições, exclusões e erros |

## Tecnologias

- **Back-end:** Python 3, Flask, Jinja2, Flask-WTF (WTForms), Flask-SQLAlchemy (SQLite) e python-dotenv
- **Front-end:** HTML5, CSS3, JavaScript e Bootstrap 5.3.3 com Bootstrap Icons (via CDN)
- **Fontes:** Google Fonts (Oswald e Lato)
- **Hospedagem:** PythonAnywhere

## Organização da aplicação

```
ladi/
├── app.py                 cria a aplicação, define as rotas, os tratadores de erro e a segurança do login
├── config.py              configurações por ambiente (desenvolvimento e produção), lidas do .env
├── logs.py                configuração do logging em arquivo com rotação
├── models.py              objeto db e os models (tabelas) do banco
├── forms.py               formulários Flask-WTF e seus validadores
├── dados_iniciais.py      carga inicial do banco e criação do primeiro administrador
├── imagens.py             salva e remove as imagens enviadas pelo painel
├── requirements.txt       dependências do projeto
├── .env.example           modelo das variáveis de ambiente
├── templates/
│   ├── base.html          layout comum a todas as páginas (head, navbar, rodapé e scripts)
│   ├── partials/          trechos reutilizados com {% include %}
│   │   ├── _navbar.html           menu com os submenus de cada página
│   │   ├── _rodape.html           endereço, contatos e link da área restrita
│   │   ├── _membro.html           card de um membro
│   │   ├── _campo.html            campo de formulário com rótulo e mensagens de erro
│   │   ├── _mensagens.html        mensagens do flash()
│   │   └── _botao_inscricao.html  botão de inscrição (aberta ou "em breve")
│   ├── index.html         página inicial
│   ├── quem_somos.html    Quem somos, com os membros vindos do banco
│   ├── eventos.html       linha do tempo e simulações da ONU
│   ├── clube.html         Clube de leitura
│   ├── artigos/
│   │   ├── lista.html     listagem de artigos com busca
│   │   ├── artigo.html    página de um artigo
│   │   └── _card.html     card de artigo (usado na listagem e na página inicial)
│   ├── admin/
│   │   ├── login.html             login do administrador
│   │   ├── _cabecalho.html        cabeçalho e menu do painel
│   │   ├── painel.html            resumo com os totais e o estado das inscrições
│   │   ├── membros.html           membros por diretoria
│   │   ├── membro_form.html       cadastro e edição de membro
│   │   ├── artigos.html           lista de artigos
│   │   ├── artigo_form.html       editor de artigo, com o botão de negrito
│   │   ├── eventos.html           lista de eventos
│   │   ├── evento_form.html       cadastro e edição de evento
│   │   └── inscricoes.html        abrir e fechar inscrições e trocar os links
│   └── 400.html, 404.html, 500.html   páginas de erro
├── static/
│   ├── css/
│   │   ├── global.css     cores, fontes, menu, banners, rodapé e estilos comuns
│   │   ├── home.css       estilos da página inicial
│   │   ├── quem-somos.css, eventos.css, clube.css, artigos.css   estilos de cada página
│   │   └── admin.css      estilos do login e do painel
│   ├── js/
│   │   ├── global.js      cor do menu ao rolar e fechamento do menu no celular
│   │   ├── carrossel.js   setas das abas de membros com mais de 4 pessoas
│   │   ├── confirmar.js   confirmação antes de excluir
│   │   └── editor.js      botão de negrito do editor de artigos
│   ├── img/               imagens do site (banners, eventos, livros, professores e membros)
│   └── uploads/           imagens enviadas pelo painel (criada automaticamente, fora do Git)
├── instance/ladi.db       banco SQLite (criado na primeira execução, fora do Git)
└── logs/app.log           registro de execução (criado automaticamente, fora do Git)
```

Seguindo a separação de responsabilidades vista em aula, `app.py` importa `models.py`, `forms.py`, `config.py` e `logs.py`, mas nenhum deles importa o `app.py`. O objeto `db` é criado em `models.py` e ligado à aplicação com `db.init_app(app)`, evitando importações circulares.

### Banco de dados

| Model | Tabela | Campos principais | Uso |
|---|---|---|---|
| `Diretoria` | `diretoria` | nome, slug, ordem | Abas da seção de membros |
| `Membro` | `membro` | nome, cargo, foto, ordem, diretoria_id | Cards de membros (relacionamento N:1 com `Diretoria`) |
| `Administrador` | `administrador` | usuario, senha_hash | Login do painel (a senha é guardada só como hash) |
| `Artigo` | `artigo` | titulo, autor, data_publicacao, imagem, conteudo | Página de artigos e home |
| `Evento` | `evento` | titulo, categoria, descricao, imagem, data, periodo, destaque | Linha do tempo e mosaico da home |
| `Inscricao` | `inscricao` | chave, nome, aberta, link | Botões de inscrição do clube e das simulações |

Na primeira execução, `db.create_all()` cria as tabelas e `popula_banco()` cadastra as diretorias, os membros, os eventos, os artigos iniciais e as inscrições. O primeiro administrador é criado com o usuário e a senha definidos no `.env`.

### Rotas

| Rota | Método | Função | Descrição |
|---|---|---|---|
| `/` | GET | `index` | Página inicial, com eventos em destaque e artigos recentes |
| `/quem-somos` | GET | `quem_somos` | História, missão, diretorias, membros e perguntas frequentes |
| `/eventos` | GET | `eventos` | Linha do tempo e inscrição nas simulações |
| `/clube-de-leitura` | GET | `clube` | Clube de leitura e inscrição |
| `/artigos` | GET | `artigos` | Lista de artigos; aceita busca com `?q=` |
| `/artigos/<id>` | GET | `artigo` | Página de um artigo |
| `/admin/login` | GET, POST | `entrar` | Login do administrador |
| `/admin/sair` | POST | `sair` | Logout |
| `/admin` | GET | `painel` | Resumo do painel |
| `/admin/membros` | GET | `admin_membros` | Membros por diretoria |
| `/admin/membros/novo` | GET, POST | `novo_membro` | Cadastro de membro |
| `/admin/membros/<id>/editar` | GET, POST | `editar_membro` | Edição de membro |
| `/admin/membros/<id>/excluir` | POST | `excluir_membro` | Exclusão de membro |
| `/admin/artigos` | GET | `admin_artigos` | Lista de artigos |
| `/admin/artigos/novo` | GET, POST | `novo_artigo` | Publicação de artigo |
| `/admin/artigos/<id>/editar` | GET, POST | `editar_artigo` | Edição de artigo |
| `/admin/artigos/<id>/excluir` | POST | `excluir_artigo` | Exclusão de artigo |
| `/admin/eventos` | GET | `admin_eventos` | Lista de eventos |
| `/admin/eventos/novo` | GET, POST | `novo_evento` | Cadastro de evento |
| `/admin/eventos/<id>/editar` | GET, POST | `editar_evento` | Edição de evento |
| `/admin/eventos/<id>/excluir` | POST | `excluir_evento` | Exclusão de evento |
| `/admin/inscricoes` | GET | `admin_inscricoes` | Estado e links das inscrições |
| `/admin/inscricoes/<id>` | POST | `salvar_inscricao` | Abre, fecha ou troca o link de uma inscrição |

Todas as rotas do painel exigem login. As que alteram dados só aceitam POST, seguido de redirect (padrão PRG).

### Segurança

- Senha do administrador guardada com hash (`werkzeug.security`), nunca em texto.
- Proteção CSRF em todos os formulários (`CSRFProtect`).
- Login bloqueado por 15 minutos após 5 tentativas erradas seguidas.
- Sessão com cookie `HttpOnly`, `SameSite=Lax`, `Secure` em produção e validade de 8 horas.
- Uploads aceitam só JPG, PNG e WEBP, até 5 MB, e são salvos com nome aleatório.
- Textos dos artigos são escapados; só o `**negrito**` vira HTML.
- `SECRET_KEY` e senha inicial ficam no `.env`, fora do Git.

### Logging

`logs.py` grava em `logs/app.log` (até 100 KB por arquivo, guardando 3 arquivos antigos). O nível é `DEBUG` em desenvolvimento e `INFO` em produção, e pode ser trocado com `LOG_LEVEL` no `.env`.

| Nível | O que é registrado |
|---|---|
| DEBUG | Cada página acessada e as buscas de artigos |
| INFO | Início da aplicação, carga do banco, logins e cadastros e edições do painel |
| WARNING | Páginas não encontradas (404), senhas erradas, bloqueios de login, exclusões e uploads acima do limite |
| ERROR | Erros internos (500), com o traceback completo |

## Como executar localmente

```bash
python -m venv venv
source venv/bin/activate        # no Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

No `.env`, troque a `SECRET_KEY` por um valor aleatório e defina o usuário e a senha do primeiro administrador:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Depois, rode:

```bash
python app.py
```

e acesse http://127.0.0.1:5000. O banco é criado e populado na primeira execução. Para começar do zero, apague o arquivo `instance/ladi.db` e rode de novo.

## Implantação no PythonAnywhere

1. Em **Consoles → Bash**, baixe o código e crie o ambiente virtual:
   ```bash
   git clone https://github.com/joaopiller/ladi.git
   cd ladi
   mkvirtualenv --python=/usr/bin/python3.13 venv
   pip install -r requirements.txt
   ```
2. Crie o `.env` no servidor (`nano .env`) com `APP_ENV=production`, uma `SECRET_KEY` nova, `ADMIN_USUARIO` e `ADMIN_SENHA`.
3. Na aba **Web**, clique em **Add a new web app**, escolha **Manual configuration** e a mesma versão do Python.
4. Preencha **Source code** e **Working directory** com `/home/<usuario>/ladi` e **Virtualenv** com `/home/<usuario>/.virtualenvs/venv`.
5. Em **Static files**, adicione a URL `/static/` apontando para `/home/<usuario>/ladi/static`.
6. Substitua o conteúdo do **WSGI configuration file** por:
   ```python
   import os
   import sys

   pasta = "/home/<usuario>/ladi"
   if pasta not in sys.path:
       sys.path.insert(0, pasta)

   from dotenv import load_dotenv
   load_dotenv(os.path.join(pasta, ".env"))

   from app import app as application
   ```
7. Clique em **Reload**. Para atualizar depois, rode `git pull` na pasta do projeto e clique em **Reload** de novo.

## Guia do usuário

### Visitantes

- **Menu:** no computador, passe o mouse sobre Quem somos, Eventos ou Clube de leitura para ver as seções de cada página, ou clique no nome para abrir a página. No celular, o menu fica no botão ☰.
- **Membros:** em Quem somos, escolha uma diretoria nas abas. Quando a diretoria tem mais de 4 membros, use as setas para ver os demais.
- **Eventos:** a linha do tempo mostra os eventos do mais antigo para o mais recente. Os cards da página inicial levam direto ao evento na linha do tempo.
- **Artigos:** a página Artigos lista os textos do mais recente para o mais antigo. Use a busca para procurar por título, autor ou trecho do texto, e clique em um card para ler o artigo completo.
- **Inscrições:** no Clube de leitura e na seção Simulações da ONU, o botão **Fazer inscrição** abre o formulário. Quando as inscrições estão fechadas, ele aparece como **Inscrições em breve**.
- **Contato:** o botão **Fale conosco** abre um e-mail para a LADI no Gmail. O rodapé tem o endereço, o e-mail, o Instagram e o LinkedIn.

### Administradores

**Acesso**

1. Clique no botão **Área restrita**, no rodapé de qualquer página (abaixo dos ícones das redes sociais), ou acesse `/admin`.
2. Entre com o usuário e a senha. Depois de 5 tentativas erradas, o login fica bloqueado por 15 minutos.
3. Logado, o menu ganha o item **Painel** e o botão do rodapé passa a se chamar **Painel**. A sessão dura até 8 horas; para sair antes, use o botão **Sair** no topo do painel.

**Painel:** a página inicial mostra o total de membros, artigos e eventos e se as inscrições estão abertas. O menu do painel leva a cada área.

**Membros**

- **Novo membro:** preencha nome, cargo, diretoria e foto. Prefira fotos verticais (3:4), com o rosto centralizado.
- **Posição na aba:** define a ordem dentro da diretoria (1 aparece primeiro). Em branco, o membro vai para o fim.
- **Editar:** permite mudar a diretoria, o cargo ou a foto. Para manter a foto atual, basta não enviar outra.
- **Excluir:** pede confirmação e apaga também a foto enviada.

**Artigos**

- **Novo artigo:** informe título, autor, data de publicação, imagem de capa (de preferência horizontal) e o texto.
- **Parágrafos:** separe os parágrafos com uma linha em branco.
- **Negrito:** selecione um trecho e clique em **Negrito**, ou escreva o trecho entre dois asteriscos, `**assim**`.
- **Editar e excluir:** funcionam como nos membros. O título na lista abre o artigo publicado em outra aba.

**Eventos**

- **Data:** define a posição do evento na linha do tempo, que fica sempre em ordem cronológica.
- **Texto da data:** é opcional e substitui o mês e o ano no card, por exemplo "1º e 2º semestres de 2026".
- **Destacar na página inicial:** coloca o evento no mosaico da home, que mostra os 4 destaques mais recentes.

**Inscrições**

- Ligue ou desligue **Inscrições abertas** e informe o link do formulário (começando com `https://`).
- Com as inscrições abertas, o botão do site leva ao link. Fechadas, o botão aparece como "Inscrições em breve".
- Use **Testar o link atual** para conferir o formulário antes de abrir as inscrições.

**Imagens:** os formatos aceitos são JPG, PNG e WEBP, até 5 MB.
