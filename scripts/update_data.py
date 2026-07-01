#!/usr/bin/env python3
"""
update_data.py — actualiza public/data.json con datos frescos usando Claude + búsqueda web.

Para cada liga trae, con la fecha de cada evento:
  - fichajes (transfers), movimientos de banquillo (coaches), destacados (highlights)
Y, una vez por semana o cuando falten, las plantillas (rosters) de los equipos top.

Requisitos:  pip install anthropic requests   +   ANTHROPIC_API_KEY en el entorno.
Uso:  python scripts/update_data.py        |    python scripts/update_data.py --dry-run
"""
import os, sys, json, datetime, pathlib, time

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "public" / "data.json"

LEAGUE_LABEL = {
    "nba": "NBA (baloncesto, Estados Unidos)",
    "euroliga": "EuroLeague (baloncesto europeo)",
    "eurocup": "EuroCup (baloncesto europeo)",
    "bcl": "Basketball Champions League (BCL, FIBA)",
    "endesa": "Liga Endesa ACB (baloncesto, España)",
    "lnb": "Betclic Élite / LNB Pro A (baloncesto, Francia)",
    "bbl": "easyCredit BBL (baloncesto, Alemania)",
    "bsl": "Basketbol Süper Ligi BSL (baloncesto, Turquía)",
}
LEAGUE_IDS = list(LEAGUE_LABEL.keys())
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
DRY = "--dry-run" in sys.argv


def load_data(): return json.loads(DATA_PATH.read_text(encoding="utf-8"))
def save_data(d): DATA_PATH.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

def extract_json(text):
    a, b = text.find("{"), text.rfind("}")
    if a == -1 or b == -1: raise ValueError("sin JSON en la respuesta")
    return json.loads(text[a:b + 1])

def ask(client, prompt, max_tokens=2000):
    msg = client.messages.create(
        model=MODEL, max_tokens=max_tokens,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(getattr(b, "text", "") for b in msg.content if getattr(b, "type", "") == "text")
    return extract_json(text)

def news_prompt(label, today):
    return (
f"""Eres un proveedor de datos de baloncesto. Busca en la web las noticias MÁS RECIENTES (hasta hoy {today}, que es la fecha de hoy) sobre la {label}, de cara a la temporada 2026/27.
Devuelve ÚNICAMENTE un objeto JSON válido (sin markdown ni texto extra) con esta forma EXACTA:
{{
 "transfers":[["Jugador","detalle breve","Origen","Destino","Confirmado|Acuerdo|Reportado|Rumor","YYYY-MM-DD"]],
 "coaches":[["Entrenador o club","detalle breve","Equipo","Nuevo|Renovado|Actual","YYYY-MM-DD"]],
 "highlights":[["Titular","detalle breve","TÍTULO|RESULTADO|FICHAJE|BANQUILLO","YYYY-MM-DD"]]
}}
El ÚLTIMO campo de cada fila es la FECHA real del anuncio en formato YYYY-MM-DD; si no la conoces, usa la de hoy ({today}).
Máximo 12 transfers y 8 coaches. En "highlights" incluye SOLO los 4 movimientos MÁS IMPORTANTES y RECIENTES (bombazos, fichajes estrella, campeones), lo más nuevo primero.
Nombres reales de jugadores, clubes y entrenadores. Etiqueta rumores como "Rumor". No inventes. Todo en español.""")

def roster_prompt(label):
    return (
f"""Dame las plantillas actuales de cara a 2026/27 de los principales equipos de la {label}.
Devuelve ÚNICAMENTE un objeto JSON válido (sin markdown) con esta forma:
{{"rosters":{{"Nombre del equipo":[["PG|SG|SF|PF|C","Jugador","estado breve"]]}}}}
Incluye 6 equipos importantes, con 8 a 12 jugadores cada uno. El "estado breve" en español (por ejemplo: "renovado", "ficha 26/27", "baja", "hasta 2028"). Usa nombres reales. Sé conciso.""")

def norm_rows(rows, n):
    out = []
    for r in rows:
        if not isinstance(r, list): continue
        r = [str(x) for x in r]
        while len(r) < n: r.append("")
        out.append(r[:n])
    return out

def main():
    data = load_data()
    if DRY:
        print("DRY-RUN. Ligas en el seed:", list(data["leagues"].keys()))
        for lid in LEAGUE_IDS:
            L = data["leagues"].get(lid, {})
            print(f"  {lid}: {len(L.get('transfers',[]))} fichajes, {len(L.get('coaches',[]))} banquillos, "
                  f"{len(L.get('highlights',[]))} destacados, {len(L.get('rosters',{}))} plantillas")
        print("Estructura OK (no se escribe nada en dry-run).")
        return

    try:
        import anthropic
    except ImportError:
        sys.exit("Falta 'anthropic'. Instala: pip install anthropic")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("Falta ANTHROPIC_API_KEY en el entorno.")

    client = anthropic.Anthropic()
    today = datetime.date.today().strftime("%Y-%m-%d")
    # Plantillas: refrescar los lunes, o cuando una liga aún no tenga plantillas (ahorra coste)
    refresh_rosters_all = (datetime.date.today().weekday() == 0)

    for lid in LEAGUE_IDS:
        label = LEAGUE_LABEL[lid]
        data["leagues"].setdefault(lid, {})
        print(f"Actualizando {lid}…")
        try:
            j = ask(client, news_prompt(label, today), max_tokens=2200)
            if j.get("transfers"):  data["leagues"][lid]["transfers"]  = norm_rows(j["transfers"], 6)
            if j.get("coaches"):    data["leagues"][lid]["coaches"]    = norm_rows(j["coaches"], 5)
            if j.get("highlights"): data["leagues"][lid]["highlights"] = norm_rows(j["highlights"], 4)
            print(f"  ✓ noticias: {len(j.get('transfers',[]))} fichajes, {len(j.get('coaches',[]))} banquillos")
        except Exception as e:
            print(f"  ! noticias {lid}: {e} (se mantiene lo previo)")

        need_rosters = refresh_rosters_all or not data["leagues"][lid].get("rosters")
        if need_rosters:
            try:
                jr = ask(client, roster_prompt(label), max_tokens=4000)
                rosters = jr.get("rosters", {})
                clean = {}
                for team, players in rosters.items():
                    if isinstance(players, list) and players:
                        clean[str(team)] = norm_rows(players, 3)
                if clean:
                    data["leagues"][lid]["rosters"] = clean
                    print(f"  ✓ plantillas: {len(clean)} equipos")
            except Exception as e:
                print(f"  ! plantillas {lid}: {e} (se mantienen las previas)")
        time.sleep(1)

    now = datetime.datetime.now(datetime.timezone.utc)
    data["updated"] = now.isoformat()
    meses = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]
    data["updatedLabel"] = f"{now.day} {meses[now.month-1]} {now.year}"
    save_data(data)
    print(f"✓ data.json actualizado · {data['updatedLabel']}")


if __name__ == "__main__":
    main()
