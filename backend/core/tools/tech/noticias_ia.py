from core.tools.utils import parse_rss_feeds

FEEDS_IA = [
    {"nome": "Hugging Face",             "url": "https://huggingface.co/blog/feed.xml"},
    {"nome": "Google AI",                "url": "https://blog.google/technology/ai/rss/"},
    {"nome": "MIT Technology Review — AI", "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed"},
]


def noticias_ia(max_results: int = 5) -> list[dict]:
    """Últimas notícias de IA de múltiplas fontes."""
    return parse_rss_feeds(FEEDS_IA, max_results)
