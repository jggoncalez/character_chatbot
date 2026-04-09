import httpx

def trending_github(language: str = "") -> list[dict]:
    """
    Repositórios em alta no GitHub.
    GitHub não tem API oficial pra trending —
    usa a API de busca com filtros de estrelas e data.
    """
    try:
        from datetime import datetime, timedelta

        # repos criados nos últimos 7 dias com muitas estrelas
        data_limite = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        query = f"created:>{data_limite} stars:>50"
        if language:
            query += f" language:{language}"

        res = httpx.get(
            "https://api.github.com/search/repositories",
            params={
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": 5
            },
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "character_chatbot/1.0"
            },
            timeout=10
        )

        if res.status_code == 403:
            return [{"erro": "Rate limit do GitHub atingido. Tente em alguns minutos."}]

        data = res.json()

        return [
            {
                "nome": r.get("full_name", ""),
                "descricao": r.get("description", ""),
                "linguagem": r.get("language", ""),
                "estrelas": r.get("stargazers_count", 0),
                "url": r.get("html_url", "")
            }
            for r in data.get("items", [])
        ]

    except Exception as e:
        return [{"erro": str(e)}]