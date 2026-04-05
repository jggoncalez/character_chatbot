import httpx


def buscar_docs_python(query: str) -> list[dict]:
    """Busca na documentação oficial do Python via docs.python.org."""
    try:
        res = httpx.get(
            "https://docs.python.org/3/search-index.json",
            timeout=10
        )

        # o índice é grande — filtra por query
        data = res.json()
        items = data.get("objects", [])

        resultados = []
        query_lower = query.lower()

        for item in items:
            # item: [nome, tipo, doc_name, anchor, desc]
            nome = item[0] if len(item) > 0 else ""
            desc = item[4] if len(item) > 4 else ""

            if query_lower in nome.lower() or query_lower in desc.lower():
                resultados.append({
                    "nome": nome,
                    "descricao": desc,
                    "url": f"https://docs.python.org/3/{item[2]}.html#{item[3]}"
                })

            if len(resultados) >= 5:
                break

        if not resultados:
            # fallback — linka direto pra busca
            return [{
                "nome": f"Busca por '{query}'",
                "descricao": "Veja os resultados na documentação oficial",
                "url": f"https://docs.python.org/3/search.html?q={query}"
            }]

        return resultados

    except Exception as e:
        return [{"erro": str(e)}]