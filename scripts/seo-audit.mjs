#!/usr/bin/env node
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const dist = join(root, "dist");
const base = "https://anandakalapatha.com";

const pages = readdirSync(dist).filter((f) => f.endsWith(".html"));
const errors = [];
const warnings = [];
const ok = [];

function absOk(url) {
  return typeof url === "string" && (url.startsWith("http") || url.startsWith("/"));
}

for (const file of pages) {
  const html = readFileSync(join(dist, file), "utf8");
  const label = file;

  const title = html.match(/<title>([^<]+)<\/title>/i)?.[1];
  const desc = html.match(
    /<meta[^>]+name=["']description["'][^>]+content=["']([^"']+)["']/i,
  )?.[1];
  const canonical = html.match(
    /<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)["']/i,
  )?.[1];
  const robots = html.match(
    /<meta[^>]+name=["']robots["'][^>]+content=["']([^"']+)["']/i,
  )?.[1];
  const ogImage = html.match(
    /<meta[^>]+property=["']og:image["'][^>]+content=["']([^"']+)["']/i,
  )?.[1];
  const h1s = [...html.matchAll(/<h1\b[^>]*>([\s\S]*?)<\/h1>/gi)];
  const ldBlocks = [
    ...html.matchAll(
      /<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi,
    ),
  ];

  if (!title) errors.push(`${label}: missing <title>`);
  else if (title.length < 15 || title.length > 70)
    warnings.push(`${label}: title length ${title.length} (aim 15–70)`);
  else ok.push(`${label}: title ok`);

  if (!desc) errors.push(`${label}: missing meta description`);
  else if (desc.length < 50 || desc.length > 170)
    warnings.push(`${label}: description length ${desc.length} (aim 50–170)`);
  else ok.push(`${label}: description ok`);

  if (!canonical) errors.push(`${label}: missing canonical`);
  else if (!canonical.startsWith(base))
    warnings.push(`${label}: canonical not absolute to domain (${canonical})`);
  else ok.push(`${label}: canonical ok`);

  if (!ogImage) warnings.push(`${label}: missing og:image`);
  else if (!ogImage.startsWith("http"))
    warnings.push(`${label}: og:image should be absolute URL`);
  else ok.push(`${label}: og:image ok`);

  if (file === "index.html") {
    // Desktop + mobile each have an h1 — expected; warn if none
    if (h1s.length < 1) errors.push(`${label}: missing h1`);
    else ok.push(`${label}: h1 present (${h1s.length})`);
  } else if (h1s.length !== 1) {
    warnings.push(`${label}: expected 1 h1, found ${h1s.length}`);
  } else ok.push(`${label}: single h1`);

  if (!ldBlocks.length) errors.push(`${label}: missing JSON-LD`);
  else {
    ldBlocks.forEach((block, i) => {
      try {
        const data = JSON.parse(block[1]);
        const types = [];
        const walk = (node) => {
          if (!node || typeof node !== "object") return;
          if (Array.isArray(node)) return node.forEach(walk);
          if (node["@type"]) types.push(node["@type"]);
          if (node["@graph"]) walk(node["@graph"]);
        };
        walk(data);
        if (!types.length) errors.push(`${label}: JSON-LD #${i + 1} has no @type`);
        else ok.push(`${label}: JSON-LD #${i + 1} types=${types.flat().join(",")}`);
      } catch (e) {
        errors.push(`${label}: JSON-LD #${i + 1} invalid JSON (${e.message})`);
      }
    });
  }

  // Internal links exist in dist
  for (const m of html.matchAll(/href=["'](\/[^"'#]+)["']/g)) {
    const href = m[1].split("?")[0];
    if (href.startsWith("/assets/")) {
      if (!existsSync(join(dist, href.slice(1))))
        errors.push(`${label}: missing asset ${href}`);
    } else if (href.endsWith(".html") || href === "/") {
      const target =
        href === "/" ? "index.html" : href.replace(/^\//, "");
      if (!existsSync(join(dist, target)))
        errors.push(`${label}: broken link ${href}`);
    }
  }

  if (file.startsWith("politica") || file.startsWith("aviso")) {
    if (robots && /noindex/i.test(robots))
      warnings.push(`${label}: noindex set (ok for legal drafts)`);
  }
}

console.log("\n=== Ananda SEO audit ===\n");
ok.forEach((l) => console.log("OK   ", l));
warnings.forEach((l) => console.log("WARN ", l));
errors.forEach((l) => console.log("ERR  ", l));
console.log(
  `\nSummary: ${ok.length} ok, ${warnings.length} warnings, ${errors.length} errors\n`,
);
process.exit(errors.length ? 1 : 0);
