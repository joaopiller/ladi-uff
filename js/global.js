const navbar = document.getElementById("navbar");

function atualizarNavbar() {
  if (window.scrollY > 50) {
    navbar.classList.add("rolou");
  } else {
    navbar.classList.remove("rolou");
  }
}

window.addEventListener("scroll", atualizarNavbar);
atualizarNavbar();

const menu = document.getElementById("menu");
const botaoMenu = document.querySelector(".navbar-toggler");
const linksMenu = document.querySelectorAll(".link-menu");

function fecharMenu() {
  if (menu.classList.contains("show")) {
    botaoMenu.click();
  }
}

for (let i = 0; i < linksMenu.length; i++) {
  linksMenu[i].addEventListener("click", fecharMenu);
}

const linksDropdown = document.querySelectorAll(".dropdown-toggle");

function abrirPaginaDoDropdown() {
  window.location.href = this.getAttribute("href");
}

for (let i = 0; i < linksDropdown.length; i++) {
  linksDropdown[i].addEventListener("click", abrirPaginaDoDropdown);
}

const botaoCopiar = document.getElementById("copiar-email");

function copiarEmail() {
  navigator.clipboard.writeText("ladi.uff@gmail.com");
  botaoCopiar.innerHTML = '<i class="bi bi-check2 me-2"></i>E-mail copiado!';

  setTimeout(function () {
    botaoCopiar.innerHTML = '<i class="bi bi-clipboard me-2"></i>Copiar e-mail';
  }, 2000);
}

botaoCopiar.addEventListener("click", copiarEmail);
