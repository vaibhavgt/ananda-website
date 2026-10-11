# Ananda Kalapatha

Sitio estático (HTML + Vite + Tailwind) a partir del Figma *Home desktop* / *Home - Mobile*.

## Páginas

| Ruta | Contenido |
| --- | --- |
| `/` | Home (desktop artboard + mobile) |
| `/experiencias.html` | Hub Yoga / Masajes / Viajes |
| `/yoga.html` | Yoga |
| `/masajes.html` | Masajes |
| `/viajes.html` | Viajes y retiros |
| `/blog.html` | Blog (entradas iniciales) |
| `/aviso-legal.html` | Aviso legal |
| `/politica-privacidad.html` | Privacidad |
| `/politica-cookies.html` | Cookies |

## Desarrollo

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
npm run preview
```

## Vercel (desde GitHub)

1. Importar el repo `vaibhavgt/ananda-website`
2. Framework preset: **Vite**
3. Build: `npm run build` · Output: `dist`

## Notas

- Tipografía display en Figma: **Rische** → web: **Cormorant Garamond**
- Imágenes en `public/assets/images/`
- Completar datos legales/fiscales del titular antes de producción
- El formulario de contacto es front-end (alert); conectar Formspree / API cuando tengáis email
