
import feedparser

FEEDS_EDUCACAO = [
    {
        "nome": "Nova Escola",
        "url": "https://novaescola.org.br/feed"
    },
    {
        "nome": "MEC",
        "url": "https://www.gov.br/mec/pt-br/assuntos/noticias/RSS"
    },
    {
        "nome": "G1 Educação",
        "url": "https://g1.globo.com/rss/g1/educacao/"
    }
]

def noticias_educacao(max_results: int = 5) -> list[dict]:
    """Busca notícias recentes de educação de múltiplas fontes."""
    noticias = []

    for feed_config in FEEDS_EDUCACAO:
        try:
            feed = feedparser.parse(feed_config["url"])

            for entry in feed.entries[:2]:  # 2 de cada fonte
                # data de publicação
                published = ""
                if hasattr(entry, "published"):
                    published = entry.published[:10]

                title = entry.get("title", "")
                if isinstance(title, list):
                    title = title[0] if title else ""
                title = str(title).strip()

                summary = entry.get("summary", "")
                if isinstance(summary, list):
                    summary = summary[0] if summary else ""
                summary = str(summary)[:200].strip()

                noticias.append({
                    "titulo": title,
                    "resumo": summary,
                    "fonte": feed_config["nome"],
                    "url": entry.get("link", ""),
                    "publicado": published
                })

        except Exception:
            continue  # se um feed falhar, continua pros outros

    # ordena por data e limita
    return noticias[:max_results] if noticias else [
        {"erro": "Nenhuma notícia encontrada no momento"}
    ]
    
if __name__ == "__main__":
    noticias = noticias_educacao()
    for n in noticias:
        print(f"{n['titulo']} ({n['fonte']})\n{n['url']}\nPublicado em: {n['publicado']}\nResumo: {n['resumo']}\n")