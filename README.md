# Site da LADI-UFF

Site institucional da **Liga Acadêmica de Direito Internacional da Universidade Federal Fluminense (LADI-UFF)**, desenvolvido como trabalho da disciplina de Introdução ao Desenvolvimento Web.

## Tecnologias

- HTML5
- CSS3
- JavaScript
- [Bootstrap 5](https://getbootstrap.com/) e Bootstrap Icons

## Páginas

- `/` — página inicial
- `/quem-somos/` — história, missão e visão, membros e perguntas frequentes
- `/eventos/` — eventos realizados e simulações da ONU
- `/clube-de-leitura/` — Clube de Leitura da LADI: O Mundo em Páginas

## Como rodar

As páginas usam endereços de pasta (por exemplo, `/quem-somos/`), então o site precisa ser aberto
por um servidor. Na pasta do projeto, rode:

```
python3 -m http.server
```

e acesse `http://localhost:8000`. No GitHub Pages o site funciona sem nenhuma configuração.

## Estrutura de pastas

```
├── index.html              página inicial
├── css/
│   ├── global.css          cores, fontes, menu, rodapé e estilos usados em várias páginas
│   └── home.css            estilos só da página inicial
├── js/
│   └── global.js           menu (usado em todas as páginas)
├── quem-somos/
│   ├── index.html
│   ├── style.css
│   └── script.js           carrossel dos membros
├── eventos/
│   ├── index.html
│   └── style.css
├── clube-de-leitura/
│   ├── index.html
│   └── style.css
└── img/                    imagens de todas as páginas
```
