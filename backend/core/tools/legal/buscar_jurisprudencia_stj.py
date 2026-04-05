import httpx

def buscar_jurisprudencia(query: str) -> list[dict]:
    """
    Busca jurisprudência no STJ via pesquisa pública.
    Sem chave.
    """
    try:
        res = httpx.get(
            "https://scon.stj.jus.br/SCON/pesquisar.jsp",
            params={
                "b": "ACOR",
                "p": "true",
                "l": 5,
                "i": 1,
                "operador": "e",
                "thesaurus": "JURIDICO",
                "q": query
            },
            headers={
                "User-Agent": "character_chatbot/1.0"
            },
            timeout=10,
            follow_redirects=True
        )

        # STJ não tem API JSON — retorna HTML
        # extrai o que for possível ou aponta pra URL
        if res.status_code == 200:
            return [
                {
                    "info": (
                        f"Resultados para '{query}' no STJ. "
                        "Acesse o link para ver os acórdãos completos."
                    ),
                    "url": (
                        f"https://scon.stj.jus.br/SCON/pesquisar.jsp"
                        f"?b=ACOR&q={query}&operador=e&thesaurus=JURIDICO"
                    )
                }
            ]

        return [{"erro": f"STJ retornou HTTP {res.status_code}"}]

    except Exception as e:
        return [{"erro": str(e)}]
