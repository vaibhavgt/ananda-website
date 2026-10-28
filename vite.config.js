import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import { resolve } from "node:path";

export default defineConfig({
  plugins: [tailwindcss()],
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, "index.html"),
        experiencias: resolve(__dirname, "experiencias.html"),
        yoga: resolve(__dirname, "yoga.html"),
        masajes: resolve(__dirname, "masajes.html"),
        viajes: resolve(__dirname, "viajes.html"),
        elCamino: resolve(__dirname, "el-camino.html"),
        contacto: resolve(__dirname, "contacto.html"),
        blog: resolve(__dirname, "blog.html"),
        avisoLegal: resolve(__dirname, "aviso-legal.html"),
        privacidad: resolve(__dirname, "politica-privacidad.html"),
        cookies: resolve(__dirname, "politica-cookies.html"),
      },
    },
  },
});
