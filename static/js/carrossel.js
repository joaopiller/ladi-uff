const carrosseis = document.querySelectorAll(".carrossel-membros");
const membrosVisiveis = 4;

function iniciarCarrossel(carrossel) {
  const linha = carrossel.querySelector(".linha-rolagem");
  const setaAnterior = carrossel.querySelector(".seta-anterior");
  const setaProxima = carrossel.querySelector(".seta-proxima");
  let posicao = 0;

  function moverCarrossel() {
    const largura = linha.children[0].offsetWidth;
    const totalMembros = linha.children.length;
    if (largura === 0) {
      return;
    }
    if (window.innerWidth < 768 || posicao < 0) {
      posicao = 0;
    }
    if (posicao > totalMembros - membrosVisiveis) {
      posicao = totalMembros - membrosVisiveis;
    }
    linha.style.transform = "translateX(-" + posicao * largura + "px)";
    setaAnterior.disabled = posicao === 0;
    setaProxima.disabled = posicao >= totalMembros - membrosVisiveis;
  }

  function voltarMembro() {
    posicao = posicao - 1;
    moverCarrossel();
  }

  function avancarMembro() {
    posicao = posicao + 1;
    moverCarrossel();
  }

  setaAnterior.addEventListener("click", voltarMembro);
  setaProxima.addEventListener("click", avancarMembro);
  window.addEventListener("resize", moverCarrossel);
}

for (let i = 0; i < carrosseis.length; i++) {
  iniciarCarrossel(carrosseis[i]);
}
