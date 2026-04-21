import feedparser


def parse_rss_feeds(feeds: list[dict], max_results: int = 5) -> list[dict]:
    """Extrai notícias de uma lista de feeds RSS.

    Cada feed dict deve ter: {"nome": str, "url": str}
    Retorna lista de: {"titulo", "resumo", "fonte", "url", "publicado"}
    """
    noticias = []
    for feed_config in feeds:
        try:
            feed = feedparser.parse(feed_config["url"])
            for entry in feed.entries[:2]:
                titulo = entry.get("title", "")
                resumo = entry.get("summary", "")
                publicado = entry.get("published", "")
                noticias.append({
                    "titulo": str(titulo).strip() if titulo else "",
                    "resumo": str(resumo)[:200].strip() if resumo else "",
                    "fonte": feed_config["nome"],
                    "url": entry.get("link", ""),
                    "publicado": str(publicado)[:10] if publicado else "",
                })
        except Exception:
            continue
    return noticias[:max_results] if noticias else [{"erro": "Nenhuma notícia encontrada no momento"}]
