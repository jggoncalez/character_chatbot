from core.tools.utils import parse_rss_feeds

_FEEDS_JURIDICOS = [
    {"nome": "Conjur",       "url": "https://www.conjur.com.br/rss.xml"},
    {"nome": "STJ Notícias", "url": "https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias/RSS.xml"},
]


def noticias_juridicas() -> list[dict]:
    """RSS de notícias jurídicas — sem chave."""
    return parse_rss_feeds(_FEEDS_JURIDICOS)
