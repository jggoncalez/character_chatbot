import os

import httpx
from dotenv import load_dotenv


load_dotenv()


def _get_brapi_key() -> str:
    return os.getenv("BRAPI_KEY", "").strip()


def _brapi_401_error(ticker: str) -> dict:
    return {
        "erro": (
            f"HTTP 401 ao consultar a BRAPI para '{ticker}'. "
            "Verifique se a variável BRAPI_KEY está definida e se o token é válido."
        )
    }

def cotacao_fii(ticker: str) -> dict:
    """Busca cotação real de FII na B3 via BRAPI."""
    try:
        # garante o sufixo 11 se não tiver
        ticker = ticker.upper().strip()

        api_key = _get_brapi_key()
        if not api_key:
            return {
                "erro": (
                    "BRAPI_KEY não configurada. "
                    "Defina a variável de ambiente ou ajuste o arquivo .env."
                )
            }

        res = httpx.get(
            f"https://brapi.dev/api/quote/{ticker}",
            params={"token": api_key},
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        
        if res.status_code == 401:
            return _brapi_401_error(ticker)

        if res.status_code != 200:
            return {"erro": f"HTTP {res.status_code}: {res.text[:200]}"}
        
        data = res.json()
        
        if not data.get("results"):
            return {"erro": f"FII '{ticker}' não encontrado"}
        
        quote = data["results"][0]
        
        return {
            "ticker": ticker,
            "nome": quote.get("longName", ""),
            "preco": quote.get("regularMarketPrice"),
            "variacao_dia": quote.get("regularMarketChangePercent"),
            "abertura": quote.get("regularMarketOpen"),
            "minimo_dia": quote.get("regularMarketDayLow"),
            "maximo_dia": quote.get("regularMarketDayHigh"),
            "volume": quote.get("regularMarketVolume"),
            "dividendo_yield": quote.get("dividendYield"),
            "pvp": quote.get("priceToBook"),  # P/VP — métrica chave de FII
        }
        
    except Exception as e:
        return {"erro": str(e)}


def listar_fiis_populares() -> list[dict]:
    """Retorna cotações dos FIIs mais negociados da B3."""
    fiis = [
        "HGLG11",  # logística
        "KNRI11",  # renda
        "MXRF11",  # papel
        "XPML11",  # shoppings
        "BTLG11",  # logística
        "VISC11",  # shoppings
        "HGBS11",  # shoppings
        "IRDM11",  # papel
    ]
    
    try:
        tickers = ",".join(fiis)
        api_key = _get_brapi_key()
        if not api_key:
            return [{"erro": "BRAPI_KEY não configurada. Verifique seu arquivo .env."}]

        res = httpx.get(
            f"https://brapi.dev/api/quote/{tickers}",
            params={"token": api_key},
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if res.status_code == 401:
            return [_brapi_401_error("lista de FIIs")]

        if res.status_code != 200:
            return [{"erro": f"HTTP {res.status_code}: {res.text[:200]}"}]
        
        data = res.json()
        results = data.get("results", [])
        
        return [
            {
                "ticker": q.get("symbol"),
                "nome": q.get("longName", ""),
                "preco": q.get("regularMarketPrice"),
                "variacao_dia": q.get("regularMarketChangePercent"),
                "dividendo_yield": q.get("dividendYield"),
                "pvp": q.get("priceToBook"),
            }
            for q in results
        ]
        
    except Exception as e:
        return [{"erro": str(e)}]
    
if __name__ == "__main__":
    print(cotacao_fii('XPML11'))