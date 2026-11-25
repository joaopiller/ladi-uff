const seletoresRevelar = ".card-evento, .linha-tempo li, #artigos .card-artigo";

function terminarRevelar() {
  this.classList.remove("revelar", "visivel");
  this.style.transitionDelay = "";
  this.removeEventListener("transitionend", terminarRevelar);
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
  let linhaAnterior = null;
  let posicaoNaLinha = 0;

  for (let i = 0; i < elementos.length; i++) {
    const elemento = elementos[i];
    if (elemento.getBoundingClientRect().top < window.innerHeight) {
      continue;
    }

    const linha = elemento.parentElement.parentElement;
    if (linha === linhaAnterior) {
      posicaoNaLinha++;
    } else {
      posicaoNaLinha = 0;
      linhaAnterior = linha;
    }

    elemento.classList.add("revelar");
    elemento.style.transitionDelay = (posicaoNaLinha % 3) * 90 + "ms";
    observador.observe(elemento);
  }
}

document.addEventListener("DOMContentLoaded", prepararAnimacoes);
