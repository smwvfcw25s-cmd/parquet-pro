#!/usr/bin/env python3
"""assemble.py — construye el index.html final, autónomo y offline.
Inserta React + ReactDOM (UMD), CSS propio (sin Tailwind CDN), los datos (SEED)
y la app ya compilada a JS normal (sin Babel en el navegador).
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]

react = (ROOT/"node_modules"/"react"/"umd"/"react.production.min.js").read_text(encoding="utf-8")
react_dom = (ROOT/"node_modules"/"react-dom"/"umd"/"react-dom.production.min.js").read_text(encoding="utf-8")
app_js = (ROOT/"build"/"app.js").read_text(encoding="utf-8")
data = json.loads((ROOT/"public"/"data.json").read_text(encoding="utf-8"))

CSS = """
  html,body,#root{height:100%;margin:0;background:#0C0F16}
  *{box-sizing:border-box}
  .flex{display:flex}.grid{display:grid}
  .items-center{align-items:center}
  .justify-between{justify-content:space-between}
  .justify-center{justify-content:center}
  .mx-auto{margin-left:auto;margin-right:auto}
  .w-full{width:100%}
  .px-4{padding-left:16px;padding-right:16px}
  @media (min-width:640px){ .sm\\:px-6{padding-left:24px;padding-right:24px} }
  @keyframes pq-marquee{from{transform:translateX(0)}to{transform:translateX(-50%)}}
  .pq-ribbon:hover .pq-track{animation-play-state:paused}
  @keyframes pq-pulse{0%,100%{opacity:1}50%{opacity:.35}} .pq-pulse{animation:pq-pulse 1.3s infinite}
  @keyframes pq-spin{to{transform:rotate(360deg)}} .pq-spin{animation:pq-spin .9s linear infinite}
  @media (max-width:560px){ .hide-sm{display:none} }
  *:focus-visible{outline:2px solid #F4A93C;outline-offset:2px;border-radius:6px}
  @media (prefers-reduced-motion:reduce){.pq-track{animation:none!important}}
  .pq-scroll::-webkit-scrollbar{height:6px;width:6px}.pq-scroll::-webkit-scrollbar-thumb{background:#313A4D;border-radius:6px}
  a{color:inherit}
"""

HTML = (
"<!doctype html>\n<html lang=\"es\">\n<head>\n"
"<meta charset=\"utf-8\"/>\n"
"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"/>\n"
"<title>PARQUET PRO \u00b7 baloncesto 25-26 \u2192 26/27</title>\n"
"<link href=\"https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap\" rel=\"stylesheet\"/>\n"
"<style>" + CSS + "</style>\n"
"</head>\n<body>\n<div id=\"root\"></div>\n"
"<script>" + react + "</script>\n"
"<script>" + react_dom + "</script>\n"
"<script>window.SEED = " + json.dumps(data, ensure_ascii=False) + ";</script>\n"
"<script>\n" + app_js + "\n</script>\n"
"</body>\n</html>\n"
)

(ROOT/"index.html").write_text(HTML, encoding="utf-8")
print("\u2713 index.html autónomo escrito:", len(HTML), "bytes")
