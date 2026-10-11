import "./style.css";
import { wireInnerNav } from "./partials.js";

wireInnerNav();

const forms = document.querySelectorAll("form[data-contact]");
forms.forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const nombre = String(data.get("nombre") || "").trim();
    alert(
      nombre
        ? `Gracias, ${nombre}. Te responderé lo antes posible.`
        : "Gracias. Te responderé lo antes posible.",
    );
    event.currentTarget.reset();
  });
});
