from core.tools.utils import parse_rss_feeds

_FEEDS_SAUDE = [
    {"nome": "G1 Saúde",           "url": "https://g1.globo.com/rss/g1/ciencia-e-saude/"},
    {"nome": "Ministério da Saúde", "url": "https://www.gov.br/saude/pt-br/assuntos/noticias/RSS"},
]


def noticias_saude() -> list[dict]:
    """RSS de notícias de saúde — sem chave."""
    return parse_rss_feeds(_FEEDS_SAUDE)
