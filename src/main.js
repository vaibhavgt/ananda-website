import "./style.css";

const FORMSPREE_ENDPOINT = "https://formspree.io/f/xqppqnyg";

const SECTION_IDS = {
  origen: "origen",
  camino: "camino",
  experiencias: "experiencias",
  filosofia: "filosofia",
  contacto: "contacto",
  yoga: "experiencias",
  masajes: "experiencias",
  viajes: "experiencias",
};

function resolveSectionId(key) {
  if (typeof window === "undefined") return SECTION_IDS[key] || key;
  const mobile = window.matchMedia("(max-width: 900px)").matches;
  if (mobile) {
    const map = {
      origen: "m-origen",
      camino: "m-camino",
      experiencias: "m-experiencias",
      filosofia: "m-filosofia",
      contacto: "m-contacto",
      yoga: "m-experiencias",
      masajes: "m-experiencias",
      viajes: "m-experiencias",
    };
    if (map[key]) return map[key];
    if (key.startsWith("m-")) return key;
  }
  return SECTION_IDS[key] || key;
}

function logicalKey(raw) {
  return String(raw || "")
    .replace(/^#/, "")
    .replace(/^m-/, "");
}

function scrollToSection(rawId, { updateHash = true } = {}) {
  const key = logicalKey(rawId);
  const id = resolveSectionId(key);
  const el = document.getElementById(id);
  if (!el) return false;

  const reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)",
  ).matches;
  el.scrollIntoView({
    behavior: reduceMotion ? "auto" : "smooth",
    block: "start",
  });

  if (updateHash) {
    history.replaceState(null, "", `#${key}`);
  }
  return true;
}

function hashFromHref(href) {
  if (!href) return null;
  try {
    const url = new URL(href, window.location.href);
    const path = url.pathname.replace(/\/$/, "") || "/";
    if (path !== "/" && path !== "/index.html") return null;
    return url.hash ? logicalKey(url.hash) : null;
  } catch {
    return href.startsWith("#") ? logicalKey(href) : null;
  }
}

document.addEventListener("click", (event) => {
  const link = event.target.closest("a[href]");
  if (!link) return;

  const hrefAttr = link.getAttribute("href") || "";
  const hash = hashFromHref(hrefAttr);
  if (!hash || !(hash in SECTION_IDS || document.getElementById(hash))) return;

  const sameDocument =
    hrefAttr.startsWith("#") ||
    link.pathname === window.location.pathname ||
    ((link.pathname === "/" || link.pathname === "/index.html") &&
      (window.location.pathname === "/" ||
        window.location.pathname === "/index.html"));

  if (!sameDocument) return;

  event.preventDefault();
  scrollToSection(hash);
});

async function handleSubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const submitBtn = form.querySelector('[type="submit"]');
  const data = new FormData(form);
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
    form.reset();
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
}

document.querySelectorAll("form[data-contact]").forEach((form) => {
  form.addEventListener("submit", handleSubmit);
});

const menuBtn = document.querySelector("#menu-toggle");
const menuPanel = document.querySelector("#mobile-menu");
menuBtn?.addEventListener("click", () => {
  const open = menuPanel?.classList.toggle("is-open") === true;
  menuBtn.setAttribute("aria-expanded", String(open));
});

menuPanel?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    menuPanel.classList.remove("is-open");
    menuBtn?.setAttribute("aria-expanded", "false");
  });
});

function scrollFromLocationHash() {
  const hash = logicalKey(window.location.hash);
  if (!hash) return;
  requestAnimationFrame(() => scrollToSection(hash, { updateHash: false }));
}

window.addEventListener("hashchange", scrollFromLocationHash);
window.addEventListener("load", scrollFromLocationHash);
