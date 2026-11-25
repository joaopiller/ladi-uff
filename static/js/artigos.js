const grade = document.querySelector(".grade-artigos");
const linksPaginacao = document.querySelectorAll(".paginacao a");
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

for (let i = 0; i < linksPaginacao.length; i++) {
  linksPaginacao[i].addEventListener("click", trocarPagina);
}

if (window.location.hash === "#lista-artigos" && !reduzirAnimacoes) {
  grade.classList.add("entrando");
}

window.addEventListener("pageshow", function () {
  grade.classList.remove("saindo");
});
