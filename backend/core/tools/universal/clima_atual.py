import httpx

def clima_atual(city: str = "Sao Paulo") -> dict:
    url = f"https://wttr.in/{city}?format=j1"
    try:
        res = httpx.get(url, timeout=5)
        data = res.json()
        current = data["current_condition"][0]
        return {
            "cidade": city,
            "temperatura": current["temp_C"],
            "sensacao": current["FeelsLikeC"],
            "descricao": current["weatherDesc"][0]["value"],
            "umidade": current["humidity"]
        }
    except Exception as e:
        return {"erro": str(e)}
    
if __name__ == "__main__":
    print(clima_atual())