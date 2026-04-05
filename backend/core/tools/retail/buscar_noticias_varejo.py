import feedparser

FEEDS_VAREJO = [
    {
        "nome": "Supermercado Moderno",
        "url": "https://www.sm.com.br/feed"
    },
    {
        "nome": "ABRAS",
        "url": "https://www.abras.com.br/feed"
    },
    {
        "nome": "Mercado & Consumo",
        "url": "https://mercadoeconsumo.com.br/feed/"
    }
]

def buscar_noticias_varejo(max_results: int = 5) -> list[dict]:
    """
    Notícias do setor supermercadista e varejo alimentar.
    Múltiplas fontes via RSS — sem chave.
    """
    noticias = []

    for feed_config in FEEDS_VAREJO:
        try:
            feed = feedparser.parse(feed_config["url"])

            for entry in feed.entries[:2]:
                titulo = entry.get("title", "")
                resumo = entry.get("summary", "")
                publicado = entry.get("published", "")
                
                titulo = titulo.strip() if isinstance(titulo, str) else ""
                resumo = (resumo.strip() if isinstance(resumo, str) else "")[:200]
                publicado = (publicado[:10] if isinstance(publicado, str) else "")
                
                noticias.append({
                    "titulo": titulo,
                    "resumo": resumo,
                    "fonte": feed_config["nome"],
                    "url": entry.get("link", ""),
                    "publicado": publicado
                })

        except Exception:
            continue

    return noticias[:max_results] if noticias else [
        {"erro": "Nenhuma notícia de varejo disponível no momento"}
    ]