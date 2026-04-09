import feedparser

def buscar_noticias_financeiras() -> list[dict]:
    """RSS do InfoMoney — sem autenticação"""
    feed = feedparser.parse(
        "https://www.infomoney.com.br/feed/"
    )
    return [
        {"titulo": e.title, "link": e.link}
        for e in feed.entries[:5]
    ]

if __name__ == "__main__":
    noticias = buscar_noticias_financeiras()
    for n in noticias:
        print(f"{n['titulo']}\n{n['link']}\n")