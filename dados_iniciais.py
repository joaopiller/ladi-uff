import os
from datetime import date

from models import Administrador, Artigo, Diretoria, Evento, Inscricao, Membro, db

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

ARTIGOS = [
    {
        "titulo": "50 anos de relações diplomáticas entre Brasil e China",
        "autor": "Equipe LADI-UFF",
        "data_publicacao": date(2026, 11, 3),
        "imagem": "img/eventos/forum-china-brasil.jpg",
        "conteudo": """Em **15 de agosto de 1974**, Brasil e China estabeleceram relações diplomáticas. Cinquenta anos depois, os dois países mantêm uma parceria que vai muito além do comércio e envolve cooperação científica, tecnológica e cultural.

Para marcar a data, a LADI participou do **Fórum China-Brasil**, ao lado dos professores Evandro Menezes de Carvalho e Sérgio Gustavo Mattos Pauseiro. O encontro reuniu estudantes e pesquisadores para discutir o papel dos dois países na ordem internacional.

Entre os temas debatidos estiveram a atuação conjunta no **BRICS**, os desafios do comércio internacional e a importância do diálogo acadêmico para aproximar as duas sociedades.

Para quem estuda Direito Internacional, a relação sino-brasileira é um ótimo exemplo de como tratados, acordos de cooperação e organismos multilaterais se traduzem em políticas concretas.""",
    },
    {
        "titulo": "Refúgio no Brasil: o que diz a Lei 9.474/1997",
        "autor": "Equipe LADI-UFF",
        "data_publicacao": date(2026, 11, 10),
        "imagem": "img/eventos/refugiados.jpg",
        "conteudo": """O Brasil é signatário da **Convenção de 1951 relativa ao Estatuto dos Refugiados** e do Protocolo de 1967. Internamente, o tema é regulado pela **Lei 9.474/1997**, considerada uma das legislações mais avançadas da América Latina sobre o assunto.

A lei reconhece como refugiada a pessoa que deixa seu país por fundado temor de perseguição por motivos de raça, religião, nacionalidade, grupo social ou opinião política. Além disso, inclui quem foge de **grave e generalizada violação de direitos humanos**, uma definição mais ampla, inspirada na Declaração de Cartagena.

A mesma lei criou o **Comitê Nacional para os Refugiados (CONARE)**, órgão responsável por analisar os pedidos de reconhecimento da condição de refugiado no país.

Outro ponto central é o princípio da **não devolução**: a pessoa refugiada não pode ser enviada de volta a um território onde sua vida ou liberdade estejam ameaçadas.

Foi com esse tema em mente que a LADI desenvolveu o **Projeto Refugiados nas Escolas**, em parceria com o programa Pares Cáritas, levando o debate sobre refúgio para além da universidade.""",
    },
    {
        "titulo": "O que é uma simulação da ONU e por que participar",
        "autor": "Equipe LADI-UFF",
        "data_publicacao": date(2026, 11, 17),
        "imagem": "img/eventos/simulacao-onu.jpg",
        "conteudo": """Nas simulações da ONU, cada participante representa a delegação de um país ou organismo internacional e debate temas reais da agenda global, seguindo as regras de procedimento de órgãos como a **Assembleia Geral** e o **Conselho de Segurança**.

Antes do debate, os delegados estudam a posição do país que representam, preparam discursos e redigem propostas de resolução. No dia da simulação, precisam negociar, formar alianças e defender seus argumentos em público.

Por isso, participar de uma simulação é uma forma prática de desenvolver **pesquisa, oratória, negociação e escrita técnica**, habilidades valiosas para qualquer carreira jurídica.

Na LADI, os calouros podem começar pela **MiniMUN**, pensada para quem está entrando na Faculdade de Direito. Já a Simulação de final de ano é organizada em parceria com a Liga de Direito Internacional da UNIRIO e reúne estudantes de diversas instituições.

As inscrições são divulgadas no nosso Instagram, @ladi.uff.""",
    },
]

EVENTOS = [
    {
        "titulo": "Fórum China-Brasil",
        "categoria": "Fórum",
        "data": date(2024, 11, 1),
        "imagem": "img/eventos/forum-china-brasil.jpg",
        "descricao": "A LADI teve a oportunidade de celebrar os 50 anos de relações bilaterais entre Brasil e China no Fórum China-Brasil. Foi uma tarde repleta de discussões importantes e inúmeros aprendizados.",
    },
    {
        "titulo": "Projeto Refugiados nas Escolas",
        "categoria": "Extensão",
        "data": date(2025, 8, 1),
        "imagem": "img/eventos/refugiados-feira.jpg",
        "destaque": True,
        "descricao": "Em parceria com o programa Pares Cáritas, a Faculdade de Direito recebeu uma palestra da empreendedora e refugiada Rama e uma feira cultural com artesanato e culinária típica dos países de origem dos participantes.",
    },
    {
        "titulo": "Curso de Oratória",
        "categoria": "Curso",
        "data": date(2025, 9, 1),
        "imagem": "img/eventos/oratoria.jpg",
        "destaque": True,
        "descricao": "Integrantes da LADI participaram de um curso com a fonoaudióloga Jane Celeste Guberfain, professora da UNIRIO, trabalhando voz, dicção e argumentação para simulações e competições de arbitragem.",
    },
    {
        "titulo": "Feira das Ligas",
        "categoria": "Extensão",
        "data": date(2025, 9, 15),
        "imagem": "img/eventos/feira-das-ligas.jpg",
        "descricao": "Na Semana Jurídica, a LADI montou seu estande na feira organizada pelo CAEV e apresentou aos estudantes seus projetos, grupos de estudo e processos seletivos.",
    },
    {
        "titulo": "Simulação da ONU: A Questão Palestina",
        "categoria": "Simulação",
        "data": date(2025, 11, 1),
        "imagem": "img/eventos/simulacao-onu.jpg",
        "destaque": True,
        "descricao": "Em conjunto com a Liga de Direito Internacional da UNIRIO, a LADI organizou uma simulação da Assembleia Geral da ONU que reuniu estudantes de diversas instituições.",
    },
    {
        "titulo": "Visitas aos consulados",
        "categoria": "Visitas",
        "data": date(2026, 2, 1),
        "periodo": "2026",
        "imagem": "img/eventos/consulado-colombia.jpg",
        "descricao": "Membros da LADI visitaram o Consulado da Colômbia e o Consulado do Reino dos Países Baixos para conhecer de perto a prática diplomática e consular.",
    },
    {
        "titulo": "MiniMUN 2026",
        "categoria": "Simulação",
        "data": date(2026, 5, 1),
        "periodo": "1º e 2º semestres de 2026",
        "imagem": "img/eventos/minimun.jpg",
        "destaque": True,
        "descricao": "A MiniMUN é um projeto inédito na Faculdade de Direito da UFF que busca aproximar os estudantes ingressantes dos debates do Direito Internacional. Em 2026, foram realizadas duas edições: uma no primeiro e outra no segundo semestre.",
    },
]

INSCRICOES = [
    {"chave": "clube", "nome": "Clube de leitura", "aberta": True,
     "link": "https://forms.gle/Qduk1hexQ9m3KnxZ8"},
    {"chave": "simulacoes", "nome": "Simulações da ONU", "aberta": False, "link": None},
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
    for artigo in ARTIGOS:
        db.session.add(Artigo(**artigo))
    for evento in EVENTOS:
        db.session.add(Evento(**evento))
    for inscricao in INSCRICOES:
        db.session.add(Inscricao(**inscricao))
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
