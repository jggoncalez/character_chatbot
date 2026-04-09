import httpx

def buscar_anvisa(query: str) -> list[dict]:
    """
    Busca medicamentos e produtos na base da ANVISA.
    API pública — sem chave.
    """
    try:
        res = httpx.get(
            "https://consultas.anvisa.gov.br/api/consulta/medicamentos/",
            params={
                "count": 5,
                "filter[nomeProduto]": query
            },
            headers={
                "Accept": "application/json",
                "User-Agent": "character_chatbot/1.0"
            },
            timeout=10
        )

        if res.status_code != 200:
            return [{"erro": f"ANVISA retornou HTTP {res.status_code}"}]

        data = res.json()
        content = data.get("content", [])

        if not content:
            return [{"erro": f"Nenhum medicamento encontrado para '{query}'"}]

        return [
            {
                "nome": item.get("nomeProduto", ""),
                "laboratorio": item.get("nomeTitular", ""),
                "categoria": item.get("categoriaProduto", ""),
                "situacao": item.get("situacaoRegistro", ""),
                "vencimento_registro": item.get("dataVencimentoRegistro", ""),
                "classe_terapeutica": item.get("classeTerapeutica", ""),
            }
            for item in content
        ]

    except Exception as e:
        return [{"erro": str(e)}]

