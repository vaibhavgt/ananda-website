import "./style.css";

const DESKTOP_QUERY = "(min-width: 901px)";

/** Map logical section → desktop / mobile element ids */
const SECTION_MAP = {
  origen: { desktop: "origen", mobile: "m-origen" },
  camino: { desktop: "camino", mobile: "m-camino" },
  experiencias: { desktop: "experiencias", mobile: "m-experiencias" },
  filosofia: { desktop: "filosofia", mobile: "m-filosofia" },
  contacto: { desktop: "contacto", mobile: "m-contacto" },
  yoga: { desktop: "yoga", mobile: "m-experiencias" },
  masajes: { desktop: "masajes", mobile: "m-experiencias" },
  viajes: { desktop: "viajes", mobile: "m-experiencias" },
};

function isDesktop() {
  return window.matchMedia(DESKTOP_QUERY).matches;
}

function resolveSectionId(raw) {
  const key = raw.replace(/^m-/, "");
  const entry = SECTION_MAP[key];
  if (!entry) return raw;
  return isDesktop() ? entry.desktop : entry.mobile;
}

function scrollToSection(rawId, { updateHash = true } = {}) {
  const targetId = resolveSectionId(rawId);
  const el = document.getElementById(targetId);
  if (!el) return false;

  el.scrollIntoView({ behavior: "smooth", block: "start" });
  if (updateHash) {
    const logical = rawId.replace(/^m-/, "");
    history.replaceState(null, "", `#${logical}`);
  }
  return true;
}

function hashFromHref(href) {
  if (!href) return null;
  try {
    const url = new URL(href, window.location.origin);
    if (url.pathname !== "/" && url.pathname !== "/index.html") return null;
    return url.hash ? url.hash.slice(1) : null;
  } catch {
    if (href.startsWith("#")) return href.slice(1);
    return null;
  }
}

document.addEventListener("click", (event) => {
  const link = event.target.closest("a[href]");
  if (!link) return;
  const hash = hashFromHref(link.getAttribute("href"));
  if (!hash || !SECTION_MAP[hash.replace(/^m-/, "")]) return;

  // Same-page hash navigation
  if (
    link.pathname === window.location.pathname ||
    link.getAttribute("href").startsWith("#")
  ) {
    event.preventDefault();
    scrollToSection(hash);
  }
});

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

// Arrive with /#origen from another page, or refresh with hash
function scrollFromLocationHash() {
  const hash = window.location.hash.slice(1);
  if (!hash) return;
  // Wait a tick for layout/fonts
  requestAnimationFrame(() => {
    setTimeout(() => scrollToSection(hash, { updateHash: false }), 50);
  });
}

window.addEventListener("load", scrollFromLocationHash);
window.addEventListener("hashchange", () => {
  const hash = window.location.hash.slice(1);
  if (hash) scrollToSection(hash, { updateHash: false });
});
