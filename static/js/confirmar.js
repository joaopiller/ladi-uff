const formsConfirmar = document.querySelectorAll("form[data-confirmar]");

function confirmarEnvio(evento) {
  if (!confirm(this.dataset.confirmar)) {
    evento.preventDefault();
  }
}

for (let i = 0; i < formsConfirmar.length; i++) {
  formsConfirmar[i].addEventListener("submit", confirmarEnvio);
}
