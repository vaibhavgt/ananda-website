import "./style.css";
import { wireInnerNav } from "./partials.js";

wireInnerNav();

const FORMSPREE_ENDPOINT = "https://formspree.io/f/xqppqnyg";

document.querySelectorAll("form[data-contact]").forEach((form) => {
  form.action ||= FORMSPREE_ENDPOINT;
  form.method = "POST";
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const current = event.currentTarget;
    const submitBtn = current.querySelector('[type="submit"]');
    const data = new FormData(current);
    const nombre = String(data.get("nombre") || "").trim();

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.setAttribute("aria-busy", "true");
    }

    try {
      const res = await fetch(FORMSPREE_ENDPOINT, {
        method: "POST",
        body: data,
        headers: { Accept: "application/json" },
      });
      if (!res.ok) throw new Error(`Formspree ${res.status}`);
      current.reset();
      alert(
        nombre
          ? `Gracias, ${nombre}. Te responderé lo antes posible.`
          : "Gracias. Te responderé lo antes posible.",
      );
    } catch {
      alert(
        "No se pudo enviar el mensaje. Inténtalo de nuevo o escríbeme a info@anandakalapatha.com.",
      );
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.removeAttribute("aria-busy");
      }
    }
  });
});
