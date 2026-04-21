from core.tools.medical.buscar_anvisa import _buscar_medicamentos_anvisa


def buscar_remedios(medicamento: str) -> list[dict]:
    """
    Busca medicamentos com registro válido (situação V) na ANVISA.
    API pública — sem chave.
    """
    items = _buscar_medicamentos_anvisa(
        medicamento,
        params_extra={"filter[situacaoRegistro]": "V"},
    )
    if items and "erro" in items[0]:
        return items
    return [
        {
            "nome": item.get("nomeProduto", ""),
            "principio_ativo": item.get("principioAtivo", ""),
            "laboratorio": item.get("nomeTitular", ""),
            "classe_terapeutica": item.get("classeTerapeutica", ""),
            "tipo": item.get("tipoProduto", ""),
            "situacao": item.get("situacaoRegistro", ""),
        }
        for item in items
    ]
