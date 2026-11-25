const grade = document.querySelector(".grade-artigos");
const linksDaLista = document.querySelectorAll(".paginacao a, .filtro-tags a, .limpar-busca");
const reduzirAnimacoes = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function trocarPagina(evento) {
  if (reduzirAnimacoes || evento.ctrlKey || evento.metaKey || evento.shiftKey) {
    return;
  }
  evento.preventDefault();
  const destino = this.href;
  grade.classList.add("saindo");
  setTimeout(function () {
    window.location.href = destino;
  }, 220);
}

for (let i = 0; i < linksDaLista.length; i++) {
  linksDaLista[i].addEventListener("click", trocarPagina);
}

if (window.location.hash === "#lista-artigos" && !reduzirAnimacoes) {
  grade.classList.add("entrando");
}

window.addEventListener("pageshow", function () {
  grade.classList.remove("saindo");
});
