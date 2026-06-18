import feedparser, os, re
from urllib.parse import quote, urlparse
import pandas as pd
from datetime import datetime, timezone

#keywords e eixos — editais sobre IA, incentivo a publicações e memória no Brasil
EIXOS = {
    "Inteligência Artificial": [
        '"edital" "inteligência artificial"',
        '"chamada pública" "inteligência artificial"',
        '"edital" "IA" pesquisa',
        'fomento "inteligência artificial" edital',
        '"chamada" projetos "inteligência artificial"',
    ],
    "Incentivo a Publicações": [
        '"edital" "incentivo à publicação"',
        '"edital" "publicação científica"',
        '"edital" apoio à publicação',
        '"edital" fomento publicação livros',
        '"chamada pública" "publicação acadêmica"',
    ],
    "Memória": [
        '"edital" "memória"',
        '"edital" "preservação da memória"',
        '"edital" patrimônio "memória"',
        '"chamada pública" "memória" cultural',
        '"edital" "memória" acervo',
    ],
    "Preservação de Acervo": [
        '"curso" "preservação de acervo"',
        '"curso" "conservação de acervo"',
        '"capacitação" "preservação de acervo"',
        '"oficina" "conservação preventiva"',
        '"formação" "preservação de acervos"',
        # prioridade: Rio de Janeiro e online
        '"curso" "preservação de acervo" "Rio de Janeiro"',
        '"curso online" "preservação de acervo"',
        '"curso" "conservação de acervo" online',
        '"curso" "conservação de acervo" "Rio de Janeiro"',
    ],
}

#filtros
ANO_MINIMO = 2026   

#bloqueio de estrangeiros em pt
FONTES_BLOQUEADAS = [
    # Portugal
    "publico.pt", "observador.pt", "expresso.pt", "sapo.pt", "rtp.pt",
    "dn.pt", "jn.pt", "cmjornal", "eco.sapo", "jornaldenegocios",
    "tsf.pt", "sicnoticias", "noticiasaominuto",
]

def eh_bloqueada(fonte, link):
    alvo = (fonte or "").lower() + " " + (link or "").lower()
    try:
        dom = urlparse(link or "").netloc.lower()
        alvo += " " + dom
    except Exception:
        pass
    return any(b in alvo for b in FONTES_BLOQUEADAS)

def ano_da_data(s):
    if not s:
        return None
    try:
        return pd.to_datetime(s, errors="coerce").year
    except Exception:
        return None

arquivo = "dados/noticias.csv"

linhas = []
descartadas_ano = 0
descartadas_fonte = 0

for eixo, keywords in EIXOS.items():
    for kw in keywords:
        url = f"https://news.google.com/rss/search?q={quote(kw)}&hl=pt-BR&gl=BR&ceid=BR:pt"
        for e in feedparser.parse(url).entries:
            fonte = e.get("source", {}).get("title", "")
            link = e.link
            data_pub = e.get("published", "")

            #filtro de origem
            if eh_bloqueada(fonte, link):
                descartadas_fonte += 1
                continue

            #filtro de ano
            ano = ano_da_data(data_pub)
            if ano is not None and ano < ANO_MINIMO:
                descartadas_ano += 1
                continue

            linhas.append({
                "eixo": eixo,
                "keyword": kw,
                "titulo": e.title,
                "data_pub": data_pub,
                "fonte": fonte,
                "link": link,
                "coletado_em": datetime.now(timezone.utc).isoformat(),
            })

novo = pd.DataFrame(linhas)

if os.path.exists(arquivo):
    antigo = pd.read_csv(arquivo)
    df = pd.concat([antigo, novo]).drop_duplicates(subset="link", keep="first")

    if "data_pub" in df.columns:
        df = df[df["data_pub"].apply(lambda s: (ano_da_data(s) is None) or (ano_da_data(s) >= ANO_MINIMO))]
    if "fonte" in df.columns and "link" in df.columns:
        df = df[~df.apply(lambda r: eh_bloqueada(r.get("fonte",""), r.get("link","")), axis=1)]
else:
    df = novo.drop_duplicates(subset="link")

os.makedirs("dados", exist_ok=True)
df.to_csv(arquivo, index=False)
print(f"{len(novo)} novas | {len(df)} no total | descartadas: {descartadas_ano} por ano, {descartadas_fonte} por fonte")
