import yfinance as yf


def cotacao_fii(ticker: str) -> dict:
    """Busca cotação real de FII na B3 via Yahoo Finance — sem autenticação"""
    try:
        ticker = ticker.upper().strip()

        # Define tickers a serem tentados
        tickers_to_try = [ticker]
        if not ticker.endswith('.SA'):
            tickers_to_try.append(f"{ticker}.SA")

        # Tenta cada variação de ticker
        for attempt_ticker in tickers_to_try:
            try:
                stock = yf.Ticker(attempt_ticker)
                hist = stock.history(period="5d")

                if not hist.empty:
                    info = stock.info or {}

                    # Preço de fechamento do último dia
                    last_price = hist['Close'].iloc[-1]

                    # Variação percentual em relação ao dia anterior
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
    """Lista FIIs populares brasileiros com suas cotações"""
    fiis = ["HGLG11", "MXRF11", "XPML11", "BTLG11"]
    resultados = []

    for ticker in fiis:
        resultado = cotacao_fii(ticker)
        if "erro" not in resultado:
            resultados.append(resultado)

    return resultados if resultados else [
        {"erro": "Nenhuma cotação disponível"}
    ]