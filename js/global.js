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
