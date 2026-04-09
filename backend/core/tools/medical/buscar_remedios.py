import httpx

def buscar_remedios(medicamento: str) -> list[dict]:
    """
    Busca preço e disponibilidade de medicamentos
    via API pública da CMED (Câmara de Regulação do Mercado de Medicamentos).
    """
    try:
        # CMED disponibiliza tabela de preços — usa o endpoint de consulta
        res = httpx.get(
            "https://consultas.anvisa.gov.br/api/consulta/medicamentos/",
            params={
                "count": 5,
                "filter[nomeProduto]": medicamento,
                "filter[situacaoRegistro]": "V"  # V = Válido
            },
            headers={
                "Accept": "application/json",
                "User-Agent": "character_chatbot/1.0"
            },
            timeout=10
        )

        if res.status_code != 200:
            return [{"erro": f"HTTP {res.status_code}"}]

        content = res.json().get("content", [])

        if not content:
            return [{"erro": f"Medicamento '{medicamento}' não encontrado"}]

        return [
            {
                "nome": item.get("nomeProduto", ""),
                "principio_ativo": item.get("principioAtivo", ""),
                "laboratorio": item.get("nomeTitular", ""),
                "classe_terapeutica": item.get("classeTerapeutica", ""),
                "tipo": item.get("tipoProduto", ""),
                "situacao": item.get("situacaoRegistro", ""),
            }
            for item in content
        ]

    except Exception as e:
        return [{"erro": str(e)}]
