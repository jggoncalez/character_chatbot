from core.tools.utils import parse_rss_feeds

FEEDS_EDUCACAO = [
    {"nome": "Nova Escola",  "url": "https://novaescola.org.br/feed"},
    {"nome": "MEC",          "url": "https://www.gov.br/mec/pt-br/assuntos/noticias/RSS"},
    {"nome": "G1 Educação",  "url": "https://g1.globo.com/rss/g1/educacao/"},
]


def noticias_educacao(max_results: int = 5) -> list[dict]:
    """Busca notícias recentes de educação de múltiplas fontes."""
    return parse_rss_feeds(FEEDS_EDUCACAO, max_results)


if __name__ == "__main__":
    for n in noticias_educacao():
        print(f"{n.get('titulo')} ({n.get('fonte')})\n{n.get('url')}\n")
