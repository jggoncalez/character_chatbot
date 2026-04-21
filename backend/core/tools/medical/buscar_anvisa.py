import httpx

_ANVISA_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "character_chatbot/1.0"
}


def _buscar_medicamentos_anvisa(termo: str, params_extra: dict | None = None) -> list[dict]:
    """Chamada base à API da ANVISA. Retorna items brutos ou lista com chave 'erro'."""
    params: dict = {"count": 5, "filter[nomeProduto]": termo}
    if params_extra:
        params.update(params_extra)
    try:
        res = httpx.get(
            "https://consultas.anvisa.gov.br/api/consulta/medicamentos/",
            params=params,
            headers=_ANVISA_HEADERS,
            timeout=10,
        )
        if res.status_code != 200:
            return [{"erro": f"ANVISA retornou HTTP {res.status_code}"}]
        content = res.json().get("content", [])
        if not content:
            return [{"erro": f"Nenhum medicamento encontrado para '{termo}'"}]
        return content
    except Exception as e:
        return [{"erro": str(e)}]


def buscar_anvisa(query: str) -> list[dict]:
    """
    Busca medicamentos e produtos na base da ANVISA.
    API pública — sem chave.
    """
    items = _buscar_medicamentos_anvisa(query)
    if items and "erro" in items[0]:
        return items
    return [
        {
            "nome": item.get("nomeProduto", ""),
            "laboratorio": item.get("nomeTitular", ""),
            "categoria": item.get("categoriaProduto", ""),
            "situacao": item.get("situacaoRegistro", ""),
            "vencimento_registro": item.get("dataVencimentoRegistro", ""),
            "classe_terapeutica": item.get("classeTerapeutica", ""),
        }
        for item in items
    ]
