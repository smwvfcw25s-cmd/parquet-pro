# PARQUET PRO

Panel de baloncesto (NBA · Euroliga · Liga Endesa) que se **actualiza solo**.
La web no contiene datos propios: lee un `public/data.json` que un robot rellena
cada pocas horas usando Claude con búsqueda web. Cero servidores que mantener.

```
parquet-pro/
├── index.html                 ← la web (un solo archivo, sin build)
├── public/
│   └── data.json              ← los datos (lo reescribe el robot)
├── scripts/
│   ├── build_site.py          ← genera data.json + index.html desde el seed
│   └── update_data.py         ← el robot: Claude + búsqueda web → data.json
├── .github/workflows/
│   └── update.yml             ← cron: corre el robot cada 3 h y sube data.json
└── requirements.txt
```

## Dos formas de que se actualice solo

**A) Autónomo en el navegador (la propia web se actualiza).** Abre `index.html`,
pulsa el engranaje, pega tu clave de la API de Anthropic y la web buscará en
internet (vía Claude) para refrescar fichajes, banquillos y destacados. Para que
lo haga sola al abrirse y cada pocas horas, pega la clave en `CONFIG.API_KEY`
dentro del `index.html`. Es lo más "solitario": un solo archivo, sin servidor.
Aviso: la clave queda visible en el archivo, así que úsalo en un repo/host privado.

**B) Robot de GitHub Actions (recomendado, no expone la clave).** El cron ejecuta
`update_data.py` cada 3 h, reescribe `data.json` y la web lo lee. La clave vive como
secreto en GitHub, nunca en el navegador.

Puedes usar las dos a la vez: la web lee `data.json` (robot) y, si hay clave, además
se refresca sola en cliente.

## Cómo funciona

1. `index.html` carga `./data.json` al abrirse. Si no lo encuentra (p. ej. abierto
   como archivo suelto), usa una copia incrustada para no quedarse en blanco.
2. `update_data.py` pregunta a Claude, **con búsqueda web activada**, por los últimos
   fichajes, movimientos de banquillo y destacados de cada liga, y exige respuesta en
   JSON. Conserva clasificaciones/resultados/plantillas salvo que conectes una API de datos.
3. GitHub Actions ejecuta ese script cada 3 horas y hace commit del `data.json` nuevo.
   La web, al recargar, muestra los datos frescos.

## Puesta en marcha (15 min)

1. **Crea un repositorio** en GitHub y sube esta carpeta.
2. **Añade tu clave**: Settings → Secrets and variables → Actions → New repository secret
   - Nombre: `ANTHROPIC_API_KEY`  · Valor: tu clave de la API de Anthropic.
3. **Activa Actions** (pestaña *Actions*). Lánzalo a mano una vez con *Run workflow*
   para comprobar que escribe `public/data.json`. Luego irá solo cada 3 h.
4. **Publica la web** (estático, gratis). Cualquiera vale:
   - **Cloudflare Pages / Netlify / Vercel**: conecta el repo, sin build, carpeta raíz.
   - **GitHub Pages**: Settings → Pages → Deploy from branch → root.
   Asegúrate de que `index.html` y `public/data.json` quedan accesibles. Si tu host sirve
   `public/` aparte, mueve `data.json` junto al `index.html` o ajusta el `fetch` del HTML.

## Probar en local

```bash
pip install -r requirements.txt
python scripts/update_data.py --dry-run     # valida sin gastar API
export ANTHROPIC_API_KEY=sk-...             # tu clave
python scripts/update_data.py               # actualiza data.json de verdad
python -m http.server 8000                  # abre http://localhost:8000
```

## Subir el nivel (opcional)

- **Clasificaciones y resultados en vivo**: conecta **API-Sports (api-basketball)**.
  Hay un gancho en `update_data.py` → `fetch_standings_apisports()`; añade el secret
  `APISPORTS_KEY`, descoméntalo en el workflow y completa el parseo por liga.
  La ACB no tiene API pública: para esa, raspar `acb.com` o seguir con el seed + Claude.
- **Más frecuencia**: cambia el `cron` del workflow (ojo al consumo de API).
- **Más ligas**: añade entradas en `LEAGUE_LABEL` (script) y en `LEAGUES_META` (web).
- **Tweets embebidos**: requieren la API de X (de pago). De momento la pestaña *Fuentes*
  enlaza a las mejores cuentas, que es lo más práctico y gratis.

## Notas

- Datos iniciales verificados a 30 jun 2026 (basketball-reference, euroleaguebasketball,
  basketnews, acb.com).
- El robot prioriza lo confirmado y etiqueta rumores como tales, pero conviene revisar:
  el mercado va rápido y la búsqueda web no es infalible.
