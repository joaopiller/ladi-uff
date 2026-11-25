const seletoresRevelar = [
  ".secao .titulo-secao", ".secao .linha-titulo", ".foto-quem-somos", ".card-evento",
  ".livro", ".card-professor", ".card-missao", ".card-tripe", ".membro", ".linha-tempo li",
  ".caixa-inscricao", ".chamada", ".card-artigo", ".card-passo", ".livro-lido",
  ".perguntas", ".estado-vazio", ".artigo-texto p"
].join(", ");

function terminarRevelar() {
  this.classList.remove("revelar", "visivel");
  this.style.transitionDelay = "";
  this.removeEventListener("transitionend", terminarRevelar);
}

function atrasoNaLinha(elemento) {
  const coluna = elemento.closest(".row > *");
  if (!coluna) {
    return 0;
  }
  const posicao = Array.prototype.indexOf.call(coluna.parentElement.children, coluna);
  return (posicao % 4) * 90;
}

function prepararAnimacoes() {
  const reduzir = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduzir || !("IntersectionObserver" in window)) {
    return;
  }

  const observador = new IntersectionObserver(function (entradas) {
    for (let i = 0; i < entradas.length; i++) {
      if (entradas[i].isIntersecting) {
        const elemento = entradas[i].target;
        elemento.addEventListener("transitionend", terminarRevelar);
        elemento.classList.add("visivel");
        observador.unobserve(elemento);
      }
    }
  }, { threshold: 0.12 });

  const elementos = document.querySelectorAll(seletoresRevelar);
  for (let i = 0; i < elementos.length; i++) {
    const elemento = elementos[i];
    const posicao = elemento.getBoundingClientRect();
    if (posicao.height === 0 || posicao.top < window.innerHeight || elemento.closest(".entrando")) {
      continue;
    }
    elemento.classList.add("revelar");
    elemento.style.transitionDelay = atrasoNaLinha(elemento) + "ms";
    observador.observe(elemento);
  }
}

document.addEventListener("DOMContentLoaded", prepararAnimacoes);
