#!/usr/bin/env python3
"""Rebuild yoga / masajes / viajes as real absolute artboards (not raster screenshots)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fs(px: int) -> str:
    return f"clamp({max(10, int(px * 0.55))}px, calc({px}/1512*min(100vw,1512px)), {px}px)"


def abs_s(x, y, w, h, H, extra=""):
    e = (";" + extra) if extra else ""
    return (
        f"left:calc({x}/1512*100%);top:calc({y}/{H}*100%);"
        f"width:calc({w}/1512*100%);height:calc({h}/{H}*100%){e}"
    )


def T(x, y, w, h, H, text, *, size, family="var(--font-body)", weight="400",
      color="var(--color-grey)", extra="", tag="p"):
    style = abs_s(
        x, y, w, h, H,
        f"font-size:{fs(size)};font-family:{family};font-weight:{weight};"
        f"color:{color};margin:0;line-height:1.35;{extra}",
    )
    return f'<{tag} class="abs" style="{style}">{text}</{tag}>'


def media(x, y, w, h, H, src, extra="", z=1):
    style = abs_s(x, y, w, h, H, f"z-index:{z};{extra}")
    return (
        f'<div class="abs media" style="{style}" aria-hidden="true">'
        f'<img src="{src}" alt="" /></div>'
    )


def rect(x, y, w, h, H, bg, z=1):
    style = abs_s(x, y, w, h, H, f"background:{bg};z-index:{z}")
    return f'<div class="abs" style="{style}" aria-hidden="true"></div>'


def cta(x, y, w, h, H, label, href="/contacto.html"):
    style = abs_s(
        x, y, w, h, H,
        "z-index:20;display:flex;align-items:center;justify-content:center",
    )
    return f'<a class="abs hit btn-fill-abs" href="{href}" style="{style}">{label}</a>'


def nav(H, light=True):
    color = "var(--color-beige)" if light else "var(--color-musgo)"
    filt = "filter:brightness(0) invert(1)" if light else ""
    links = []
    for lab, href in [
        ("EL ORIGEN", "/#origen"),
        ("EL CAMINO", "/el-camino.html"),
        ("EXPERIENCIAS", "/experiencias.html"),
        ("CONTACTO", "/contacto.html"),
    ]:
        st = "color:var(--color-amarillo)" if lab == "EXPERIENCIAS" else ""
        links.append(f'<a href="{href}" style="{st}">{lab}</a>')
    nav_html = '<span aria-hidden="true">|</span>'.join(links)
    brand = abs_s(50, 35, 230, 72, H, "z-index:40")
    nav_style = abs_s(
        808, 49, 640, 24, H,
        f"font-size:{fs(16)};letter-spacing:.1em;font-family:var(--font-ui);"
        f"font-weight:500;color:{color};display:flex;justify-content:flex-end;"
        f"gap:.35rem;align-items:center;text-transform:uppercase;"
        f"white-space:nowrap;z-index:40",
    )
    return f"""
  <a class="abs hit brand" href="/" style="{brand}" aria-label="Ananda Kalapatha">
    <img src="/assets/images/logo-green-v2.png" alt="" style="width:calc(72/1512*100%);height:auto;{filt}" />
    <span style="font-size:{fs(14)};letter-spacing:.2em;line-height:1.15;color:{color};font-family:var(--font-ui)">ANANDA<br />KALAPATHA</span>
  </a>
  <nav class="abs hit nav-desk" aria-label="Principal" style="{nav_style}">{nav_html}</nav>
"""


def footer(H, fy):
    return f"""
  <div class="abs footer-bg" style="{abs_s(0, fy, 1512, H - fy, H, 'background:var(--color-musgo);z-index:1')}"></div>
  <div class="abs media" style="{abs_s(1300, fy + 80, 266, 369, H, 'z-index:2;opacity:.85')}" aria-hidden="true"><img src="/assets/images/footer-leaf-v2.png" alt="" style="object-fit:contain" /></div>
  <a class="abs hit brand" href="/" style="{abs_s(125, fy + 120, 400, 82, H, 'z-index:20;display:flex;align-items:center;gap:.65rem')}">
    <img src="/assets/images/logo-white-v2.png" alt="" style="width:calc(85/1512*100%);height:auto" />
    <span style="font-size:{fs(18)};letter-spacing:.14em;line-height:1.1;color:var(--color-beige);font-family:var(--font-ui)">ANANDA<br />KALAPATHA</span>
  </a>
  <p class="abs" style="{abs_s(160, fy + 250, 336, 19, H, f'font-size:{fs(14)};font-family:var(--font-body);color:var(--color-beige);margin:0;opacity:.9')}">Un espacio para volver a ti</p>
  <nav class="abs hit footer-nav-abs" style="{abs_s(634, fy + 80, 200, 220, H, f'display:flex;flex-direction:column;gap:.85rem;font-size:{fs(14)};font-family:var(--font-ui);letter-spacing:.12em;z-index:20')}">
    <a href="/#origen">EL ORIGEN</a><a href="/el-camino.html">EL CAMINO</a><a href="/experiencias.html">EXPERIENCIAS</a><a href="/blog.html">BLOG</a><a href="/contacto.html">CONTACTO</a>
  </nav>
  <p class="abs" style="{abs_s(961, fy + 110, 255, 96, H, f'font-size:{fs(16)};font-family:var(--font-body);color:var(--color-beige);margin:0;line-height:1.4')}">Yoga, terapias y viajes para una vida más consciente</p>
  <div class="abs" style="{abs_s(961, fy + 290, 180, 30, H, 'display:flex;gap:1.1rem;z-index:20')}">
    <a class="hit" href="https://www.instagram.com/ananda_kalapatha/" target="_blank" rel="noopener" aria-label="Instagram"><img src="/assets/images/icon-ig-v2.svg" width="24" height="24" alt="" style="filter:brightness(0) invert(1)" /></a>
    <a class="hit" href="https://wa.me/34640549641" target="_blank" rel="noopener" aria-label="WhatsApp"><img src="/assets/images/icon-wa-v2.svg" width="24" height="24" alt="" style="filter:brightness(0) invert(1)" /></a>
    <a class="hit" href="mailto:info@anandakalapatha.com" aria-label="Email"><img src="/assets/images/icon-mail-v2.svg" width="24" height="24" alt="" style="filter:brightness(0) invert(1)" /></a>
  </div>
  <p class="abs" style="{abs_s(125, fy + 430, 445, 25, H, f'font-size:{fs(13)};font-family:var(--font-body);color:var(--color-beige);margin:0;opacity:.85')}">2026 Ananda Kalapatha. Todos los derechos reservados</p>
  <p class="abs" style="{abs_s(851, fy + 430, 547, 25, H, f'font-size:{fs(13)};font-family:var(--font-body);color:var(--color-beige);margin:0;opacity:.85;text-align:right')}"><a class="hit" href="/aviso-legal.html" style="color:inherit;text-decoration:none">Aviso legal</a> | <a class="hit" href="/politica-privacidad.html" style="color:inherit;text-decoration:none">Política de privacidad</a> | <a class="hit" href="/politica-cookies.html" style="color:inherit;text-decoration:none">Política de cookies</a></p>
"""


def shell(title, desc, canonical, body, art_class, H, content, mobile):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<meta name="theme-color" content="#666F56" />
<link rel="canonical" href="https://anandakalapatha.com/{canonical}" />
<link rel="icon" type="image/png" href="/assets/images/logo-green-v2.png" />
</head>
<body class="{body}">
<a href="#contenido" class="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-[200] focus:bg-beige focus:px-4 focus:py-2 focus:text-musgo">Saltar al contenido</a>
<header class="site-header mobile-chrome is-solid">
  <a href="/" class="site-brand" aria-label="Inicio"><img src="/assets/images/logo-green-v2.png" alt="" class="size-11 object-cover" width="72" height="72" /><span>ANANDA<br />KALAPATHA</span></a>
  <button id="menu-toggle" class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu">MENU</button>
</header>
<nav id="mobile-menu" class="mobile-menu mobile-chrome" aria-label="Móvil">
  <a href="/#origen">EL ORIGEN</a><a href="/el-camino.html">EL CAMINO</a><a href="/experiencias.html">EXPERIENCIAS</a><a href="/blog.html">BLOG</a><a href="/contacto.html">CONTACTO</a>
</nav>
<main class="{art_class}" id="contenido" aria-label="{title.split('—')[0].strip()}" style="aspect-ratio:1512/{H}">
{content}
</main>
{mobile}
<script type="module" src="/src/main.js"></script>
</body>
</html>
"""


def build_yoga():
    H = 9986
    parts = []
    parts.append(media(0, 0, 1512, 778, H, "/assets/images/yoga/hero-full.jpg"))
    parts.append(
        rect(
            0, 0, 1512, 778, H,
            "linear-gradient(90deg,rgba(70,78,58,.55),rgba(70,78,58,.22) 55%,rgba(70,78,58,.05))",
            2,
        )
    )
    parts.append(nav(H, True))
    parts.append(
        T(64, 188, 200, 52, H, "YOGA", size=40, family="var(--font-ui)", weight="500",
          color="var(--color-beige)", extra="letter-spacing:.3em")
    )
    parts.append(
        T(64, 286, 708, 160, H, "La práctica como<br />espacio de escucha.", size=56,
          family="var(--font-display)", color="var(--color-beige)", tag="h1",
          extra="line-height:1.1")
    )
    parts.append(
        T(64, 486, 708, 90, H,
          "Āsana, prāṇāyāma y meditación como distintas puertas para volver al cuerpo, "
          "regular la energía y cultivar una atención más consciente.",
          size=18, weight="500", color="var(--color-beige)")
    )
    parts.append(cta(64, 597, 339, 55, H, "DESCUBRE LAS CLASES", "#asana"))

    parts.append(rect(0, 992, 510, 298, H, "var(--color-musgo)", 1))
    parts.append(
        media(20, 1012, 470, 258, H, "/assets/images/yoga/tex1.png",
              "opacity:.35;mix-blend-mode:soft-light", 2)
    )
    parts.append(rect(491, 992, 530, 298, H, "var(--color-terracota)", 1))
    parts.append(
        media(510, 1012, 493, 258, H, "/assets/images/texture-terracota.png",
              "opacity:.4;mix-blend-mode:soft-light", 2)
    )
    parts.append(rect(1003, 992, 509, 298, H, "var(--color-amarillo)", 1))
    parts.append(
        media(1015, 1012, 476, 258, H, "/assets/images/texture-amarilla.png",
              "opacity:.4;mix-blend-mode:soft-light", 2)
    )
    parts.append(
        T(153, 1099, 204, 52, H, "Āsana", size=40, family="var(--font-display)",
          color="var(--color-beige)", extra="text-align:center")
    )
    parts.append(
        T(114, 1170, 285, 62, H, "Para una postura firme (sthira) y cómoda (sukham)",
          size=15, weight="500", color="var(--color-beige)", extra="text-align:center")
    )
    parts.append(
        T(563, 1099, 321, 52, H, "PRĀṆĀYĀMA", size=32, family="var(--font-display)",
          color="var(--color-beige)", extra="text-align:center")
    )
    parts.append(
        T(606, 1170, 299, 62, H, "Para la expansión (āyāma) de la energía vital (prāṇa)",
          size=15, weight="500", color="var(--color-beige)", extra="text-align:center")
    )
    parts.append(
        T(1132, 1099, 213, 52, H, "DHYĀNA", size=40, family="var(--font-display)",
          color="var(--color-grey)", extra="text-align:center")
    )
    parts.append(
        T(1099, 1170, 311, 62, H,
          "Para el flujo continuo (ekatānatā) de la atención o consciencia",
          size=15, weight="500", color="var(--color-grey)", extra="text-align:center")
    )

    parts.append(
        f'<div id="asana" class="abs scroll-anchor" style="{abs_s(0, 1338, 1, 1, H)}"></div>'
    )
    parts.append(media(0, 1338, 513, 513, H, "/assets/images/yoga/asana-foto.jpg"))
    parts.append(
        T(625, 1351, 408, 31, H, "ĀSANA · DESDE EL CUERPO", size=16,
          family="var(--font-ui)", weight="500", color="var(--color-terracota)",
          extra="letter-spacing:.16em")
    )
    parts.append(rect(625, 1412, 107, 2, H, "var(--color-terracota)", 5))
    parts.append(
        T(625, 1442, 536, 100, H, "Habitar el cuerpo a través de la práctica.", size=36,
          family="var(--font-display)", color="var(--color-grey)", tag="h2")
    )
    parts.append(
        T(626, 1595, 822, 244, H,
          "Āsana es la dimensión corporal de la práctica del yoga. En los textos clásicos "
          "se refiere inicialmente a una postura estable y cómoda para la práctica interior; "
          "con el desarrollo posterior de las tradiciones de Haṭha Yoga, el trabajo corporal "
          "se amplió. En mis clases trabajamos con movimiento, respiración, atención y "
          "permanencia, adaptando la práctica a cada persona.",
          size=17, weight="500")
    )

    parts.append(
        T(66, 1977, 424, 50, H, "Estilos de práctica", size=36,
          family="var(--font-display)", color="var(--color-grey)", tag="h2")
    )
    parts.append(
        T(693, 1918, 706, 31, H, "DIFERENTES FORMAS DE EXPLORAR EL CUERPO", size=14,
          family="var(--font-ui)", weight="500", color="var(--color-terracota)",
          extra="letter-spacing:.12em;text-align:right")
    )

    for y, num, title in [
        (2073, "01", "HATHA YOGA"),
        (2141, "02", "ASHTANGA VINYASA"),
        (2209, "03", "YOGA RESTAURATIVO"),
    ]:
        parts.append(
            T(64, y, 35, 30, H, num, size=18, family="var(--font-ui)", weight="500",
              color="var(--color-musgo)")
        )
        parts.append(
            T(125, y, 306, 31, H, title, size=16, family="var(--font-ui)", weight="500",
              color="var(--color-grey)", extra="letter-spacing:.08em")
        )
        parts.append(rect(64, y + 48, 436, 1, H, "rgba(102,111,86,.3)", 5))

    styles = [
        (2073, "01", "HATHA YOGA",
         "El Hatha Yoga nos permite permanecer más tiempo en las posturas y observar "
         "alineación, respiración y sensaciones. Una práctica para desarrollar fuerza, "
         "movilidad y presencia sin prisa.",
         "/assets/images/yoga/img3.jpg"),
        (2350, "02", "ASHTANGA VINYASA",
         "Ashtanga Vinyasa enlaza movimiento y respiración de forma continua. La práctica "
         "se construye progresivamente según experiencia y conciencia corporal.",
         "/assets/images/yoga/img4.jpg"),
        (2722, "03", "YOGA RESTAURATIVO",
         "Posturas cómodas mantenidas con soportes para soltar esfuerzo, bajar el ritmo "
         "y permanecer en una escucha más profunda.",
         "/assets/images/yoga/img5.jpg"),
    ]
    for cy, num, title, body, img in styles:
        parts.append(rect(586, cy, 823, 340, H, "var(--color-beige)", 3))
        parts.append(
            f'<div class="abs" style="{abs_s(586, cy, 823, 340, H, "border:1px solid rgba(102,111,86,.18);z-index:3")}" aria-hidden="true"></div>'
        )
        parts.append(
            T(632, cy + 34, 35, 30, H, num, size=18, family="var(--font-ui)",
              color="var(--color-musgo)")
        )
        parts.append(
            T(693, cy + 34, 400, 31, H, title, size=16, family="var(--font-ui)",
              weight="500", color="var(--color-grey)", extra="letter-spacing:.1em")
        )
        parts.append(media(632, cy + 96, 148, 159, H, img, z=4))
        parts.append(T(805, cy + 101, 563, 150, H, body, size=15, weight="500"))
        parts.append(
            T(843, cy + 272, 229, 26, H, "ONLINE · PRIVADO", size=13,
              family="var(--font-ui)", weight="500", color="var(--color-musgo)",
              extra="letter-spacing:.12em")
        )
        parts.append(
            T(1150, cy + 272, 149, 26, H, "PRESENCIAL", size=13, family="var(--font-ui)",
              weight="500", color="var(--color-musgo)", extra="letter-spacing:.12em")
        )

    parts.append(
        T(64, 3105, 244, 31, H, "ĀSANA · ONLINE", size=16, family="var(--font-ui)",
          weight="500", color="var(--color-terracota)", extra="letter-spacing:.16em")
    )
    parts.append(
        T(64, 3196, 500, 100, H, "Una práctica construida contigo", size=36,
          family="var(--font-display)", color="var(--color-grey)", tag="h2")
    )
    parts.append(
        T(64, 3326, 1384, 60, H,
          "Las sesiones de Āsana online son privadas y se adaptan a tu experiencia, "
          "tu cuerpo y el momento en el que te encuentres.",
          size=17, weight="500")
    )

    for ox, oy, ow, oh, title, sub, body, img, btn in [
        (0, 3438, 480, 412, "SESIÓN INDIVIDUAL", "1 CLASE · 75 min",
         "Para conocer la práctica, trabajar algo concreto o recibir orientación personalizada.",
         "/assets/images/yoga/img3.jpg", "RESERVA TU CLASE"),
        (501, 3416, 509, 462, "PRÁCTICA SEMANAL", "4 CLASES · 1 vez por semana",
         "Para establecer continuidad y una práctica sostenible.",
         "/assets/images/yoga/img4.jpg", "EMPEZAR ESTE PROCESO"),
        (1032, 3438, 476, 412, "PRÁCTICA INTENSIVA", "8 CLASES · 2 veces por semana",
         "Para profundizar con mayor regularidad y acompañamiento.",
         "/assets/images/yoga/img5.jpg", "EMPEZAR ESTE PROCESO"),
    ]:
        parts.append(media(ox, oy, ow, oh, H, img, z=1))
        parts.append(rect(ox, oy, ow, oh, H, "rgba(70,78,58,.72)", 2))
        parts.append(
            T(ox + 40, oy + 56, ow - 80, 35, H, title, size=16, family="var(--font-ui)",
              weight="500", color="var(--color-beige)",
              extra="letter-spacing:.1em;text-align:center")
        )
        parts.append(
            T(ox + 40, oy + 110, ow - 80, 35, H, sub, size=15, family="var(--font-ui)",
              color="var(--color-amarillo)", extra="text-align:center")
        )
        parts.append(
            T(ox + 40, oy + 170, ow - 80, 120, H, body, size=14, weight="500",
              color="var(--color-beige)", extra="text-align:center")
        )
        parts.append(cta(ox + (ow - 240) // 2, oy + oh - 80, 240, 48, H, btn))

    parts.append(media(0, 4002, 540, 700, H, "/assets/images/yoga/img6.jpg"))
    parts.append(
        T(587, 4002, 342, 31, H, "ĀSANA · PRESENCIAL", size=16, family="var(--font-ui)",
          weight="500", color="var(--color-terracota)", extra="letter-spacing:.16em")
    )
    parts.append(
        T(587, 4077, 494, 100, H, "Practicar juntas, allá dónde estemos", size=36,
          family="var(--font-display)", color="var(--color-grey)", tag="h2")
    )
    parts.append(
        T(587, 4216, 839, 90, H,
          "Prácticas presenciales de Āsana en formato privado o grupal, según ubicación, "
          "calendario y colaboraciones.",
          size=17, weight="500")
    )
    parts.append(rect(587, 4434, 426, 353, H, "var(--color-musgo)", 2))
    parts.append(
        T(735, 4475, 176, 36, H, "PRIVADA", size=16, family="var(--font-ui)", weight="500",
          color="var(--color-beige)", extra="letter-spacing:.14em;text-align:center")
    )
    parts.append(
        T(630, 4545, 331, 120, H,
          "Sesiones individuales adaptadas a tu experiencia y a lo que precisas trabajar ahora.",
          size=15, weight="500", color="var(--color-beige)", extra="text-align:center")
    )
    parts.append(rect(1047, 4434, 426, 353, H, "var(--color-terracota)", 2))
    parts.append(
        T(1215, 4478, 176, 36, H, "GRUPAL", size=16, family="var(--font-ui)", weight="500",
          color="var(--color-beige)", extra="letter-spacing:.14em;text-align:center")
    )
    parts.append(
        T(1104, 4545, 331, 120, H,
          "Encuentros en comunidad para practicar y nutrir la experiencia del yoga.",
          size=15, weight="500", color="var(--color-beige)", extra="text-align:center")
    )
    parts.append(cta(587, 4880, 339, 55, H, "RESERVA TU CLASE"))

    parts.append(
        f'<div id="pranayama" class="abs scroll-anchor" style="{abs_s(0, 4932, 1, 1, H)}"></div>'
    )
    parts.append(
        T(64, 4932, 232, 31, H, "02 PRĀṆĀYĀMA", size=16, family="var(--font-ui)",
          weight="500", color="var(--color-terracota)", extra="letter-spacing:.16em")
    )
    parts.append(
        T(64, 4974, 482, 50, H, "Del cuerpo a la respiración", size=36,
          family="var(--font-display)", color="var(--color-grey)", tag="h2")
    )
    parts.append(media(25, 5116, 508, 400, H, "/assets/images/yoga/img3.jpg"))
    parts.append(
        T(587, 5116, 573, 31, H, "PRĀṆĀYĀMA · DESDE LA RESPIRACIÓN", size=15,
          family="var(--font-ui)", weight="500", color="var(--color-terracota)",
          extra="letter-spacing:.14em")
    )
    parts.append(
        T(587, 5207, 519, 100, H, "Aprender a respirar con atención.", size=36,
          family="var(--font-display)", color="var(--color-grey)", tag="h3")
    )
    parts.append(
        T(588, 5360, 822, 244, H,
          "Prāṇāyāma es la disciplina dedicada a la observación y regulación de la "
          "respiración. Significa expandir (āyāma) la energía vital (prāṇa). La práctica "
          "se construye progresivamente: observar, incorporar técnicas clásicas y, con "
          "el tiempo, ratios y retenciones.",
          size=16, weight="500")
    )

    for num, title, sub, x in [
        ("01", "FUNDAMENTOS", "Respirar, observar, preparar", 64),
        ("02", "TÉCNICAS", "Aprender y practicar progresivamente", 510),
        ("03", "RATIOS E INTEGRACIÓN", "Profundizar y construir práctica", 1003),
    ]:
        parts.append(
            T(x, 5719, 140, 86, H, num, size=64, family="var(--font-display)",
              color="var(--color-oliva)")
        )
        parts.append(
            T(x, 5833, 364, 31, H, title, size=15, family="var(--font-ui)", weight="500",
              color="var(--color-grey)", extra="letter-spacing:.1em")
        )
        parts.append(T(x, 5885, 380, 30, H, sub, size=14, weight="500"))

    parts.append(
        T(64, 6015, 327, 31, H, "PRĀṆĀYĀMA · ONLINE", size=16, family="var(--font-ui)",
          weight="500", color="var(--color-terracota)", extra="letter-spacing:.16em")
    )
    parts.append(
        T(64, 6106, 644, 100, H, "Una práctica que se construye con constancia", size=36,
          family="var(--font-display)", color="var(--color-grey)", tag="h3")
    )
    for ox, title, sub, body, img, btn in [
        (82, "CICLO DE INICIACIÓN", "4 SEMANAS · 2 clases/semana",
         "Fundamentos de la respiración y construcción de una práctica personal.",
         "/assets/images/yoga/img2.jpg", "COMENZAR EL CICLO"),
        (777, "MODALIDAD MENSUAL", "2 clases por semana",
         "Para quienes ya conocen las bases y quieren profundizar en ratios y retenciones.",
         "/assets/images/yoga/img5.jpg", "CONTINUAR LA PRÁCTICA"),
    ]:
        parts.append(media(ox, 6258, 654, 447, H, img, z=1))
        parts.append(rect(ox, 6258, 654, 447, H, "rgba(70,78,58,.75)", 2))
        parts.append(
            T(ox + 90, 6300, 470, 31, H, title, size=16, family="var(--font-ui)",
              weight="500", color="var(--color-beige)",
              extra="text-align:center;letter-spacing:.1em")
        )
        parts.append(
            T(ox + 90, 6345, 470, 31, H, sub, size=14, family="var(--font-ui)",
              color="var(--color-amarillo)", extra="text-align:center")
        )
        parts.append(
            T(ox + 70, 6409, 510, 120, H, body, size=14, weight="500",
              color="var(--color-beige)", extra="text-align:center")
        )
        parts.append(cta(ox + 160, 6600, 300, 48, H, btn))

    parts.append(media(0, 6801, 700, 469, H, "/assets/images/yoga/img4.jpg"))
    parts.append(
        T(868, 6801, 398, 31, H, "PRĀṆĀYĀMA · PRESENCIAL", size=15,
          family="var(--font-ui)", weight="500", color="var(--color-terracota)",
          extra="letter-spacing:.14em")
    )
    parts.append(
        T(868, 6892, 644, 100, H, "Prácticas y talleres en presencia", size=36,
          family="var(--font-display)", color="var(--color-grey)", tag="h3")
    )
    parts.append(
        T(868, 7034, 542, 90, H,
          "Encuentros para explorar la respiración de forma guiada y en comunidad.",
          size=16, weight="500")
    )
    parts.append(cta(868, 7160, 339, 55, H, "VER DISPONIBILIDAD"))

    parts.append(
        f'<div id="dhyana" class="abs scroll-anchor" style="{abs_s(0, 7300, 1, 1, H)}"></div>'
    )
    parts.append(
        T(62, 7300, 200, 31, H, "03 DHYĀNA", size=16, family="var(--font-ui)",
          weight="500", color="var(--color-terracota)", extra="letter-spacing:.16em")
    )
    parts.append(
        T(62, 7339, 541, 50, H, "De la respiración a la quietud", size=36,
          family="var(--font-display)", color="var(--color-grey)", tag="h2")
    )
    parts.append(media(25, 7453, 508, 564, H, "/assets/images/yoga/img5.jpg"))
    parts.append(
        T(588, 7498, 458, 31, H, "DHYĀNA · DESDE LA ATENCIÓN", size=15,
          family="var(--font-ui)", weight="500", color="var(--color-terracota)",
          extra="letter-spacing:.14em")
    )
    parts.append(
        T(588, 7589, 519, 100, H, "Aprender a observar", size=36,
          family="var(--font-display)", color="var(--color-grey)", tag="h3")
    )
    parts.append(
        T(588, 7735, 822, 282, H,
          "Dhyāna es un entrenamiento de la atención. Mi acercamiento está influido por "
          "Vipassanā e integra técnicas con respiración, mirada o mantra como objetos "
          "de atención.",
          size=16, weight="500")
    )
    parts.append(
        T(64, 8101, 263, 31, H, "DHYĀNA · ONLINE", size=16, family="var(--font-ui)",
          weight="500", color="var(--color-terracota)", extra="letter-spacing:.16em")
    )
    parts.append(
        T(62, 8210, 648, 50, H, "Construir la práctica juntas", size=36,
          family="var(--font-display)", color="var(--color-grey)", tag="h3")
    )
    parts.append(
        T(62, 8292, 1387, 90, H,
          "Encuentros en directo para aprender técnicas, resolver dudas y sostener el "
          "hábito entre sesiones.",
          size=16, weight="500")
    )

    for ox, title, sub, body, bg, btn in [
        (66, "PRÁCTICA GRUPAL", "2 CLASES/SEMANA · 30/45 min",
         "Meditar en grupo, sostener el hábito y profundizar progresivamente.",
         "var(--color-musgo)", "UNIRME A LA PRÁCTICA"),
        (828, "PRÁCTICA PRIVADA", "2 CLASES/SEMANA · 30/45 min",
         "Acompañamiento adaptado a tu experiencia, con propuesta entre encuentros.",
         "var(--color-terracota)", "COMENZAR PROCESO"),
    ]:
        parts.append(rect(ox, 8432, 623, 458, H, bg, 1))
        parts.append(
            media(ox, 8438, 623, 452, H, "/assets/images/yoga/tex2.png",
                  "opacity:.3;mix-blend-mode:soft-light", 2)
        )
        parts.append(
            T(ox + 100, 8483, 420, 36, H, title, size=18, family="var(--font-ui)",
              weight="500", color="var(--color-beige)",
              extra="text-align:center;letter-spacing:.12em")
        )
        parts.append(
            T(ox + 90, 8547, 442, 31, H, sub, size=14, family="var(--font-ui)",
              color="var(--color-amarillo)", extra="text-align:center")
        )
        parts.append(
            T(ox + 90, 8607, 450, 150, H, body, size=14, weight="500",
              color="var(--color-beige)", extra="text-align:center")
        )
        parts.append(cta(ox + 170, 8780, 280, 48, H, btn))

    parts.append(footer(H, 8963))

    mobile = """
<main class="mobile-yoga" aria-label="Yoga móvil">
  <section class="mh-section mh-hero" style="position:relative;min-height:72vh;display:grid;align-items:end;color:var(--color-beige)">
    <img src="/assets/images/yoga/hero-full.jpg" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0" />
    <div style="position:absolute;inset:0;background:rgba(70,78,58,.75);z-index:1"></div>
    <div style="position:relative;z-index:2;padding:2rem 1.25rem 3rem">
      <p class="eyebrow" style="color:var(--color-amarillo)">YOGA</p>
      <h1 class="display" style="color:var(--color-beige)">La práctica como espacio de escucha.</h1>
      <a href="/contacto.html" class="btn-fill" style="margin-top:1.25rem">RESERVA TU CLASE</a>
    </div>
  </section>
  <section class="mh-section">
    <p class="eyebrow" style="color:var(--color-terracota)">ĀSANA · PRĀṆĀYĀMA · DHYĀNA</p>
    <h2 class="display text-grey">Tres puertas hacia la práctica</h2>
    <img class="mh-img" src="/assets/images/yoga/asana-foto.jpg" alt="" />
    <p class="body-copy">Hatha, Ashtanga y restaurativo · online y presencial.</p>
    <a href="/contacto.html" class="btn-fill" style="margin-top:1.25rem">HABLEMOS</a>
  </section>
  <footer class="mh-footer">
    <p class="font-ui tracking-[0.16em]">ANANDA KALAPATHA</p>
    <nav class="mh-footer-nav"><a href="/experiencias.html">EXPERIENCIAS</a><a href="/contacto.html">CONTACTO</a></nav>
  </footer>
</main>
"""
    (ROOT / "yoga.html").write_text(
        shell(
            "Yoga — Ananda Kalapatha",
            "Āsana, prāṇāyāma y meditación.",
            "yoga.html",
            "page-yoga",
            "artboard-yoga",
            H,
            "\n".join(parts),
            mobile,
        )
    )
    print("yoga", (ROOT / "yoga.html").stat().st_size)


def build_masajes():
    H = 6146
    p = []
    p.append(media(0, 0, 1512, 900, H, "/assets/images/masaje/hero-full.jpg"))
    p.append(
        rect(
            0, 0, 1512, 900, H,
            "linear-gradient(90deg,rgba(109,75,64,.78),rgba(109,75,64,.4) 55%,rgba(109,75,64,.15))",
            2,
        )
    )
    p.append(nav(H, True))
    p.append(
        T(64, 220, 885, 52, H, "MASAJES Y CUIDADO CORPORAL", size=32,
          family="var(--font-ui)", weight="500", color="var(--color-beige)",
          extra="letter-spacing:.2em")
    )
    p.append(
        T(64, 313, 832, 160, H, "Cuida tu cuerpo antes<br />de que te pida parar.",
          size=48, family="var(--font-display)", color="var(--color-beige)", tag="h1",
          extra="line-height:1.1")
    )
    p.append(
        T(64, 521, 628, 90, H,
          "Masajes con aceite templado, presiones y estiramientos adaptados a ti. "
          "Un cuidado a través del tacto para aflojar tensiones y descansar.",
          size=17, weight="500", color="var(--color-beige)")
    )
    p.append(cta(64, 652, 339, 55, H, "DESCUBRE LAS SESIONES", "#sesiones"))

    p.append(
        T(64, 1197, 444, 31, H, "LA IMPORTANCIA DEL MASAJE", size=15,
          family="var(--font-ui)", weight="500", color="var(--color-terracota)",
          extra="letter-spacing:.16em")
    )
    p.append(
        T(64, 1296, 628, 100, H, "El cuidado también empieza en el tacto", size=36,
          family="var(--font-display)", color="var(--color-grey)", tag="h2")
    )
    p.append(
        T(64, 1434, 801, 337, H,
          "El masaje lleva siglos formando parte del cuidado del cuerpo en tradiciones "
          "como el Āyurveda y la tailandesa. No necesitas sentir dolor para dedicarte "
          "este espacio: un tiempo para descansar, percibir dónde acumulas tensión y "
          "prestar atención a cómo te encuentras. Adapto el ritmo y la intensidad de "
          "cada sesión a ti.",
          size=16, weight="500")
    )
    p.append(media(906, 1117, 542, 814, H, "/assets/images/masaje/intro-foto.jpg"))
    p.append(cta(64, 1809, 339, 55, H, "RESERVA TU SESIÓN"))

    p.append(
        f'<div id="sesiones" class="abs scroll-anchor" style="{abs_s(0, 2043, 1, 1, H)}"></div>'
    )
    p.append(
        T(64, 2043, 206, 31, H, "LAS SESIONES", size=15, family="var(--font-ui)",
          weight="500", color="var(--color-terracota)", extra="letter-spacing:.16em")
    )
    p.append(
        T(64, 2142, 628, 100, H, "Distintas maneras de cuidar tu cuerpo.", size=36,
          family="var(--font-display)", color="var(--color-grey)", tag="h2")
    )

    sessions = [
        (64, "/assets/images/masaje/abhyanga.jpg", "abhyanga", "MASAJE ABHYANGA",
         "Aceite templado y movimientos envolventes. Favorece la relajación.",
         "60 o 90 min",
         "El Abhyanga forma parte del cuidado corporal del Āyurveda. Movimientos "
         "rítmicos sobre todo el cuerpo; adapto la presión a tu sensibilidad."),
        (536, "/assets/images/masaje/thai.jpg", "Tailandés", "MASAJE TRADICIONAL THAI",
         "Presiones y estiramientos asistidos, con ropa cómoda y sin aceites.",
         "120 min",
         "Sobre un futón en el suelo. Combino presiones, movilizaciones y estiramientos; "
         "no necesitas ser flexible."),
        (1008, "/assets/images/masaje/marma.jpg", "Marma", "TERAPIA MARMA",
         "Trabajo sobre puntos vitales del Āyurveda. Relajación y percepción corporal.",
         "60 o 90 min",
         "Contacto y presiones sobre marmas, combinando movimientos envolventes y "
         "aceite templado."),
    ]
    for x, img, label, title, lead, dur, body in sessions:
        p.append(media(x, 2310, 440, 440, H, img))
        p.append(rect(x + 55, 2681, 330, 69, H, "var(--color-beige)", 3))
        p.append(
            T(x + 70, 2689, 300, 52, H, label, size=26, family="var(--font-display)",
              color="var(--color-terracota)", extra="text-align:center")
        )
        p.append(
            T(x + 20, 2783, 400, 31, H, title, size=14, family="var(--font-ui)",
              weight="500", color="var(--color-grey)", extra="letter-spacing:.08em")
        )
        p.append(T(x + 35, 2847, 390, 100, H, lead, size=14, weight="500"))
        p.append(
            T(x + 35, 2980, 390, 30, H, f"Duración {dur}.", size=13,
              family="var(--font-ui)", weight="500", color="var(--color-musgo)")
        )
        p.append(T(x + 35, 3074, 390, 260, H, body, size=13, weight="500"))

    sessions2 = [
        (64, "/assets/images/masaje/pindas.jpg", "pindas", "MASAJE PINDAS HERBALES",
         "Saquitos de hierbas calientes y presiones suaves.", "30 min",
         "Calor y aroma de plantas para una relajación profunda. Disponible según el espacio."),
        (536, "/assets/images/masaje/shirodhara.jpg", "Shirodhara", "SHIRODHARA",
         "Hilo continuo de aceite templado sobre la frente.", "45 o 60 min",
         "Práctica āyurvédica de relajación profunda a través del calor. Disponible "
         "según el espacio."),
        (1008, "/assets/images/masaje/kati.jpg", "Kati Basti", "KATI BASTI",
         "Aceite templado contenido sobre la zona lumbar.", "30 min",
         "Cuidado centrado en la espalda baja con calor localizado."),
    ]
    for x, img, label, title, lead, dur, body in sessions2:
        p.append(media(x, 3478, 440, 440, H, img))
        p.append(rect(x + 40, 3849, 360, 69, H, "var(--color-beige)", 3))
        p.append(
            T(x + 55, 3857, 330, 52, H, label, size=26, family="var(--font-display)",
              color="var(--color-terracota)", extra="text-align:center")
        )
        p.append(
            T(x + 20, 3951, 400, 31, H, title, size=14, family="var(--font-ui)",
              weight="500", color="var(--color-grey)", extra="letter-spacing:.08em")
        )
        p.append(T(x + 35, 4015, 390, 100, H, lead, size=14, weight="500"))
        p.append(
            T(x + 35, 4143, 390, 30, H, f"Duración {dur}.", size=13,
              family="var(--font-ui)", weight="500", color="var(--color-musgo)")
        )
        p.append(T(x + 35, 4240, 390, 260, H, body, size=13, weight="500"))

    p.append(cta(491, 4696, 529, 55, H, "RESERVA TU SESIÓN"))
    p.append(
        media(0, 4834, 1512, 500, H, "/assets/images/masaje/hero-full.jpg",
              "filter:brightness(.45)", 1)
    )
    p.append(
        T(64, 4909, 292, 31, H, "TE AYUDO A ELEGIR", size=15, family="var(--font-ui)",
          weight="500", color="var(--color-amarillo)", extra="letter-spacing:.16em")
    )
    p.append(
        T(64, 4990, 995, 50, H, "¿Qué cuidado necesitas hoy?", size=36,
          family="var(--font-display)", color="var(--color-beige)", tag="h2")
    )
    p.append(
        T(64, 5076, 843, 120, H,
          "No necesitas conocer cada técnica: cuéntame cómo te encuentras y vemos qué "
          "sesión encaja, incluso una experiencia personalizada.",
          size=16, weight="500", color="var(--color-beige)")
    )
    p.append(cta(64, 5222, 463, 55, H, "HABLAR SOBRE LA SESIÓN"))
    p.append(footer(H, 5389))

    mobile = """
<main class="mobile-masaje" aria-label="Masajes móvil">
  <section class="mh-section mh-hero" style="position:relative;min-height:72vh;display:grid;align-items:end;color:var(--color-beige)">
    <img src="/assets/images/masaje/hero-full.jpg" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0" />
    <div style="position:absolute;inset:0;background:rgba(109,75,64,.72);z-index:1"></div>
    <div style="position:relative;z-index:2;padding:2rem 1.25rem 3rem">
      <p class="eyebrow" style="color:var(--color-amarillo)">MASAJES</p>
      <h1 class="display" style="color:var(--color-beige)">Cuida tu cuerpo antes de que te pida parar.</h1>
      <a href="/contacto.html" class="btn-fill" style="margin-top:1.25rem">RESERVA TU SESIÓN</a>
    </div>
  </section>
  <section class="mh-section">
    <p class="eyebrow" style="color:var(--color-terracota)">LAS SESIONES</p>
    <h2 class="display text-grey">Abhyanga, Thai, Marma y más</h2>
    <img class="mh-img" src="/assets/images/masaje/abhyanga.jpg" alt="" />
    <p class="body-copy">También pindas, shirodhara y kati basti según el espacio.</p>
    <a href="/contacto.html" class="btn-fill" style="margin-top:1.25rem">HABLAR SOBRE LA SESIÓN</a>
  </section>
  <footer class="mh-footer">
    <p class="font-ui tracking-[0.16em]">ANANDA KALAPATHA</p>
    <nav class="mh-footer-nav"><a href="/experiencias.html">EXPERIENCIAS</a><a href="/contacto.html">CONTACTO</a></nav>
  </footer>
</main>
"""
    (ROOT / "masajes.html").write_text(
        shell(
            "Masajes — Ananda Kalapatha",
            "Masajes āyurveda y thai adaptados a ti.",
            "masajes.html",
            "page-masaje",
            "artboard-masaje",
            H,
            "\n".join(p),
            mobile,
        )
    )
    print("masajes", (ROOT / "masajes.html").stat().st_size)


def build_viajes():
    H = 4389
    v = []
    v.append(media(0, 0, 1512, 900, H, "/assets/images/viajes/hero-full.jpg"))
    v.append(rect(0, 0, 764, 900, H, "rgba(70,78,58,.72)", 2))
    v.append(nav(H, True))
    v.append(
        T(64, 241, 497, 52, H, "VIAJES Y RETIROS", size=32, family="var(--font-ui)",
          weight="500", color="var(--color-beige)", extra="letter-spacing:.2em")
    )
    v.append(
        T(64, 333, 700, 240, H, "Salir de lo conocido<br />para mirar desde<br />otro lugar.",
          size=48, family="var(--font-display)", color="var(--color-beige)", tag="h1",
          extra="line-height:1.1")
    )
    v.append(
        T(64, 595, 669, 80, H,
          "Experiencias para descubrir nuevos lugares, acercarnos a otras culturas y "
          "crear espacio para vivir el camino con más presencia.",
          size=17, weight="500", color="var(--color-beige)")
    )
    v.append(cta(64, 702, 339, 55, H, "PRÓXIMAS EXPERIENCIAS", "#proxima"))

    v.append(
        T(64, 1045, 357, 31, H, "OTRA FORMA DE VIAJAR", size=15, family="var(--font-ui)",
          weight="500", color="var(--color-terracota)", extra="letter-spacing:.16em")
    )
    v.append(
        T(64, 1144, 496, 100, H, "El viaje también puede ser una pausa", size=36,
          family="var(--font-display)", color="var(--color-grey)", tag="h2")
    )
    v.append(
        T(64, 1282, 744, 274, H,
          "Viajar me ha enseñado a mirar con curiosidad. Los retiros ofrecen tiempo "
          "para detenerme y escucharme. A veces recorreremos lugares; otras, "
          "permaneceremos en un mismo espacio. Siempre habrá yoga, encuentro y lo que "
          "cada persona descubra.",
          size=16, weight="500")
    )
    v.append(media(861, 1045, 651, 759, H, "/assets/images/viajes/intro-foto.jpg"))
    for lab, x in [("DESCUBRIR", 73), ("HABITAR", 374), ("PRÁCTICAR", 638)]:
        v.append(
            T(x, 1724, 166, 31, H, lab, size=15, family="var(--font-ui)", weight="500",
              color="var(--color-musgo)", extra="letter-spacing:.14em")
        )

    v.append(
        f'<div id="proxima" class="abs scroll-anchor" style="{abs_s(0, 1863, 1, 1, H)}"></div>'
    )
    v.append(media(0, 1983, 630, 717, H, "/assets/images/viajes/india-map.jpg"))
    v.append(
        T(626, 1901, 340, 31, H, "PRÓXIMA EXPERIENCIA", size=15, family="var(--font-ui)",
          weight="500", color="var(--color-terracota)", extra="letter-spacing:.16em")
    )
    v.append(
        T(626, 2060, 654, 100, H, "India: Entre el mundo y lo que eres.", size=36,
          family="var(--font-display)", color="var(--color-grey)", tag="h2")
    )
    v.append(rect(626, 2165, 140, 28, H, "var(--color-musgo)", 3))
    v.append(
        T(636, 2168, 130, 22, H, "VIAJE + RETIRO", size=11, family="var(--font-ui)",
          weight="500", color="var(--color-beige)", extra="letter-spacing:.08em")
    )
    v.append(
        T(661, 2198, 500, 28, H, "18 mar – 02 abr 2027 · 16 días · grupo reducido",
          size=15, weight="500")
    )
    v.append(
        T(626, 2251, 822, 397, H,
          "Viaje en grupo pequeño con guía local. Vrindavan, Holi, Benarés y cinco días "
          "de retiro en Rishikesh con maestros locales y traducción al español. Entre el "
          "mundo y lo que eres hay un reflejo: cada encuentro fuera te invita a "
          "reconocerte dentro.",
          size=15, weight="500")
    )
    v.append(cta(626, 2672, 463, 55, H, "DESCUBRE EL VIAJE"))

    v.append(
        media(0, 2840, 1512, 654, H, "/assets/images/viajes/img5.jpg",
              "filter:brightness(.5)", 1)
    )
    v.append(
        T(64, 2986, 995, 50, H, "¿Nos encontramos en otro momento?", size=36,
          family="var(--font-display)", color="var(--color-beige)", tag="h2")
    )
    v.append(
        T(64, 3086, 879, 60, H,
          "Si esta fecha no te encaja, deja tu correo y te escribo cuando haya nuevas "
          "propuestas.",
          size=16, weight="500", color="var(--color-beige)")
    )
    form_style = abs_s(64, 3196, 560, 55, H, "z-index:20;display:flex;gap:.5rem")
    v.append(
        f"""<form class="abs hit" data-contact action="https://formspree.io/f/xqppqnyg" method="POST" style="{form_style}">
  <input type="hidden" name="tema" value="Viajes / próximas experiencias" />
  <input name="email" type="email" required placeholder="Tu correo" autocomplete="email" style="flex:1;border:0;border-bottom:1px solid rgba(245,243,239,.7);background:transparent;color:var(--color-beige);font-size:{fs(16)};padding:.5rem 0;font-family:var(--font-body);outline:none" />
  <button type="submit" class="btn-fill-abs" style="min-width:180px">AVÍSAME</button>
</form>"""
    )
    v.append(footer(H, 3494))

    mobile = """
<main class="mobile-viajes" aria-label="Viajes móvil">
  <section class="mh-section mh-hero" style="position:relative;min-height:72vh;display:grid;align-items:end;color:var(--color-beige)">
    <img src="/assets/images/viajes/hero-full.jpg" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0" />
    <div style="position:absolute;inset:0;background:rgba(70,78,58,.72);z-index:1"></div>
    <div style="position:relative;z-index:2;padding:2rem 1.25rem 3rem">
      <p class="eyebrow" style="color:var(--color-amarillo)">VIAJES Y RETIROS</p>
      <h1 class="display" style="color:var(--color-beige)">Salir de lo conocido para mirar desde otro lugar.</h1>
      <a href="/contacto.html" class="btn-fill" style="margin-top:1.25rem">DESCUBRE EL VIAJE</a>
    </div>
  </section>
  <section class="mh-section">
    <p class="eyebrow" style="color:var(--color-terracota)">PRÓXIMA EXPERIENCIA</p>
    <h2 class="display text-grey">India: Entre el mundo y lo que eres.</h2>
    <p class="body-copy">18 mar – 02 abr 2027 · 16 días · grupo reducido</p>
    <a href="/contacto.html" class="btn-fill" style="margin-top:1.25rem">HABLEMOS</a>
  </section>
  <footer class="mh-footer">
    <p class="font-ui tracking-[0.16em]">ANANDA KALAPATHA</p>
    <nav class="mh-footer-nav"><a href="/experiencias.html">EXPERIENCIAS</a><a href="/contacto.html">CONTACTO</a></nav>
  </footer>
</main>
"""
    (ROOT / "viajes.html").write_text(
        shell(
            "Viajes y retiros — Ananda Kalapatha",
            "Viajes y retiros conscientes.",
            "viajes.html",
            "page-viajes",
            "artboard-viajes",
            H,
            "\n".join(v),
            mobile,
        )
    )
    print("viajes", (ROOT / "viajes.html").stat().st_size)


if __name__ == "__main__":
    build_yoga()
    build_masajes()
    build_viajes()
