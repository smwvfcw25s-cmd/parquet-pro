#!/usr/bin/env python3
"""
update_data.py — actualiza public/data.json con datos frescos.

Cómo funciona:
  - Para cada liga (NBA, Euroliga, Liga Endesa) pide a Claude, CON la herramienta
    de búsqueda web activada, las últimas noticias de fichajes, movimientos de
    banquillo y destacados, y exige una respuesta SOLO en JSON.
  - Conserva clasificaciones, resultados y plantillas previos salvo que tengas
    una API de datos conectada (ver fetch_standings_apisports, opcional).
  - Escribe public/data.json con una nueva marca de tiempo.

Pensado para correr en GitHub Actions cada pocas horas (ver .github/workflows/update.yml).

Requisitos:
  pip install anthropic requests
  Variable de entorno ANTHROPIC_API_KEY  (obligatoria)
  Variable de entorno APISPORTS_KEY      (opcional, para clasificaciones en vivo)

Uso:
  python scripts/update_data.py            # actualiza de verdad
  python scripts/update_data.py --dry-run  # no llama a la red, solo valida el flujo
"""
import os, sys, json, re, datetime, pathlib, time

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "public" / "data.json"

LEAGUE_LABEL = {
    "nba": "NBA (baloncesto, Estados Unidos)",
    "euroliga": "EuroLeague (baloncesto europeo)",
    "endesa": "Liga Endesa ACB (baloncesto, España)",
}
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
DRY = "--dry-run" in sys.argv


def load_data():
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def save_data(data):
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def extract_json(text):
    """Saca el primer objeto JSON de un texto que puede traer ruido alrededor."""
    a, b = text.find("{"), text.rfind("}")
    if a == -1 or b == -1:
        raise ValueError("sin JSON en la respuesta")
    return json.loads(text[a:b + 1])


def ask_claude_for_league(client, league_id):
    """Devuelve dict con transfers / coaches / highlights frescos para una liga."""
    label = LEAGUE_LABEL[league_id]
    today = datetime.date.today().strftime("%d/%m/%Y")
    prompt = f"""Eres un proveedor de datos de baloncesto. Busca en la web las noticias MÁS RECIENTES
(hasta hoy {today}) sobre la {label}, de cara a la temporada 2026/27.

Devuelve ÚNICAMENTE un objeto JSON válido (sin markdown ni texto antes o después) con esta forma EXACTA:
{{
 "transfers":[["Jugador","detalle breve","Origen","Destino","Confirmado|Acuerdo|Reportado|Rumor"]],
 "coaches":[["Entrenador o club","detalle breve","Equipo","Nuevo|Renovado|Actual"]],
 "highlights":[["Titular","detalle breve","TÍTULO|RESULTADO|FICHAJE|BANQUILLO"]]
}}
Reglas:
- Máximo 12 movimientos en "transfers", 8 en "coaches", 4 en "highlights".
- Prioriza lo CONFIRMADO y reciente. Usa nombres reales de jugadores, clubes y entrenadores.
- Si un dato es rumor, etiquétalo como "Rumor". No inventes.
- Texto en español. Sé conciso."""

    msg = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
    j = extract_json(text)
    out = {}
    for key in ("transfers", "coaches", "highlights"):
        rows = j.get(key, [])
        if isinstance(rows, list) and rows:
            out[key] = [list(map(str, r)) for r in rows if isinstance(r, list)]
    return out


def fetch_standings_apisports(league_id):
    """OPCIONAL: clasificaciones desde API-Sports si hay APISPORTS_KEY.
    Devuelve None si no hay clave o si la liga no está soportada aquí.
    Mapea: NBA=12, EuroLeague=120, Liga Endesa=117 (IDs de api-basketball)."""
    key = os.environ.get("APISPORTS_KEY")
    if not key:
        return None
    import requests
    league_map = {"nba": 12, "euroliga": 120, "endesa": 117}
    if league_id not in league_map:
        return None
    season = datetime.date.today().year  # ajusta si la temporada aún no arrancó
    try:
        r = requests.get(
            "https://v1.basketball.api-sports.io/standings",
            headers={"x-apisports-key": key},
            params={"league": league_map[league_id], "season": f"{season-1}-{season}"},
            timeout=30,
        )
        r.raise_for_status()
        # El parseo fino depende del formato de la liga; se deja como gancho.
        # Devuelve None para no pisar el seed si no se transforma.
        return None
    except Exception as e:
        print(f"  · API-Sports {league_id}: {e}")
        return None


def main():
    data = load_data()

    if DRY:
        print("DRY-RUN · no se llama a la red. Validando estructura del seed actual:")
        for lid in ("nba", "euroliga", "endesa"):
            L = data["leagues"][lid]
            print(f"  {lid}: {len(L['transfers'])} fichajes, {len(L['coaches'])} banquillos, {len(L['highlights'])} destacados")
        # simula merge
        data["updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"
        print("Estructura OK. (No se ha escrito nada en dry-run)")
        return

    try:
        import anthropic
    except ImportError:
        sys.exit("Falta el paquete 'anthropic'. Instala con: pip install anthropic")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("Falta ANTHROPIC_API_KEY en el entorno.")

    client = anthropic.Anthropic()
    changed = False

    for lid in ("nba", "euroliga", "endesa"):
        print(f"Actualizando {lid}…")
        try:
            fresh = ask_claude_for_league(client, lid)
            for key, rows in fresh.items():
                if rows:
                    data["leagues"][lid][key] = rows
                    changed = True
            print(f"  ✓ {', '.join(f'{k}:{len(v)}' for k, v in fresh.items()) or 'sin cambios'}")
        except Exception as e:
            print(f"  ! error en {lid}: {e} (se mantienen los datos previos)")

        st = fetch_standings_apisports(lid)
        if st:
            data["leagues"][lid]["standings"] = st
            changed = True
        time.sleep(1)

    now = datetime.datetime.now(datetime.timezone.utc)
    data["updated"] = now.isoformat() + "Z"
    meses = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]
    data["updatedLabel"] = f"{now.day} {meses[now.month-1]} {now.year}"
    save_data(data)
    print(f"✓ data.json actualizado ({'con cambios' if changed else 'solo marca de tiempo'}) · {data['updatedLabel']}")


if __name__ == "__main__":
    main()
