import concurrent.futures
import yfinance as yf


def cotacao_fii(ticker: str) -> dict:
    """Busca cotação real de FII na B3 via Yahoo Finance — sem autenticação"""
    try:
        ticker = ticker.upper().strip()

        # Define tickers a serem tentados — .SA tem prioridade pois FIIs são sempre brasileiros
        if ticker.endswith('.SA'):
            tickers_to_try = [ticker]
        else:
            tickers_to_try = [f"{ticker}.SA", ticker]

        for attempt_ticker in tickers_to_try:
            try:
                stock = yf.Ticker(attempt_ticker)
                hist = stock.history(period="5d")

                if not hist.empty:
                    # Isola o .info — se falhar (404), não perde o dado do history
                    try:
                        info = stock.info or {}
                    except Exception:
                        info = {}

                    last_price = hist['Close'].iloc[-1]

                    if len(hist) > 1:
                        prev_price = hist['Close'].iloc[-2]
                        variacao_dia = ((last_price - prev_price) / prev_price) * 100
                    else:
                        variacao_dia = 0

                    return {
                        "ticker": ticker,
                        "nome": info.get("longName", ""),
                        "preco": float(last_price),
                        "variacao_dia": float(variacao_dia),
                        "abertura": float(info.get("open", 0)) if info.get("open") else None,
                        "minimo_dia": float(hist['Low'].iloc[-1]) if len(hist) > 0 else None,
                        "maximo_dia": float(hist['High'].iloc[-1]) if len(hist) > 0 else None,
                        "volume": int(info.get("volume", 0)) if info.get("volume") else None,
                        "dividendo_yield": float(info.get("dividendYield", 0)) if info.get("dividendYield") else None,
                        "pvp": float(info.get("priceToBook", 0)) if info.get("priceToBook") else None,
                    }
            except Exception:
                continue

        return {"erro": f"FII '{ticker}' não encontrado. Tente especificar .SA (ex: HGLG11.SA)"}

    except Exception as e:
        return {"erro": str(e)}


def listar_fiis_populares() -> list[dict]:
    """Lista FIIs populares brasileiros com suas cotações em paralelo."""
    fiis = ["HGLG11", "MXRF11", "XPML11", "BTLG11"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        resultados = list(executor.map(cotacao_fii, fiis))
    validos = [r for r in resultados if "erro" not in r]
    return validos if validos else [{"erro": "Nenhuma cotação disponível"}]
