const campoTexto = document.getElementById("conteudo");
const botaoNegrito = document.getElementById("botao-negrito");

function aplicarNegrito() {
  const inicio = campoTexto.selectionStart;
  const fim = campoTexto.selectionEnd;
  const texto = campoTexto.value;
  let selecionado = texto.substring(inicio, fim);

  if (selecionado === "") {
    selecionado = "texto em negrito";
  }

  campoTexto.value = texto.substring(0, inicio) + "**" + selecionado + "**" + texto.substring(fim);
  campoTexto.focus();
  campoTexto.setSelectionRange(inicio + 2, inicio + 2 + selecionado.length);
}

botaoNegrito.addEventListener("click", aplicarNegrito);
