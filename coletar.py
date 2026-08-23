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
        # subgrupo "Curso de Preservação de Acervo" (nome e cor próprios no site)
        '"curso" "preservação de acervo"',
        '"curso" "conservação de acervo"',
        '"capacitação" "preservação de acervo"',
        '"oficina" "conservação preventiva"',
        '"formação" "preservação de acervos"',
        # prioridade do subgrupo: Rio de Janeiro e online
        '"curso" "preservação de acervo" "Rio de Janeiro"',
        '"curso online" "preservação de acervo"',
        '"curso" "conservação de acervo" online',
        '"curso" "conservação de acervo" "Rio de Janeiro"',
    ],
}

#filtros
MESES_VALIDADE = 6

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

DATA_CORTE = pd.Timestamp.now(tz="UTC") - pd.DateOffset(months=MESES_VALIDADE)

def esta_expirado(data_str):
    if not data_str:
        return False
    try:
        data = pd.to_datetime(data_str, utc=True)
        return data < DATA_CORTE
    except Exception:
        return False

arquivo = "dados/noticias.csv"

linhas = []
descartadas_antigas = 0
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

            #filtro de idade
            if esta_expirado(data_pub):
                descartadas_antigas += 1
                continue

            titulo = e.title or ""
            titulo_lower = titulo.lower()

            # Classificador de Agência
            agencia = ""
            if re.search(r'\b(cnpq)\b', titulo_lower): agencia = "CNPq"
            elif re.search(r'\b(capes)\b', titulo_lower): agencia = "CAPES"
            elif re.search(r'\b(faperj)\b', titulo_lower): agencia = "FAPERJ"
            elif re.search(r'\b(secti)\b', titulo_lower): agencia = "SECTI"
            elif re.search(r'\b(fapesp|fapemig|fapergs|fap|fapeal|fapeam|fapeg|fapema|fapemat|fapes|fapesb|fapesc|fapespa|fapesq|fapi|fapt|funcap)\b', titulo_lower): agencia = "FAP (Estaduais)"
            elif re.search(r'\b(finep)\b', titulo_lower): agencia = "Finep"
            elif re.search(r'\b(bndes)\b', titulo_lower): agencia = "BNDES"
            elif re.search(r'\b(minc|cultura|funarte|lei paulo gustavo|lei aldir blanc)\b', titulo_lower): agencia = "Cultura / MinC"
            elif re.search(r'\b(mcti)\b', titulo_lower): agencia = "MCTI"

            # Classificador de Tipo
            tipo = ""
            if re.search(r'\b(bolsa|bolsas)\b', titulo_lower): tipo = "Bolsa"
            elif re.search(r'\b(prêmio|premio)\b', titulo_lower): tipo = "Prêmio"
            elif re.search(r'\b(curso|cursos|capacitação|oficina|treinamento)\b', titulo_lower): tipo = "Curso"
            elif re.search(r'\b(fomento|financiamento|subvenção|patrocínio)\b', titulo_lower): tipo = "Financiamento"

            linhas.append({
                "eixo": eixo,
                "keyword": kw,
                "titulo": titulo,
                "data_pub": data_pub,
                "fonte": fonte,
                "link": link,
                "agencia": agencia,
                "tipo_edital": tipo,
                "coletado_em": datetime.now(timezone.utc).isoformat(),
            })

novo = pd.DataFrame(linhas)

def classificar_agencia(titulo):
    t = str(titulo).lower()
    if re.search(r'\b(cnpq)\b', t): return "CNPq"
    if re.search(r'\b(capes)\b', t): return "CAPES"
    if re.search(r'\b(faperj)\b', t): return "FAPERJ"
    if re.search(r'\b(secti)\b', t): return "SECTI"
    if re.search(r'\b(fapesp|fapemig|fapergs|fap|fapeal|fapeam|fapeg|fapema|fapemat|fapes|fapesb|fapesc|fapespa|fapesq|fapi|fapt|funcap)\b', t): return "FAP (Estaduais)"
    if re.search(r'\b(finep)\b', t): return "Finep"
    if re.search(r'\b(bndes)\b', t): return "BNDES"
    if re.search(r'\b(minc|cultura|funarte|lei paulo gustavo|lei aldir blanc)\b', t): return "Cultura / MinC"
    if re.search(r'\b(mcti)\b', t): return "MCTI"
    return ""

def classificar_tipo(titulo):
    t = str(titulo).lower()
    if re.search(r'\b(bolsa|bolsas)\b', t): return "Bolsa"
    if re.search(r'\b(prêmio|premio)\b', t): return "Prêmio"
    if re.search(r'\b(curso|cursos|capacitação|oficina|treinamento)\b', t): return "Curso"
    if re.search(r'\b(fomento|financiamento|subvenção|patrocínio)\b', t): return "Financiamento"
    return ""

if os.path.exists(arquivo):
    antigo = pd.read_csv(arquivo)
    df = pd.concat([antigo, novo]).drop_duplicates(subset="link", keep="first")
    
    # Reclassificar tudo retroativamente
    df["agencia"] = df["titulo"].apply(classificar_agencia)
    df["tipo_edital"] = df["titulo"].apply(classificar_tipo)

    if "data_pub" in df.columns:
        df = df[~df["data_pub"].apply(esta_expirado)]
    if "fonte" in df.columns and "link" in df.columns:
        df = df[~df.apply(lambda r: eh_bloqueada(r.get("fonte",""), r.get("link","")), axis=1)]
else:
    df = novo.drop_duplicates(subset="link")

os.makedirs("dados", exist_ok=True)
df.to_csv(arquivo, index=False)
print(f"{len(novo)} novas | {len(df)} no total | descartadas: {descartadas_antigas} antigas, {descartadas_fonte} por fonte")
