import feedparser

def kernel_changelog() -> list[dict]:
    """Últimas versões estáveis do Kernel Linux via RSS."""
    try:
        feed = feedparser.parse("https://www.kernel.org/feeds/kdist.xml")

        return [
            {
                "versao": (e.get("title") or ""),
                "data": (e.get("published") or "")[:10],
                "url": e.get("link", "")
            }
            for e in feed.entries[:5]
        ]

    except Exception as e:
        return [{"erro": str(e)}]
