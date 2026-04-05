import httpx


def ipca_atual() -> dict:
    """
    Retorna o IPCA mais recente via API pública do Banco Central.
    Série 433 = IPCA mensal.
    Sem chave, sem cadastro.
    """
    try:
        res = httpx.get(
            "https://api.bcb.gov.br/dados/serie/"
            "bcdata.sgs.433/dados/ultimos/3?formato=json",
            timeout=5
        )

        if res.status_code != 200:
            return {"erro": f"HTTP {res.status_code}"}

        dados = res.json()

        if not dados:
            return {"erro": "Nenhum dado retornado"}

        # último registro = mais recente
        ultimo = dados[-1]

        return {
            "ipca_mensal": ultimo.get("valor"),
            "referencia": ultimo.get("data"),
            "ultimos_3_meses": [
                {
                    "mes": d.get("data"),
                    "valor": d.get("valor")
                }
                for d in dados
            ]
        }

    except Exception as e:
        return {"erro": str(e)}
