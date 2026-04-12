import yfinance as yf


def cotacao_acao(ticker: str) -> dict:
    """Busca cotação real via Yahoo Finance (yfinance) — sem autenticação

    Para ações brasileiras, use o formato com .SA (ex: ITUB.SA, VALE3.SA)
    Para ações internacionais, use o ticker padrão (ex: AAPL, MSFT)
    """
    try:
        # Normaliza o ticker para evitar problemas
        ticker = ticker.strip().upper()

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
                    # Pega o último preço e informações
                    info = stock.info or {}

                    # Preço de fechamento do último dia
                    last_price = hist['Close'].iloc[-1]

                    # Variação percentual em relação ao dia anterior
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
                        "moeda": info.get("currency", "")
                    }
            except Exception:
                continue

        return {"erro": f"Ticker '{ticker}' não encontrado no Yahoo Finance. Tente especificar .SA para ações brasileiras (ex: PETR4.SA)"}

    except Exception as e:
        return {"erro": str(e)}