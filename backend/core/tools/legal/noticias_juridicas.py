import feedparser

def noticias_juridicas() -> list[dict]:
    """RSS de notícias jurídicas — sem chave."""
    feeds = [
        {
            "nome": "Conjur",
            "url": "https://www.conjur.com.br/rss.xml"
        },
        {
            "nome": "STJ Notícias",
            "url": "https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias/RSS.xml"
        }
    ]

    noticias = []
    for f in feeds:
        try:
            feed = feedparser.parse(f["url"])
            for entry in feed.entries[:2]:
                titulo = entry.get("title", "")
                resumo = entry.get("summary", "")
                publicado = entry.get("published", "")
                
                noticias.append({
                    "titulo": titulo.strip() if isinstance(titulo, str) else "",
                    "resumo": resumo[:200].strip() if isinstance(resumo, str) else "",
                    "fonte": f["nome"],
                    "url": entry.get("link", ""),
                    "publicado": publicado[:10] if isinstance(publicado, str) else ""
                })
        except Exception:
            continue

    return noticias[:5] if noticias else [
        {"erro": "Nenhuma notícia jurídica disponível"}
    ]