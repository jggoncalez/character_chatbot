import httpx

def selic_atual() -> dict:
    """Taxa Selic meta via API pública do Banco Central."""
    try:
        # série 432 = Selic meta anual — a que todo mundo conhece
        res = httpx.get(
            "https://api.bcb.gov.br/dados/serie/"
            "bcdata.sgs.432/dados/ultimos/1?formato=json",
            timeout=5
        )

        if res.status_code != 200:
            return {"erro": f"HTTP {res.status_code}"}

        dados = res.json()
        if not dados:
            return {"erro": "Nenhum dado retornado"}

        ultimo = dados[-1]
        return {
            "selic_meta_anual": ultimo.get("valor"),
            "referencia": ultimo.get("data"),
            "unidade": "% ao ano"
        }

    except Exception as e:
        return {"erro": str(e)}
    
if __name__ == "__main__":
    print(selic_atual())