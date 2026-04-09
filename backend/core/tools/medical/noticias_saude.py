import feedparser
    
def noticias_saude() -> list[dict]:
    """RSS de notícias de saúde — bônus, sem chave."""

    feeds = [
        {
            "nome": "G1 Saúde",
            "url": "https://g1.globo.com/rss/g1/ciencia-e-saude/"
        },
        {
            "nome": "Ministério da Saúde",
            "url": "https://www.gov.br/saude/pt-br/assuntos/noticias/RSS"
        }
    ]

    noticias = []
    for f in feeds:
        try:
            feed = feedparser.parse(f["url"])
            for entry in feed.entries[:2]:
                noticias.append({
                    "titulo": str(entry.get("title", "")).strip(),
                    "resumo": str(entry.get("summary", ""))[:200].strip(),
                    "fonte": f["nome"],
                    "url": entry.get("link", ""),
                    "publicado": str(entry.get("published", ""))[:10]
                })
        except Exception:
            continue

    return noticias[:5] if noticias else [
        {"erro": "Nenhuma notícia disponível no momento"}
    ]