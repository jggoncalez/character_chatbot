from core.tools.utils import parse_rss_feeds

FEEDS_VAREJO = [
    {"nome": "Supermercado Moderno", "url": "https://www.sm.com.br/feed"},
    {"nome": "ABRAS",                "url": "https://www.abras.com.br/feed"},
    {"nome": "Mercado & Consumo",    "url": "https://mercadoeconsumo.com.br/feed/"},
]


def buscar_noticias_varejo(max_results: int = 5) -> list[dict]:
    """Notícias do setor supermercadista e varejo alimentar via RSS — sem chave."""
    return parse_rss_feeds(FEEDS_VAREJO, max_results)
