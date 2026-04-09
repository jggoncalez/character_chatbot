import httpx

def buscar_pubmed(query: str, max_results: int = 3) -> list[dict]:
    """
    Busca artigos médicos no PubMed.
    Usa a API E-utilities do NCBI — pública, sem chave.
    """
    try:
        # passo 1 — busca os IDs dos artigos
        search = httpx.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
            params={
                "db": "pubmed",
                "term": query,
                "retmax": max_results,
                "sort": "date",
                "retmode": "json"
            },
            timeout=10
        )

        ids = search.json().get("esearchresult", {}).get("idlist", [])

        if not ids:
            return [{"erro": f"Nenhum artigo encontrado para '{query}'"}]

        # passo 2 — busca os detalhes dos artigos
        summary = httpx.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
            params={
                "db": "pubmed",
                "id": ",".join(ids),
                "retmode": "json"
            },
            timeout=10
        )

        data = summary.json().get("result", {})

        artigos = []
        for pid in ids:
            item = data.get(pid, {})
            if not item:
                continue

            # autores
            authors = [
                a.get("name", "")
                for a in item.get("authors", [])[:3]
            ]

            artigos.append({
                "titulo": item.get("title", "").strip(),
                "autores": authors,
                "journal": item.get("source", ""),
                "publicado": item.get("pubdate", ""),
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pid}/"
            })

        return artigos

    except Exception as e:
        return [{"erro": str(e)}]
