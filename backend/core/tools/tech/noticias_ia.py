import feedparser

FEEDS_IA = [
    {
        "nome": "Hugging Face",
        "url": "https://huggingface.co/blog/feed.xml"
    },
    {
        "nome": "Google AI",
        "url": "https://blog.google/technology/ai/rss/"
    },
    {
        "nome": "MIT Technology Review — AI",
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed"
    },
]

def noticias_ia(max_results: int = 5) -> list[dict]:
    """Últimas notícias de IA de múltiplas fontes."""
    noticias = []

    for feed_config in FEEDS_IA:
        try:
            feed = feedparser.parse(feed_config["url"])

            for entry in feed.entries[:2]:
                titulo = entry.get("title", "")
                resumo = entry.get("summary", "")
                publicado = entry.get("published", "")
                
                noticias.append({
                    "titulo": titulo.strip() if isinstance(titulo, str) else "",
                    "resumo": resumo[:250].strip() if isinstance(resumo, str) else "",
                    "fonte": feed_config["nome"],
                    "url": entry.get("link", ""),
                    "publicado": publicado[:10] if isinstance(publicado, str) else ""
                })

        except Exception:
            continue

    return noticias[:max_results] if noticias else [
        {"erro": "Nenhuma notícia encontrada no momento"}
    ]

