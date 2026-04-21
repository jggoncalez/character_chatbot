import yfinance as yf


def cotacao_acao(ticker: str) -> dict:
    """Busca cotação real via Yahoo Finance (yfinance) — sem autenticação

    Para ações brasileiras, use o formato com .SA (ex: ITUB4.SA, VALE3.SA)
    Para ações internacionais, use o ticker padrão (ex: AAPL, MSFT)
    """
    try:
        ticker = ticker.strip().upper()

        tickers_to_try = [ticker]
        if not ticker.endswith('.SA'):
            tickers_to_try.append(f"{ticker}.SA")

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
                        variacao = ((last_price - prev_price) / prev_price) * 100
                    else:
                        variacao = 0

                    return {
                        "ticker": ticker,
                        "preco": float(last_price),
                        "variacao": float(variacao),
                        "nome": info.get("longName", ticker),
                        "moeda": info.get("currency", "BRL"),
                    }
            except Exception:
                continue

        return {"erro": f"Ticker '{ticker}' não encontrado no Yahoo Finance. Tente especificar .SA para ações brasileiras (ex: PETR4.SA)"}

    except Exception as e:
        return {"erro": str(e)}