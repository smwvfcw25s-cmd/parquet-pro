#!/usr/bin/env python3
"""
build_site.py — genera public/data.json (seed real verificado) e index.html
con los datos inline para que la web funcione sin conexión y en cualquier host.

Esto solo se usa para crear la base inicial y/o regenerar el HTML.
El que actualiza los datos a diario es scripts/update_data.py.
"""
import json, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
PUBLIC.mkdir(exist_ok=True)

# ----------------------------------------------------------------------------
# DATASET REAL (verificado 30 jun 2026)
# Fuentes: basketball-reference, landofbasketball, euroleaguebasketball,
#          basketnews, acb.com, Wikipedia.
# ----------------------------------------------------------------------------
ROSTERS = {
    "Real Madrid": [
        ["PG", "Facundo Campazzo", "Hasta 2027"], ["PG", "Andrés Feliz", "Hasta 2027"],
        ["PG", "Theo Maledon", "Hasta 2027"], ["SG", "Sergio Llull", "Renovado"],
        ["SG", "David Kramer", "Hasta 2027"], ["SG/SF", "Gabriele Procida", "Hasta 2028"],
        ["SF", "Alberto Abalde", "Hasta 2027"], ["SF/PF", "Mario Hezonja", "Hasta 2029"],
        ["PF", "Chuma Okeke", "Hasta 2027"], ["PF", "Gabriel Deck", "Hasta 2028"],
        ["PF/C", "Izan Almansa", "Hasta 2029"], ["C", "Usman Garuba", "Hasta 2027"],
        ["C", "Edy Tavares", "Hasta 2029"], ["C", "Alex Len", "Hasta 2026 +1"],
    ],
    "FC Barcelona": [
        ["PG", "Juan Núñez", "Hasta 2027"], ["PG", "Juani Marcos", "Hasta 2027"],
        ["PG", "Tomas Satoransky", "Finaliza (rumor salida)"], ["SG", "Nicolás Laprovittola", "Finaliza"],
        ["SG", "Kevin Punter", "Hasta 2027"], ["SG", "Darío Brizuela", "Hasta 2028"],
        ["SF", "Will Clyburn", "Hasta 2027"], ["PF", "Joel Parra", "Hasta 2028"],
        ["PF", "Tornike Shengelia", "Hasta 2028"], ["C", "Willy Hernangómez", "Finaliza (rumor salida)"],
        ["C", "Youssoupha Fall", "Finaliza"], ["—", "Moses Wright / Josh Nebo / Nkamhoua", "Entrantes"],
    ],
    "Valencia Basket": [
        ["PG", "TJ Shorts", "Ficha 26/27 (ex-Panathinaikos)"], ["PG", "Jean Montero", "Hasta 2028"],
        ["PG/SG", "Omari Moore", "Hasta 2027"], ["SG", "Isaac Nogués", "Hasta 2027"],
        ["SG", "Sergio De Larrea", "Multianual"], ["SG/SF", "Josep Puerto", "Hasta 2027"],
        ["SF", "Kameron Taylor", "Renueva (récord)"], ["SF", "Xabi López-Aróstegui", "Hasta 2027"],
        ["PF", "Nate Reuvers", "Hasta 2028"], ["PF/C", "Jaime Pradilla", "Hasta 2027 (oferta RM 11M€)"],
        ["C", "Neal Sako", "Hasta 2027"], ["C", "Yankuba Sima", "Hasta 2028"],
    ],
    "Baskonia": [
        ["PG", "Rafa Villar", "Hasta 2028"], ["PG", "Kobi Simmons", "Renueva hasta 2028"],
        ["PG", "Matteo Spagnolo", "Hasta 2028"], ["SG", "Markus Howard", "Hasta 2028"],
        ["SF", "DJ Stewart", "Ficha 26/27"], ["PF/SF", "Clément Frisch", "Hasta 2028"],
        ["PF", "Rodions Kurucs", "Hasta 2028"], ["PF", "Tadas Sedekerskis", "Hasta 2029"],
        ["C", "Khalifa Diop", "Largo plazo"], ["C/PF", "Mamadi Diakité", "Hasta 2027 (rumor salida)"],
    ],
    "Olympiacos": [
        ["PG", "Thomas Walkup", "Hasta 2026 +1"], ["PG", "Cory Joseph", "Hasta 2026 +1"],
        ["SG", "Evan Fournier", "Hasta 2029"], ["SG", "Tyler Dorsey", "Hasta 2027"],
        ["SF", "Kostas Papanikolaou", "Finaliza"], ["SF/PG", "Tyson Ward", "Hasta 2027"],
        ["PF", "Sasha Vezenkov", "Hasta 2029"], ["C", "Nikola Milutinov", "Hasta 2028"],
        ["C", "Tyrique Jones", "Hasta 2028"], ["C", "Donta Hall", "Hasta 2028"],
        ["PG", "Codi Miller-McIntyre", "Entrante"],
    ],
    "Panathinaikos": [
        ["PG", "Jerian Grant", "Hasta 2028"], ["SG", "Kostas Sloukas", "Hasta 2027"],
        ["SG", "Kendrick Nunn", "Hasta 2028"], ["SF", "Cedi Osman", "Hasta 2027"],
        ["PF", "Juancho Hernangómez", "Hasta 2027"], ["PF", "Kostas Mitoglou", "Hasta 2029"],
        ["PF", "Nigel Hayes-Davis", "Hasta 2028"], ["C", "Mathias Lessort", "Hasta 2028"],
        ["C", "Moustapha Fall", "Ficha 26/27 (ex-Olympiacos)"], ["SG", "Brancou Badio", "Entrante (ex-Valencia)"],
    ],
    "Fenerbahçe": [
        ["PG", "Wade Baldwin IV", "Hasta 2026 +1"], ["PG", "Shane Larkin", "Ficha 26/27 (ex-Efes)"],
        ["SG", "Talen Horton-Tucker", "Hasta 2027"], ["SF", "Tarik Biberovic", "Hasta 2028"],
        ["SF", "Shavon Shields", "Ficha 26/27 (ex-Milán)"], ["PF", "Mikael Jantunen", "Hasta 2027"],
        ["PF/C", "Nicolò Melli", "Renueva"], ["PF/SF", "Braxton Key", "Entrante (ex-Valencia)"],
        ["C", "Chris Silva", "Hasta 2026 +1"], ["C", "Marcus Bingham", "Entrante"],
    ],
}

LEAGUES = {
    "nba": {
        "champion": "New York Knicks",
        "championNote": "3.º título, primero desde 1973 · venció a San Antonio Spurs 4-1 · técnico Mike Brown",
        "results": [
            ["New York Knicks", "San Antonio Spurs", "4-1", "Final NBA"],
            ["New York Knicks", "San Antonio Spurs", "105-95", "Final · G5"],
            ["Oklahoma City Thunder", "—", "64-18", "Mejor balance liga"],
        ],
        "standings": {
            "east": [
                ["Detroit Pistons", 60, 22], ["Boston Celtics", 56, 26], ["New York Knicks", 53, 29],
                ["Cleveland Cavaliers", 52, 30], ["Toronto Raptors", 46, 36], ["Atlanta Hawks", 46, 36],
                ["Philadelphia 76ers", 45, 37], ["Orlando Magic", 45, 37], ["Charlotte Hornets", 44, 38],
                ["Miami Heat", 43, 39], ["Milwaukee Bucks", 32, 50], ["Chicago Bulls", 31, 51],
                ["Brooklyn Nets", 20, 62], ["Indiana Pacers", 19, 63], ["Washington Wizards", 17, 65],
            ],
            "west": [
                ["Oklahoma City Thunder", 64, 18], ["San Antonio Spurs", 62, 20], ["Denver Nuggets", 54, 28],
                ["Los Angeles Lakers", 53, 29], ["Houston Rockets", 52, 30], ["Minnesota Timberwolves", 49, 33],
                ["Portland Trail Blazers", 42, 40], ["Phoenix Suns", 45, 37], ["LA Clippers", 42, 40],
                ["Golden State Warriors", 37, 45], ["New Orleans Pelicans", 26, 56], ["Dallas Mavericks", 26, 56],
                ["Memphis Grizzlies", 25, 57], ["Sacramento Kings", 22, 60], ["Utah Jazz", 22, 60],
            ],
        },
        "transfers": [
            ["Miles Bridges", "Traspaso a Phoenix", "Charlotte", "Phoenix Suns", "Confirmado"],
            ["Marcus Smart", "Acuerdo reportado a 3 años", "Lakers", "Houston Rockets", "Reportado"],
            ["Giannis Antetokounmpo", "Traspaso bomba con Miami implicado", "Milwaukee", "Miami Heat", "Reportado"],
            ["Jonas Valančiūnas", "Saldría de la NBA rumbo a Žalgiris", "Denver", "Žalgiris", "Reportado"],
            ["Kawhi Leonard", "Rumores de traspaso", "LA Clippers", "Mavericks / Raptors", "Rumor"],
            ["LeBron James", "Agente libre, conversaciones con Lakers estancadas", "Lakers", "—", "Rumor"],
            ["Robert Williams III", "Salida esperada de Portland", "Portland", "Lakers / Celtics", "Rumor"],
            ["Naz Reid", "Objetivo de los Lakers", "Charlotte", "Lakers", "Rumor"],
        ],
        "coaches": [
            ["Mike Brown", "Campeón con los Knicks en su 1.ª temporada", "New York Knicks", "Actual"],
            ["Portland Trail Blazers", "Contratan nuevo entrenador (29 jun)", "Portland", "Nuevo"],
        ],
        "highlights": [
            ["Knicks campeones", "Nueva York gana su 3.º anillo, 1.º desde 1973, ante los Spurs (4-1)", "TÍTULO"],
            ["OKC, muralla en el Oeste", "Thunder cierran con el mejor balance (64-18)", "RESULTADO"],
            ["Giannis, terremoto", "Reportado un traspaso bomba con Miami en escena", "FICHAJE"],
        ],
        "sources": [
            ["Basketball-Reference", "https://www.basketball-reference.com/leagues/NBA_2026.html"],
            ["NBA.com standings", "https://www.nba.com/standings"],
            ["BasketNews · NBA Rumors", "https://basketnews.com/nba-rumors.html"],
        ],
        "accounts": [
            ["Shams Charania", "https://x.com/ShamsCharania"], ["Marc Stein", "https://x.com/TheSteinLine"],
            ["Chris Haynes", "https://x.com/ChrisBHaynes"], ["Bobby Marks", "https://x.com/BobbyMarks42"],
        ],
    },
    "euroliga": {
        "champion": "Olympiacos",
        "championNote": "4.º título, primero en 13 años · líder de la fase regular · técnico Georgios Bartzokas",
        "results": [
            ["Olympiacos", "Real Madrid", "92-85", "Final"],
            ["Olympiacos", "Fenerbahçe", "79-61", "Semifinal F4"],
            ["Real Madrid", "Valencia Basket", "105-90", "Semifinal F4"],
        ],
        "standings": {
            "playoffs": [
                ["1", "Olympiacos", "Campeón"], ["2", "Valencia Basket", "Semifinal"],
                ["3", "Real Madrid", "Subcampeón"], ["4", "Fenerbahçe", "Semifinal F4"],
                ["5", "Žalgiris Kaunas", "Cuartos"], ["6", "Hapoel Tel Aviv", "Cuartos"],
                ["7-10", "AS Mónaco", "Cuartos (play-in)"], ["7-10", "Panathinaikos", "Cuartos (play-in)"],
            ],
            "regularTop": [
                ["Olympiacos", 26, 12], ["Valencia Basket", 25, 13],
                ["Real Madrid", 24, 14], ["Fenerbahçe", 24, 14],
            ],
        },
        "transfers": [
            ["Shane Larkin", "Fichaje estrella", "Anadolu Efes", "Fenerbahçe", "Confirmado"],
            ["Shavon Shields", "Refuerzo exterior", "Olimpia Milán", "Fenerbahçe", "Confirmado"],
            ["Jonas Valančiūnas", "Acordado, pendiente de salir de la NBA", "Denver (NBA)", "Žalgiris", "Acuerdo"],
            ["TJ Shorts", "Cambio de gigante griego a la ACB", "Panathinaikos", "Valencia Basket", "Confirmado"],
            ["Matthew Strazel", "Base internacional francés", "AS Mónaco", "Anadolu Efes", "Confirmado"],
            ["Dario Šarić", "Regreso a Europa", "NBA", "Anadolu Efes", "Confirmado"],
            ["Moustapha Fall", "Pívot del campeón al rival", "Olympiacos", "Panathinaikos", "Confirmado"],
            ["Bonzie Colson", "Regresa a Tel Aviv", "Fenerbahçe", "Maccabi", "Confirmado"],
            ["Johannes Thiemann", "Campeón del mundo al Bayern", "Partizan", "Bayern Múnich", "Confirmado"],
            ["DJ Stewart", "Alero versátil", "—", "Baskonia", "Confirmado"],
            ["Chris Jones", "Base con experiencia", "—", "Crvena Zvezda", "Confirmado"],
            ["Alec Peters", "Ala-pívot tirador", "Olympiacos", "Olimpia Milán", "Confirmado"],
            ["Jaime Pradilla", "Oferta de 11M€ del Madrid", "Valencia", "Real Madrid", "Rumor"],
            ["Nando De Colo", "Se retira", "—", "—", "Retiro"],
            ["Jan Vesely", "Se retira", "FC Barcelona", "—", "Retiro"],
        ],
        "coaches": [
            ["Željko Obradović", "Nuevo entrenador (sale Ergin Ataman)", "Panathinaikos", "Nuevo"],
            ["Tony Parker", "Nuevo entrenador + 5 fichajes", "ASVEL", "Nuevo"],
            ["Álex Mumbrú", "Nuevo entrenador", "Virtus Bolonia", "Nuevo"],
            ["Ibon Navarro", "Nuevo entrenador", "Crvena Zvezda", "Nuevo"],
            ["Georgios Bartzokas", "Renueva hasta 2029", "Olympiacos", "Renovado"],
            ["Šarūnas Jasikevičius", "Renueva hasta 2029", "Fenerbahçe", "Renovado"],
            ["Joan Peñarroya", "Renueva hasta 2028", "Partizan", "Renovado"],
            ["FC Bayern Múnich", "Anuncia nuevo entrenador", "Bayern", "Nuevo"],
        ],
        "highlights": [
            ["Olympiacos, por fin", "El líder de la regular se corona campeón, 13 años después, ante el Madrid", "TÍTULO"],
            ["Larkin a Fenerbahçe", "El base sale del Efes para reforzar al rival turco", "FICHAJE"],
            ["Obradović vuelve a un banquillo", "El técnico serbio aterriza en el Panathinaikos", "BANQUILLO"],
            ["Valančiūnas, de vuelta a casa", "Acuerdo con Žalgiris pendiente de su salida de la NBA", "FICHAJE"],
        ],
        "sources": [
            ["BasketNews · Mercado Euroliga", "https://basketnews.com/news-248207-euroleague-transfer-market-2026-rosters-signings-rumors.html"],
            ["EuroLeague oficial", "https://www.euroleaguebasketball.net/en/euroleague/standings/"],
            ["Eurohoops", "https://www.eurohoops.net/en/"],
        ],
        "accounts": [
            ["BasketNews", "https://x.com/BasketNews_com"], ["David Pick", "https://x.com/IAmDPick"],
            ["Sportando", "https://x.com/Sportando"], ["Eurohoops", "https://x.com/Eurohoopsnet"],
        ],
        "rosters": ROSTERS,
    },
    "endesa": {
        "champion": "Valencia Basket",
        "championNote": "2.º título de Liga · venció al Barça 3-1 (84-108 en el Palau) · técnico Pedro Martínez · MVP Jean Montero",
        "results": [
            ["Valencia Basket", "FC Barcelona", "3-1", "Final"],
            ["FC Barcelona", "Valencia Basket", "84-108", "Final · G4"],
            ["Jean Montero", "MVP del Playoff Final", "23,8 pts", "Premio"],
        ],
        "standings": {
            "final": [
                "Valencia Basket", "Barça", "Asisa Joventut", "La Laguna Tenerife", "Real Madrid",
                "Kosner Baskonia", "UCAM Murcia", "Surne Bilbao", "Unicaja", "Kids&Us Manresa",
                "Río Breogán", "Bàsquet Girona", "San Pablo Burgos", "Hiopos Lleida",
                "Casademont Zaragoza", "MoraBanc Andorra", "Dreamland Gran Canaria", "Coviran Granada",
            ],
        },
        "transfers": [
            ["Darius Thompson", "Se desvincula del club", "Valencia Basket", "—", "Confirmado"],
            ["Marcis Steinbergs", "Refuerzo interior letón", "Kids&Us Manresa", "UCAM Murcia", "Confirmado"],
            ["Jonathan Barreiro", "Renovación por una temporada", "Unicaja", "Unicaja", "Confirmado"],
            ["Rodrigo Seoane", "Ficha y será cedido a Primera FEB", "Tizona", "Kids&Us Manresa", "Confirmado"],
            ["TJ Shorts", "Refuerzo de campanillas", "Panathinaikos", "Valencia Basket", "Confirmado"],
        ],
        "coaches": [
            ["Pedro Martínez", "Campeón de Liga con Valencia (2.º título del club)", "Valencia Basket", "Actual"],
            ["Sergio Scariolo", "Entrenador del Real Madrid (relevó a Chus Mateo)", "Real Madrid", "Actual"],
            ["Néstor 'Che' García", "Entrenador del Gran Canaria", "Dreamland Gran Canaria", "Actual"],
        ],
        "highlights": [
            ["Valencia, campeón", "El equipo de Pedro Martínez gana su 2.º título batiendo al Barça 3-1", "TÍTULO"],
            ["Montero, MVP", "El base dominicano firma una final de época (23,8 pts, 30,3 de valoración)", "RESULTADO"],
            ["Sorpresa del Barça", "Quinto en la regular, llegó a la final por su lado del cuadro", "RESULTADO"],
        ],
        "sources": [
            ["ACB oficial", "https://www.acb.com/es/liga/clasificacion"],
            ["Gigantes del Basket", "https://www.gigantes.com/liga-endesa/"],
            ["BasketNews · Ligas", "https://basketnews.com/leagues.html"],
        ],
        "accounts": [
            ["Gigantes", "https://x.com/gigantes"], ["Solobasket", "https://x.com/solobasket"],
            ["Chema de Lucas", "https://x.com/chemadelucas"], ["ACB", "https://x.com/ACBCOM"],
        ],
    },
}

DATA = {
    "updated": "2026-06-30T09:00:00Z",
    "updatedLabel": "30 jun 2026",
    "leagues": LEAGUES,
}

# ----------------------------------------------------------------------------
# Escribir data.json
# ----------------------------------------------------------------------------
(PUBLIC / "data.json").write_text(json.dumps(DATA, ensure_ascii=False, indent=2), encoding="utf-8")
print("✓ public/data.json escrito")

# ----------------------------------------------------------------------------
# Generar index.html con SEED inline
# ----------------------------------------------------------------------------
JS_APP = r"""
const { useState, useEffect, useMemo } = React;

const C = { bg:"#0C0F16", bg2:"#11151F", panel:"#161B27", panelHi:"#1C2330", line:"#252C3B",
  line2:"#313A4D", text:"#E8ECF4", sub:"#9AA6BC", faint:"#5E6B82", amber:"#F4A93C",
  live:"#FF5A4D", green:"#3FB950", red:"#F0533A", blue:"#4C9BE8", teal:"#34D3C0", gold:"#E8C45A" };
const FD="'Barlow Condensed',system-ui,sans-serif", FB="'Inter',system-ui,sans-serif", FM="'JetBrains Mono',ui-monospace,monospace";

const LEAGUES_META = [
  { id:"todas", name:"Todas", color:C.amber },
  { id:"nba", name:"NBA", color:"#C8102E" },
  { id:"euroliga", name:"Euroliga", color:"#F4732C" },
  { id:"endesa", name:"Liga Endesa", color:"#FF7A00" },
];
const leagueById = Object.fromEntries(LEAGUES_META.map(l=>[l.id,l]));

const Icon = (paths)=>({size=16,color="currentColor",style}={})=>(
  React.createElement("svg",{width:size,height:size,viewBox:"0 0 24 24",fill:"none",stroke:color,strokeWidth:2,strokeLinecap:"round",strokeLinejoin:"round",style}, paths)
);
const IcSwap = Icon([<path key="a" d="m16 3 4 4-4 4"/>,<path key="b" d="M20 7H4"/>,<path key="c" d="m8 21-4-4 4-4"/>,<path key="d" d="M4 17h16"/>]);
const IcUsers = Icon([<path key="a" d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>,<circle key="b" cx="9" cy="7" r="4"/>,<path key="c" d="M22 21v-2a4 4 0 0 0-3-3.87"/>,<path key="d" d="M16 3.13a4 4 0 0 1 0 7.75"/>]);
const IcBars = Icon([<path key="a" d="M3 3v18h18"/>,<path key="b" d="M18 17V9"/>,<path key="c" d="M13 17V5"/>,<path key="d" d="M8 17v-3"/>]);
const IcSpark = Icon([<path key="a" d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/>]);
const IcTrophy = Icon([<path key="a" d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/>,<path key="b" d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/>,<path key="c" d="M4 22h16"/>,<path key="d" d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/>,<path key="e" d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/>,<path key="f" d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>]);
const IcClip = Icon([<rect key="a" width="8" height="4" x="8" y="2" rx="1"/>,<path key="b" d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>,<path key="c" d="M12 11h4"/>,<path key="d" d="M12 16h4"/>,<path key="e" d="M8 11h.01"/>,<path key="f" d="M8 16h.01"/>]);
const IcExt = Icon([<path key="a" d="M15 3h6v6"/>,<path key="b" d="M10 14 21 3"/>,<path key="c" d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>]);
const IcChev = Icon([<path key="a" d="m6 9 6 6 6-6"/>]);
const IcLink = Icon([<path key="a" d="M9 17H7A5 5 0 0 1 7 7h2"/>,<path key="b" d="M15 7h2a5 5 0 1 1 0 10h-2"/>,<line key="c" x1="8" x2="16" y1="12" y2="12"/>]);
const IcRefresh = Icon([<path key="a" d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>,<path key="b" d="M21 3v5h-5"/>,<path key="c" d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>,<path key="d" d="M3 21v-5h5"/>]);
const IcGear = Icon([<path key="a" d="M20 7h-9"/>,<path key="b" d="M14 17H5"/>,<circle key="c" cx="17" cy="17" r="3"/>,<circle key="d" cx="7" cy="7" r="3"/>]);

// === Autoactualización: pega aquí tu clave para autonomía permanente ===
const CONFIG = { API_KEY: "", AUTO_UPDATE_MINUTES: 180 };
const LIVE_LABEL = { nba:"NBA (baloncesto, EE. UU.)", euroliga:"EuroLeague (baloncesto europeo)", endesa:"Liga Endesa ACB (España)" };
const REFRESH_PROMPT = (label, today) => "Eres un proveedor de datos de baloncesto. Busca en la web las noticias MAS RECIENTES (hasta hoy "+today+") sobre la "+label+", de cara a la temporada 2026/27. Devuelve UNICAMENTE un objeto JSON valido (sin markdown ni texto extra) con esta forma EXACTA: {\"transfers\":[[\"Jugador\",\"detalle\",\"Origen\",\"Destino\",\"Confirmado|Acuerdo|Reportado|Rumor\"]],\"coaches\":[[\"Entrenador o club\",\"detalle\",\"Equipo\",\"Nuevo|Renovado|Actual\"]],\"highlights\":[[\"Titular\",\"detalle\",\"TITULO|RESULTADO|FICHAJE|BANQUILLO\"]]}. Maximo 12 transfers, 8 coaches, 4 highlights. Prioriza lo confirmado y reciente, nombres reales, etiqueta rumores como Rumor, no inventes. En espanol.";
function extractJsonJS(t){ const a=t.indexOf("{"), b=t.lastIndexOf("}"); if(a<0||b<0) throw new Error("sin JSON"); return JSON.parse(t.slice(a,b+1)); }
async function callClaude(apiKey, prompt){
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method:"POST",
    headers:{ "content-type":"application/json", "x-api-key":apiKey, "anthropic-version":"2023-06-01", "anthropic-dangerous-direct-browser-access":"true" },
    body: JSON.stringify({ model:"claude-sonnet-4-6", max_tokens:1500, tools:[{type:"web_search_20250305", name:"web_search"}], messages:[{role:"user", content:prompt}] })
  });
  if(!res.ok) throw new Error("HTTP "+res.status);
  const data = await res.json();
  return (data.content||[]).filter(b=>b.type==="text").map(b=>b.text).join("\n");
}
async function refreshLeagueLive(apiKey, id){
  const today = new Date().toLocaleDateString("es-ES");
  const text = await callClaude(apiKey, REFRESH_PROMPT(LIVE_LABEL[id], today));
  const j = extractJsonJS(text);
  const out = {};
  ["transfers","coaches","highlights"].forEach(k=>{ if(Array.isArray(j[k]) && j[k].length) out[k]=j[k].map(r=>r.map(String)); });
  return out;
}

const TABS = [
  { id:"destacados", name:"Destacados", icon:IcSpark },
  { id:"fichajes", name:"Fichajes", icon:IcSwap },
  { id:"banquillos", name:"Banquillos", icon:IcClip },
  { id:"clasificacion", name:"Clasificación", icon:IcBars },
  { id:"plantillas", name:"Plantillas", icon:IcUsers },
  { id:"fuentes", name:"Fuentes", icon:IcLink },
];
const tagColor = (t)=>({ "TÍTULO":C.gold,"RESULTADO":C.green,"FICHAJE":C.amber,"BANQUILLO":C.teal,
  "Confirmado":C.green,"Acuerdo":C.green,"Reportado":C.blue,"Rumor":C.blue,"Retiro":C.faint,
  "Nuevo":C.teal,"Renovado":C.green,"Actual":C.sub }[t]||C.blue);

function aggregate(DB, field){
  const out=[];
  for(const id of ["nba","euroliga","endesa"]) for(const row of (DB[id] && DB[id][field])||[]) out.push({league:id,row});
  return out;
}

function App(){
  const [payload, setPayload] = useState(SEED);
  const [loading, setLoading] = useState(true);
  const [league, setLeague] = useState("nba");
  const [tab, setTab] = useState("destacados");
  const [rosterTeam, setRosterTeam] = useState(null);
  const [status, setStatus] = useState("idle");      // idle | loading | live | error
  const [apiKey, setApiKey] = useState(CONFIG.API_KEY || "");
  const [showCfg, setShowCfg] = useState(false);
  const [note, setNote] = useState("");

  const selfUpdate = async (key)=>{
    const k = key || apiKey;
    if(!k){ setShowCfg(true); return; }
    setStatus("loading"); setNote("");
    const results = {};
    for(const id of ["nba","euroliga","endesa"]){
      try{ results[id] = await refreshLeagueLive(k, id); }catch(e){ results[id] = null; }
    }
    const ok = Object.values(results).some(Boolean);
    setPayload(prev=>{
      const next = JSON.parse(JSON.stringify(prev));
      for(const id of Object.keys(results)){ const fr = results[id]; if(fr) Object.keys(fr).forEach(f=>{ next.leagues[id][f] = fr[f]; }); }
      const n = new Date(), M=["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"];
      next.updatedLabel = n.getDate()+" "+M[n.getMonth()]+" "+n.getFullYear()+" "+String(n.getHours()).padStart(2,"0")+":"+String(n.getMinutes()).padStart(2,"0");
      return next;
    });
    if(ok){ setStatus("live"); } else { setStatus("error"); setNote("No se pudo actualizar. Revisa la clave o la conexión."); }
  };

  useEffect(()=>{
    fetch("./data.json?_="+Date.now()).then(r=>{ if(!r.ok) throw 0; return r.json(); })
      .then(d=>{ if(d && d.leagues) setPayload(d); }).catch(()=>{}).finally(()=>setLoading(false));
    const onVis=()=>{ if(document.visibilityState==="visible") fetch("./data.json?_="+Date.now()).then(r=>r.ok?r.json():null).then(d=>{ if(d&&d.leagues) setPayload(d); }).catch(()=>{}); };
    document.addEventListener("visibilitychange", onVis);
    let iv=null;
    if(CONFIG.API_KEY){ selfUpdate(CONFIG.API_KEY); iv=setInterval(()=>selfUpdate(CONFIG.API_KEY), Math.max(15, CONFIG.AUTO_UPDATE_MINUTES)*60000); }
    return ()=>{ document.removeEventListener("visibilitychange", onVis); if(iv) clearInterval(iv); };
  },[]);

  const DB = payload.leagues;
  const ROSTERS = (DB.euroliga && DB.euroliga.rosters) || {};
  const lc = leagueById[league].color;
  const D = league==="todas" ? null : DB[league];

  const tickerItems = useMemo(()=>{
    const src = league==="todas"
      ? [...aggregate(DB,"transfers"), ...aggregate(DB,"coaches")]
      : [...(DB[league].transfers||[]).map(r=>({league,row:r})), ...(DB[league].coaches||[]).map(r=>({league,row:r}))];
    return src.filter(it=>["Confirmado","Acuerdo","Nuevo","Renovado"].includes(it.row[it.row.length-1]));
  },[league,payload]);

  const panel = { background:C.panel, border:"1px solid "+C.line, borderRadius:14 };
  const eyebrow = { fontFamily:FB, fontSize:11, letterSpacing:"0.14em", textTransform:"uppercase", color:C.faint, fontWeight:600 };

  return (
  <div style={{background:C.bg,color:C.text,fontFamily:FB,minHeight:"100vh"}}>
    <header style={{borderBottom:"1px solid "+C.line,background:C.bg2,position:"sticky",top:0,zIndex:30}}>
      <div className="mx-auto px-4 sm:px-6" style={{maxWidth:1180}}>
        <div className="flex items-center justify-between" style={{height:62}}>
          <div className="flex items-center" style={{gap:12}}>
            <div style={{width:34,height:34,borderRadius:9,background:C.amber,position:"relative",overflow:"hidden",flexShrink:0}}>
              <div style={{position:"absolute",inset:0,borderRadius:9,border:"2px solid "+C.bg,transform:"scale(0.62)"}}/>
              <div style={{position:"absolute",left:"50%",top:0,bottom:0,width:2,background:C.bg,transform:"translateX(-50%)"}}/>
            </div>
            <div>
              <div style={{fontFamily:FD,fontWeight:800,fontSize:22,letterSpacing:"0.02em",lineHeight:1}}>PARQUET <span style={{color:C.amber}}>PRO</span></div>
              <div style={{...eyebrow,fontSize:9.5}}>base de datos · 25-26 → 26/27</div>
            </div>
          </div>
          <div style={{position:"relative"}}>
            <div className="flex items-center" style={{gap:9}}>
              <span className="flex items-center" style={{gap:6,fontFamily:FM,fontSize:11,color:status==="error"?C.red:C.sub}}>
                <span className={status==="loading"?"pq-pulse":""} style={{width:7,height:7,borderRadius:99,background:status==="loading"?C.amber:status==="live"?C.green:status==="error"?C.red:(loading?C.amber:C.green)}}/>
                <span className="hide-sm">{status==="loading"?"actualizando…":(payload.updatedLabel||"")}</span>
              </span>
              <button onClick={()=>selfUpdate()} disabled={status==="loading"} className="flex items-center" style={{gap:6,padding:"7px 12px",borderRadius:9,background:status==="loading"?C.panelHi:C.amber,color:status==="loading"?C.sub:"#16110A",border:"none",fontFamily:FB,fontWeight:600,fontSize:12.5,cursor:status==="loading"?"default":"pointer"}}>
                <span className={status==="loading"?"pq-spin":""} style={{display:"flex"}}><IcRefresh size={14} color={status==="loading"?C.sub:"#16110A"}/></span> Actualizar
              </button>
              <button onClick={()=>setShowCfg(s=>!s)} aria-label="Ajustes de autoactualización" style={{padding:7,borderRadius:9,background:"transparent",border:"1px solid "+C.line2,color:C.sub,cursor:"pointer",display:"flex"}}><IcGear size={15} color={C.sub}/></button>
            </div>
            {showCfg && <CfgPanel apiKey={apiKey} setApiKey={setApiKey} onRun={(k)=>{setShowCfg(false);selfUpdate(k);}} note={note}/>}
          </div>
        </div>
        <div className="flex pq-scroll" style={{gap:8,overflowX:"auto",paddingBottom:12}}>
          {LEAGUES_META.map(l=>{
            const on=l.id===league;
            return <button key={l.id} onClick={()=>{setLeague(l.id);setRosterTeam(null);if(l.id==="todas"&&["clasificacion","plantillas"].includes(tab))setTab("destacados");}}
              className="flex items-center" style={{gap:7,flexShrink:0,padding:"7px 14px",borderRadius:99,cursor:"pointer",
              background:on?C.panelHi:"transparent",border:"1px solid "+(on?l.color:C.line),color:on?C.text:C.sub,fontFamily:FB,fontWeight:600,fontSize:13}}>
              <span style={{width:8,height:8,borderRadius:99,background:l.color}}/>{l.name}</button>;
          })}
        </div>
      </div>
    </header>

    <div className="pq-ribbon" style={{background:"#08090D",borderBottom:"1px solid "+C.line,overflow:"hidden",position:"relative"}}>
      <div style={{position:"absolute",left:0,top:0,bottom:0,zIndex:2,display:"flex",alignItems:"center",padding:"0 14px",background:"#08090D",borderRight:"1px solid "+C.line}}>
        <span style={{fontFamily:FD,fontWeight:800,fontSize:13,letterSpacing:"0.12em",color:C.amber}}>CONFIRMADO</span>
      </div>
      <div className="pq-track" style={{display:"flex",width:"max-content",animation:"pq-marquee 50s linear infinite",paddingLeft:130}}>
        {[...tickerItems,...tickerItems].map((it,i)=>(
          <span key={i} className="flex items-center" style={{gap:9,padding:"9px 16px",whiteSpace:"nowrap"}}>
            <span style={{width:6,height:6,borderRadius:99,background:leagueById[it.league].color}}/>
            <span style={{fontFamily:FD,fontWeight:700,fontSize:13,letterSpacing:"0.06em",color:C.amber}}>{(it.row[0]||"").toUpperCase()}</span>
            <span style={{fontFamily:FM,fontSize:11,color:C.sub}}>{it.row.length>=5?(it.row[2]+" → "+it.row[3]):it.row[2]}</span>
            <span style={{color:C.line2,marginLeft:4}}>·</span>
          </span>
        ))}
      </div>
    </div>

    <main className="mx-auto px-4 sm:px-6" style={{maxWidth:1180,paddingTop:20,paddingBottom:64}}>
      <div className="flex pq-scroll" style={{gap:2,overflowX:"auto",marginBottom:22,borderBottom:"1px solid "+C.line}}>
        {TABS.map(t=>{const on=t.id===tab;const Ic=t.icon;
          return <button key={t.id} onClick={()=>setTab(t.id)} className="flex items-center" style={{gap:7,flexShrink:0,padding:"11px 13px",background:"transparent",border:"none",borderBottom:"2px solid "+(on?lc:"transparent"),color:on?C.text:C.faint,fontFamily:FB,fontWeight:600,fontSize:13.5,cursor:"pointer",marginBottom:-1}}>
            <Ic size={15}/> {t.name}</button>;})}
      </div>

      {tab==="destacados" && <Destacados DB={DB} league={league} D={D} panel={panel} eyebrow={eyebrow}/>}
      {tab==="fichajes" && <Feed eyebrow={eyebrow} items={league==="todas"?aggregate(DB,"transfers"):DB[league].transfers.map(r=>({league,row:r}))} kind="transfer"/>}
      {tab==="banquillos" && <Feed eyebrow={eyebrow} items={league==="todas"?aggregate(DB,"coaches"):DB[league].coaches.map(r=>({league,row:r}))} kind="coach"/>}
      {tab==="clasificacion" && (league==="todas"?<Empty text="Elige una competición para ver su clasificación."/>:<Clasificacion league={league} D={D} lc={lc} panel={panel} eyebrow={eyebrow}/>)}
      {tab==="plantillas" && (league==="todas"?<Empty text="Elige una competición para ver plantillas."/>:(league==="euroliga"?<Plantillas ROSTERS={ROSTERS} lc={lc} panel={panel} eyebrow={eyebrow} rosterTeam={rosterTeam} setRosterTeam={setRosterTeam}/>:<Empty text={"Plantillas detalladas disponibles para Euroliga. Para "+leagueById[league].name+", revisa la pestaña Fuentes."}/>))}
      {tab==="fuentes" && <Fuentes DB={DB} league={league} panel={panel} eyebrow={eyebrow}/>}
    </main>

    <footer style={{borderTop:"1px solid "+C.line,padding:"16px 0",background:C.bg2}}>
      <div className="mx-auto px-4 sm:px-6 flex items-center justify-between" style={{maxWidth:1180,flexWrap:"wrap",gap:8}}>
        <span style={{fontFamily:FD,fontWeight:700,fontSize:14,color:C.faint,letterSpacing:"0.06em"}}>PARQUET PRO</span>
        <span style={{fontSize:11.5,color:C.faint}}>basketball-reference · euroleaguebasketball · basketnews · acb.com</span>
      </div>
    </footer>
  </div>);
}

function Destacados({DB,league,D,panel,eyebrow}){
  const items = league==="todas"?aggregate(DB,"highlights"):D.highlights.map(r=>({league,row:r}));
  const champs = league==="todas"?["nba","euroliga","endesa"].map(id=>({id,champ:DB[id].champion,note:DB[id].championNote})):[{id:league,champ:D.champion,note:D.championNote}];
  return <div>
    <div className="grid" style={{gridTemplateColumns:champs.length>1?"repeat(auto-fit,minmax(260px,1fr))":"1fr",gap:14,marginBottom:20}}>
      {champs.map(c=>(
        <div key={c.id} style={{...panel,padding:18,position:"relative",overflow:"hidden"}}>
          <div style={{position:"absolute",left:0,top:0,bottom:0,width:4,background:C.gold}}/>
          <div className="flex items-center" style={{gap:8,marginBottom:8}}>
            <IcTrophy size={18} color={C.gold}/>
            <span className="flex items-center" style={{gap:6,...eyebrow,fontSize:10}}>
              <span style={{width:7,height:7,borderRadius:99,background:leagueById[c.id].color}}/>{leagueById[c.id].name} · Campeón 25-26</span>
          </div>
          <div style={{fontFamily:FD,fontWeight:800,fontSize:30,lineHeight:1}}>{c.champ}</div>
          <div style={{fontSize:12.5,color:C.sub,marginTop:8,lineHeight:1.5}}>{c.note}</div>
        </div>))}
    </div>
    <div className="grid" style={{gridTemplateColumns:"repeat(auto-fill,minmax(250px,1fr))",gap:14}}>
      {items.map((it,i)=>{const r=it.row;const accent=tagColor(r[2]);
        return <div key={i} style={{...panel,padding:16,position:"relative",overflow:"hidden"}}>
          <div style={{position:"absolute",left:0,top:0,bottom:0,width:3,background:accent}}/>
          <div className="flex items-center justify-between" style={{marginBottom:10}}>
            <span style={{fontFamily:FM,fontSize:10,fontWeight:700,letterSpacing:"0.1em",color:accent}}>{r[2]}</span>
            <span className="flex items-center" style={{gap:5,...eyebrow,fontSize:10}}><span style={{width:7,height:7,borderRadius:99,background:leagueById[it.league].color}}/>{leagueById[it.league].name}</span>
          </div>
          <div style={{fontFamily:FD,fontWeight:700,fontSize:20,lineHeight:1.05,marginBottom:6}}>{r[0]}</div>
          <div style={{fontSize:13,color:C.sub,lineHeight:1.45}}>{r[1]}</div>
        </div>;})}
    </div>
  </div>;
}

function Feed({items,kind,eyebrow}){
  return <div style={{background:C.panel,border:"1px solid "+C.line,borderRadius:14,padding:"2px 18px"}}>
    {items.map((it,i)=>{const r=it.row;const status=r[r.length-1];const accent=tagColor(status);const isT=kind==="transfer";
      return <div key={i} className="flex items-center" style={{gap:12,padding:"13px 0",borderBottom:i<items.length-1?"1px solid "+C.line:"none"}}>
        {isT?<IcSwap size={17} color={accent}/>:<IcClip size={17} color={accent}/>}
        <div style={{flex:1,minWidth:0}}>
          <div style={{fontFamily:FD,fontWeight:600,fontSize:18,lineHeight:1.1}}>{r[0]}</div>
          <div style={{fontSize:12.5,color:C.sub,marginTop:2}}>{r[1]}</div>
          <div className="flex items-center" style={{gap:6,marginTop:4,fontFamily:FM,fontSize:11,color:C.faint,flexWrap:"wrap"}}>
            {isT?<React.Fragment><span>{r[2]}</span><span style={{color:accent}}>→</span><span>{r[3]}</span></React.Fragment>:<span>{r[2]}</span>}
          </div>
        </div>
        <div className="flex items-center" style={{gap:8}}>
          <span style={{fontFamily:FM,fontSize:10,fontWeight:700,padding:"3px 8px",borderRadius:6,color:accent,background:"#0e1f30",whiteSpace:"nowrap"}}>{status}</span>
          <span style={{width:8,height:8,borderRadius:99,background:leagueById[it.league].color,flexShrink:0}}/>
        </div>
      </div>;})}
  </div>;
}

function RowHead({cols,eyebrow,narrow}){
  return <div className="flex items-center" style={{padding:"9px 16px",borderBottom:"1px solid "+C.line,...eyebrow,fontSize:10}}>
    <span style={{width:narrow?26:48}}>{cols[0]}</span><span style={{flex:1}}>{cols[1]}</span>
    {cols.slice(2).map((c,i)=><span key={i} style={{width:34,textAlign:"right"}}>{c}</span>)}
  </div>;
}
function ResultsStrip({results,eyebrow,panel}){
  return <div style={{marginBottom:18}}>
    <div style={{...eyebrow,marginBottom:8}}>Resultados clave 25-26</div>
    <div className="grid" style={{gridTemplateColumns:"repeat(auto-fill,minmax(220px,1fr))",gap:12}}>
      {results.map((r,i)=>(
        <div key={i} style={{...panel,padding:14}}>
          <div style={{fontFamily:FM,fontSize:10,color:C.faint,marginBottom:8,letterSpacing:"0.08em"}}>{(r[3]||"").toUpperCase()}</div>
          <div className="flex items-center justify-between" style={{gap:8}}>
            <span style={{fontFamily:FD,fontWeight:600,fontSize:16,lineHeight:1.05}}>{r[0]}</span>
            <span style={{fontFamily:FM,fontWeight:700,fontSize:15,color:C.amber,whiteSpace:"nowrap"}}>{r[2]}</span>
          </div>
          {r[1]!=="—" && <div style={{fontFamily:FD,fontWeight:600,fontSize:16,color:C.sub,marginTop:2}}>{r[1]}</div>}
        </div>))}
    </div>
  </div>;
}
function StandingsWL({title,rows,lc,panel,eyebrow,champ}){
  return <div style={{...panel,overflow:"hidden"}}>
    <div style={{padding:"11px 16px",borderBottom:"1px solid "+C.line,...eyebrow,fontSize:11,color:C.text}}>{title}</div>
    <RowHead eyebrow={eyebrow} cols={["#","Equipo","V","D"]} narrow/>
    {rows.map((s,i)=>(
      <div key={i} className="flex items-center" style={{padding:"9px 16px",borderBottom:i<rows.length-1?"1px solid "+C.line:"none",background:i%2?"transparent":"#00000018"}}>
        <span style={{width:26,fontFamily:FM,fontWeight:700,fontSize:12,color:i<6?lc:i<10?C.blue:C.faint}}>{i+1}</span>
        <span style={{flex:1,fontFamily:FD,fontWeight:600,fontSize:15.5}}>{s[0]}{s[0]===champ?<IcTrophy size={12} color={C.gold} style={{display:"inline",marginLeft:5}}/>:null}</span>
        <span style={{width:34,textAlign:"right",fontFamily:FM,fontSize:12.5,color:C.green}}>{s[1]}</span>
        <span style={{width:34,textAlign:"right",fontFamily:FM,fontSize:12.5,color:C.sub}}>{s[2]}</span>
      </div>))}
  </div>;
}
function Clasificacion({league,D,lc,panel,eyebrow}){
  if(league==="nba") return <div>
    <ResultsStrip results={D.results} eyebrow={eyebrow} panel={panel}/>
    <div className="grid" style={{gridTemplateColumns:"repeat(auto-fit,minmax(300px,1fr))",gap:14}}>
      <StandingsWL title="Conferencia Este" rows={D.standings.east} lc={lc} panel={panel} eyebrow={eyebrow} champ="New York Knicks"/>
      <StandingsWL title="Conferencia Oeste" rows={D.standings.west} lc={lc} panel={panel} eyebrow={eyebrow} champ={null}/>
    </div></div>;
  if(league==="euroliga") return <div>
    <ResultsStrip results={D.results} eyebrow={eyebrow} panel={panel}/>
    <div style={{...panel,overflow:"hidden",marginBottom:14}}>
      <RowHead eyebrow={eyebrow} cols={["#","Equipo","Resultado"]}/>
      {D.standings.playoffs.map((s,i)=>(
        <div key={i} className="flex items-center" style={{padding:"11px 16px",borderBottom:i<7?"1px solid "+C.line:"none"}}>
          <span style={{width:48,fontFamily:FM,fontWeight:700,fontSize:12,color:lc}}>{s[0]}</span>
          <span style={{flex:1,fontFamily:FD,fontWeight:600,fontSize:17}}>{s[1]}{i===0?<IcTrophy size={13} color={C.gold} style={{display:"inline",marginLeft:6}}/>:null}</span>
          <span style={{fontSize:12,color:C.sub}}>{s[2]}</span>
        </div>))}
    </div>
    <div style={{...eyebrow,marginBottom:8}}>Líderes fase regular (balance)</div>
    <div style={{...panel,overflow:"hidden"}}>
      {D.standings.regularTop.map((s,i)=>(
        <div key={i} className="flex items-center" style={{padding:"10px 16px",borderBottom:i<3?"1px solid "+C.line:"none"}}>
          <span style={{width:30,fontFamily:FM,fontWeight:700,color:lc}}>{i+1}</span>
          <span style={{flex:1,fontFamily:FD,fontWeight:600,fontSize:16}}>{s[0]}</span>
          <span style={{fontFamily:FM,fontSize:13,color:C.green}}>{s[1]}</span>
          <span style={{fontFamily:FM,fontSize:13,color:C.sub,marginLeft:6}}>– {s[2]}</span>
        </div>))}
    </div></div>;
  return <div>
    <ResultsStrip results={D.results} eyebrow={eyebrow} panel={panel}/>
    <div style={{...panel,overflow:"hidden"}}>
      <RowHead eyebrow={eyebrow} cols={["#","Equipo",""]}/>
      {D.standings.final.map((t,i)=>(
        <div key={i} className="flex items-center" style={{padding:"10px 16px",borderBottom:i<D.standings.final.length-1?"1px solid "+C.line:"none",background:i%2?"transparent":"#00000018"}}>
          <span style={{width:30,fontFamily:FM,fontWeight:700,fontSize:13,color:i<8?lc:C.faint}}>{i+1}</span>
          <span style={{flex:1,fontFamily:FD,fontWeight:600,fontSize:17}}>{t}{i===0?<IcTrophy size={13} color={C.gold} style={{display:"inline",marginLeft:6}}/>:null}</span>
          {i<8?<span style={{fontFamily:FM,fontSize:10,color:C.faint}}>playoff</span>:null}
        </div>))}
    </div>
    <p style={{marginTop:14,fontSize:12,color:C.faint}}>Clasificación final 25-26 (incluye playoff). Los 8 primeros disputaron el playoff por el título.</p>
  </div>;
}

function Plantillas({ROSTERS,lc,panel,eyebrow,rosterTeam,setRosterTeam}){
  const teams = Object.keys(ROSTERS);
  const team = rosterTeam || teams[0];
  const roster = ROSTERS[team]||[];
  const [open,setOpen]=useState(false);
  return <div>
    <div style={{position:"relative",marginBottom:16,maxWidth:340}}>
      <button onClick={()=>setOpen(o=>!o)} className="flex items-center justify-between w-full" style={{padding:"11px 14px",borderRadius:10,background:C.panel,border:"1px solid "+C.line2,color:C.text,fontFamily:FD,fontWeight:600,fontSize:18,cursor:"pointer"}}>
        {team} <IcChev size={16} color={C.sub}/>
      </button>
      {open && <div className="pq-scroll" style={{position:"absolute",top:"calc(100% + 6px)",left:0,right:0,zIndex:20,background:C.panelHi,border:"1px solid "+C.line2,borderRadius:10,maxHeight:280,overflowY:"auto"}}>
        {teams.map(t=><button key={t} onClick={()=>{setRosterTeam(t);setOpen(false);}} className="flex items-center w-full" style={{padding:"10px 14px",background:"transparent",border:"none",color:t===team?lc:C.text,fontFamily:FB,fontSize:14,cursor:"pointer",textAlign:"left"}}>{t}</button>)}
      </div>}
    </div>
    <div style={{...panel,overflow:"hidden"}}>
      <div className="flex items-center" style={{padding:"10px 16px",borderBottom:"1px solid "+C.line,...eyebrow,fontSize:10}}>
        <span style={{width:54}}>Pos.</span><span style={{flex:1}}>Jugador</span><span>Estado 26/27</span>
      </div>
      {roster.map((p,i)=>{const out=/salida|finaliza/i.test(p[2]);const inn=/ficha|entrante|renueva|regres/i.test(p[2]);
        return <div key={i} className="flex items-center" style={{padding:"10px 16px",borderBottom:i<roster.length-1?"1px solid "+C.line:"none",background:i%2?"transparent":"#00000018"}}>
          <span style={{width:54,fontFamily:FM,fontWeight:700,fontSize:12,color:lc}}>{p[0]}</span>
          <span style={{flex:1,fontFamily:FD,fontWeight:600,fontSize:16}}>{p[1]}</span>
          <span style={{fontFamily:FM,fontSize:11,color:out?C.red:inn?C.green:C.sub,textAlign:"right"}}>{p[2]}</span>
        </div>;})}
    </div>
    <p style={{marginTop:14,fontSize:12,color:C.faint}}>Verde = alta/renovación · rojo = posible salida. Mercado en curso.</p>
  </div>;
}

function Fuentes({DB,league,panel,eyebrow}){
  const ls = league==="todas"?["nba","euroliga","endesa"]:[league];
  return <div className="grid" style={{gridTemplateColumns:"repeat(auto-fit,minmax(280px,1fr))",gap:14}}>
    {ls.map(id=>{const D=DB[id];
      return <div key={id} style={{...panel,padding:18}}>
        <div className="flex items-center" style={{gap:7,marginBottom:12}}>
          <span style={{width:9,height:9,borderRadius:99,background:leagueById[id].color}}/>
          <span style={{...eyebrow,fontSize:11,color:C.text}}>{leagueById[id].name}</span>
        </div>
        <div style={{...eyebrow,fontSize:9.5,marginBottom:6}}>Webs (se actualizan a diario)</div>
        {D.sources.map((s,i)=>(
          <a key={i} href={s[1]} target="_blank" rel="noopener noreferrer" className="flex items-center justify-between" style={{textDecoration:"none",padding:"8px 0",borderBottom:"1px solid "+C.line,color:C.text}}>
            <span style={{fontFamily:FB,fontSize:13.5}}>{s[0]}</span><IcExt size={14} color={C.faint}/>
          </a>))}
        <div style={{...eyebrow,fontSize:9.5,margin:"14px 0 6px"}}>Cuentas a seguir (X)</div>
        <div className="flex" style={{flexWrap:"wrap",gap:8}}>
          {D.accounts.map((a,i)=>(
            <a key={i} href={a[1]} target="_blank" rel="noopener noreferrer" style={{textDecoration:"none",padding:"5px 10px",borderRadius:99,border:"1px solid "+C.line2,color:C.sub,fontFamily:FB,fontSize:12.5}}>{a[0]}</a>))}
        </div>
      </div>;})}
  </div>;
}

function CfgPanel({apiKey,setApiKey,onRun,note}){
  const [k,setK]=useState(apiKey||"");
  return <div style={{position:"absolute",right:0,top:"calc(100% + 8px)",zIndex:40,width:300,maxWidth:"90vw",background:C.panelHi,border:"1px solid "+C.line2,borderRadius:12,padding:14,boxShadow:"0 12px 40px #0009"}}>
    <div style={{fontFamily:FD,fontWeight:700,fontSize:17,marginBottom:6}}>Autoactualización</div>
    <div style={{fontSize:12,color:C.sub,lineHeight:1.45,marginBottom:10}}>Pega tu clave de la API de Anthropic y la web buscará en internet para refrescar fichajes, banquillos y destacados. La clave se queda solo en memoria de esta pestaña.</div>
    <input value={k} onChange={e=>setK(e.target.value)} placeholder="sk-ant-..." spellCheck={false} type="password" style={{width:"100%",boxSizing:"border-box",padding:"9px 11px",borderRadius:8,background:C.bg,border:"1px solid "+C.line2,color:C.text,fontFamily:FM,fontSize:12,marginBottom:10}}/>
    <button onClick={()=>{setApiKey(k);onRun(k);}} style={{width:"100%",padding:"9px",borderRadius:8,background:C.amber,color:"#16110A",border:"none",fontFamily:FB,fontWeight:600,fontSize:13,cursor:"pointer"}}>Guardar y actualizar</button>
    {note && <div style={{fontSize:11.5,color:C.red,marginTop:8}}>{note}</div>}
    <div style={{fontSize:11,color:C.faint,marginTop:10,lineHeight:1.45}}>Para autonomía permanente: pega la clave en CONFIG.API_KEY del archivo (repo privado) y se actualizará sola cada pocas horas. Más seguro aún: el robot de GitHub Actions (ver README), que no expone la clave en el navegador.</div>
  </div>;
}

function Empty({text}){
  return <div className="flex items-center justify-center" style={{minHeight:170,border:"1px dashed "+C.line2,borderRadius:14,color:C.faint,fontSize:14,textAlign:"center",padding:24,lineHeight:1.5}}>{text}</div>;
}

ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
"""

HTML = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>PARQUET PRO · baloncesto 25-26 → 26/27</title>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet"/>
<script src="https://cdn.tailwindcss.com"></script>
<script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<style>
  html,body,#root{height:100%;margin:0;background:#0C0F16}
  @keyframes pq-marquee{from{transform:translateX(0)}to{transform:translateX(-50%)}}
  .pq-ribbon:hover .pq-track{animation-play-state:paused}
  @keyframes pq-pulse{0%,100%{opacity:1}50%{opacity:.35}} .pq-pulse{animation:pq-pulse 1.3s infinite}
  @keyframes pq-spin{to{transform:rotate(360deg)}} .pq-spin{animation:pq-spin .9s linear infinite}
  @media (max-width:560px){ .hide-sm{display:none} }
  *:focus-visible{outline:2px solid #F4A93C;outline-offset:2px;border-radius:6px}
  @media (prefers-reduced-motion:reduce){.pq-track{animation:none!important}}
  .pq-scroll::-webkit-scrollbar{height:6px;width:6px}.pq-scroll::-webkit-scrollbar-thumb{background:#313A4D;border-radius:6px}
  a{color:inherit}
</style>
</head>
<body>
<div id="root"></div>
<script>window.SEED = __SEED_JSON__;</script>
<script type="text/babel" data-presets="react">
__JS_APP__
</script>
</body>
</html>
"""

html = HTML.replace("__SEED_JSON__", json.dumps(DATA, ensure_ascii=False)).replace("__JS_APP__", JS_APP)
(ROOT / "index.html").write_text(html, encoding="utf-8")
print("✓ index.html escrito")
