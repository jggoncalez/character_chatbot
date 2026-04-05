import os

import httpx
from dotenv import load_dotenv

load_dotenv()

def _get_brapi_key() -> str:
    return os.getenv("BRAPI_KEY", "").strip()

def cotacao_acao(ticker: str) -> dict:
    """Busca cotação real na BRAPI — gratuita, dados da B3"""
    try:
        api_key = _get_brapi_key()
        if not api_key:
            return {"erro": "BRAPI_KEY não configurada. Verifique seu arquivo .env."}

        url = f"https://brapi.dev/api/quote/{ticker}"
        res = httpx.get(url, params={"token": api_key}, timeout=5)

        if res.status_code == 401:
            return {"erro": f"HTTP 401 ao consultar a BRAPI para '{ticker}'. Verifique a BRAPI_KEY."}

        if res.status_code != 200:
            return {"erro": f"HTTP {res.status_code}: {res.text[:200]}"}

        data = res.json()
        quote = data["results"][0]
        return {
            "ticker": ticker,
            "preco": quote["regularMarketPrice"],
            "variacao": quote["regularMarketChangePercent"],
            "nome": quote["longName"]
        }
    except Exception as e:
        return {"erro": str(e)}

if __name__ == "__main__":
    print(cotacao_acao("ITUB4"))