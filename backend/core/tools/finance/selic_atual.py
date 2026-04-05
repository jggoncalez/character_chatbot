import httpx

def selic_atual() -> dict:
    """API pública do Banco Central"""
    try:
        url = (
            "https://api.bcb.gov.br/dados/serie/"
            "bcdata.sgs.11/dados/ultimos/1?formato=json"
        )
        res = httpx.get(url, timeout=5)
        dados = res.json()[0]
        return {"selic": dados["valor"], "data": dados["data"]}
    except Exception as e:
        return {"erro": str(e)}
    
if __name__ == "__main__":
    print(selic_atual())