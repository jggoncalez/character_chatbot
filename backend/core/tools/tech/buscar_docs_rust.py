import httpx

def buscar_docs_rust(query: str) -> list[dict]:
    """Busca na documentação do Rust via docs.rs e doc.rust-lang.org."""
    try:
        # docs.rs tem API de busca pra crates
        res = httpx.get(
            "https://docs.rs/search",
            params={"query": query},
            timeout=10,
            follow_redirects=True
        )

        # fallback estruturado — docs.rs não tem API JSON pública simples
        # usa a busca do crates.io que tem API REST
        crates = httpx.get(
            "https://crates.io/api/v1/crates",
            params={
                "q": query,
                "per_page": 5,
                "sort": "relevance"
            },
            headers={"User-Agent": "character_chatbot/1.0"},
            timeout=10
        )

        data = crates.json()
        resultados = []

        for crate in data.get("crates", []):
            resultados.append({
                "nome": crate.get("name", ""),
                "descricao": crate.get("description", ""),
                "versao": crate.get("newest_version", ""),
                "downloads": crate.get("downloads", 0),
                "url": f"https://docs.rs/{crate.get('name', '')}"
            })

        if not resultados:
            return [{
                "nome": f"Busca por '{query}'",
                "descricao": "Veja os resultados na documentação oficial",
                "url": f"https://doc.rust-lang.org/std/?search={query}"
            }]

        return resultados

    except Exception as e:
        return [{"erro": str(e)}]

