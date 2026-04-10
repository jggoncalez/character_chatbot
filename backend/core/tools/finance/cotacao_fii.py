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
    fiis = ["HGLG11", "MXRF11", "XPML11", "BTLG11"]  # reduz pra 4
    resultados = []
    
    for ticker in fiis:
        resultado = cotacao_fii(ticker)  # já existe, chama 1 por vez
        if "erro" not in resultado:
            resultados.append(resultado)
    
    return resultados if resultados else [
        {"erro": "Nenhuma cotação disponível"}
    ]