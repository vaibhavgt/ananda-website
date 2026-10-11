import "./style.css";

function handleSubmit(event) {
  event.preventDefault();
  const data = new FormData(event.currentTarget);
  const nombre = String(data.get("nombre") || "").trim();
  alert(
    nombre
      ? `Gracias, ${nombre}. Te responderé lo antes posible.`
      : "Gracias. Te responderé lo antes posible.",
  );
  event.currentTarget.reset();
}

document.querySelectorAll("form[data-contact]").forEach((form) => {
  form.addEventListener("submit", handleSubmit);
});

const menuBtn = document.querySelector("#menu-toggle");
const menuPanel = document.querySelector("#mobile-menu");
menuBtn?.addEventListener("click", () => {
  const open = menuPanel?.classList.toggle("hidden") === false;
  menuBtn.setAttribute("aria-expanded", String(open));
});

menuPanel?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    menuPanel.classList.add("hidden");
    menuBtn?.setAttribute("aria-expanded", "false");
  });
});
