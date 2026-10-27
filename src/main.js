import "./style.css";

const DESKTOP_QUERY = "(min-width: 901px)";

/** Figma Y / artboard height (6920) — desktop scroll positions */
const DESKTOP_RATIOS = {
  origen: 1700 / 6920,
  experiencias: 2580 / 6920,
  camino: 3480 / 6920,
  filosofia: 4820 / 6920,
  contacto: 5700 / 6920,
  yoga: 3000 / 6920,
  masajes: 3000 / 6920,
  viajes: 3000 / 6920,
};

/** Figma Y / mobile artboard height (8064 after empty-footer crop) */
const MOBILE_RATIOS = {
  origen: 1743 / 8064,
  experiencias: 2833 / 8064,
  camino: 4089 / 8064,
  filosofia: 5088 / 8064,
  contacto: 6153 / 8064,
  yoga: 3111 / 8064,
  masajes: 3418 / 8064,
  viajes: 3728 / 8064,
};

const MOBILE_IDS = {
  origen: "m-origen",
  camino: "m-camino",
  experiencias: "m-experiencias",
  filosofia: "m-filosofia",
  contacto: "m-contacto",
  yoga: "m-experiencias",
  masajes: "m-experiencias",
  viajes: "m-experiencias",
};

function isDesktop() {
  return window.matchMedia(DESKTOP_QUERY).matches;
}

function logicalKey(raw) {
  return String(raw || "").replace(/^m-/, "").replace(/^#/, "");
}

function syncLayoutVisibility() {
  const artboard = document.querySelector(".artboard");
  const mobile = document.querySelector(".mobile-site");
  const mobileArtboard = document.querySelector(".artboard-mobile");
  const desktop = isDesktop();

  if (artboard) {
    artboard.toggleAttribute("inert", !desktop);
    artboard.setAttribute("aria-hidden", desktop ? "false" : "true");
  }
  if (mobile) {
    mobile.toggleAttribute("inert", desktop);
    mobile.setAttribute("aria-hidden", desktop ? "true" : "false");
  }
  if (mobileArtboard) {
    mobileArtboard.toggleAttribute("inert", desktop);
    mobileArtboard.setAttribute("aria-hidden", desktop ? "true" : "false");
  }
}

function scrollToSection(rawId, { updateHash = true } = {}) {
  const key = logicalKey(rawId);
  if (!key) return false;

  const reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)",
  ).matches;
  const behavior = reduceMotion ? "auto" : "smooth";

  if (isDesktop()) {
    const artboard = document.querySelector(".artboard");
    const ratio = DESKTOP_RATIOS[key];
    if (!artboard || ratio == null) return false;

    const top = Math.max(
      0,
      artboard.offsetTop + artboard.offsetHeight * ratio - 8,
    );
    // Instant positioning — smooth scroll is unreliable on the scaled artboard
    document.documentElement.scrollTop = top;
    document.body.scrollTop = top;
    window.scrollTo(0, top);
  } else {
    const artboard = document.querySelector(".artboard-mobile");
    const ratio = MOBILE_RATIOS[key];
    if (artboard && ratio != null) {
      // Leave room above section titles so letterforms aren't clipped by the viewport edge
      const top = Math.max(
        0,
        artboard.offsetTop + artboard.offsetHeight * ratio - 48,
      );
      document.documentElement.scrollTop = top;
      document.body.scrollTop = top;
      window.scrollTo(0, top);
    } else {
      const id = MOBILE_IDS[key] || key;
      const el = document.getElementById(id);
      if (!el) return false;
      el.scrollIntoView({ behavior, block: "start" });
    }
  }

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
  if (!hash || !(hash in DESKTOP_RATIOS || hash in MOBILE_RATIOS || hash in MOBILE_IDS)) return;

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

const FORMSPREE_ENDPOINT = "https://formspree.io/f/xqppqnyg";

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
      "No se pudo enviar el mensaje. Inténtalo de nuevo o escríbeme a hola@anandakalapatha.com.",
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
  const open = menuPanel?.classList.toggle("hidden") === false;
  menuBtn.setAttribute("aria-expanded", String(open));
});

menuPanel?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    menuPanel.classList.add("hidden");
    menuBtn?.setAttribute("aria-expanded", "false");
  });
});

function scrollFromLocationHash() {
  const hash = logicalKey(window.location.hash);
  if (!hash) return;
  // Wait for fonts/layout so artboard height is final; repeat once after paint
  const run = () => scrollToSection(hash, { updateHash: false });
  requestAnimationFrame(() => {
    run();
    setTimeout(run, 120);
    setTimeout(run, 400);
  });
}

const topnav = document.querySelector("[data-desktop-topnav]");

function syncTopnav() {
  if (!topnav) return;
  if (!isDesktop()) {
    topnav.classList.remove("is-visible");
    return;
  }
  // Show sticky menu once the hero artboard nav scrolls away
  const show = window.scrollY > window.innerHeight * 0.55;
  topnav.classList.toggle("is-visible", show);
}

syncLayoutVisibility();
syncTopnav();
window.addEventListener("resize", () => {
  syncLayoutVisibility();
  syncTopnav();
});
window.addEventListener("scroll", syncTopnav, { passive: true });
window.addEventListener("load", scrollFromLocationHash);
window.addEventListener("hashchange", () => {
  const hash = logicalKey(window.location.hash);
  if (hash) scrollToSection(hash, { updateHash: false });
});

// Expose for debugging / manual QA
window.__anandaScrollTo = scrollToSection;
