import httpx
from urllib.parse import quote

def buscar_wikipedia(query: str) -> dict:
    """Busca um artigo na Wikipedia em português."""
    try:
        # Busca o título mais relevante
        search_url = "https://pt.wikipedia.org/api/rest_v1/page/summary/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        # Primeiro normaliza o termo
        search = httpx.get(
            "https://pt.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "srlimit": 1
            },
            headers=headers,
            timeout=5
        )
        
        if search.status_code != 200:
            return {"erro": f"Erro na busca: status {search.status_code}"}
        
        results = search.json()
        hits = results["query"]["search"]
        
        if not hits:
            return {"erro": f"Nenhum resultado para '{query}'"}
        
        # Pega o título do primeiro resultado
        title = hits[0]["title"]
        
        # Busca o resumo do artigo
        summary = httpx.get(
            f"{search_url}{quote(title)}",
            headers=headers,
            timeout=5
        )
        
        if summary.status_code != 200:
            return {"erro": f"Erro ao buscar resumo: status {summary.status_code}"}
        
        data = summary.json()
        
        return {
            "titulo": data.get("title"),
            "resumo": data.get("extract"),
            "url": data.get("content_urls", {})
                       .get("desktop", {})
                       .get("page", "")
        }
        
    except Exception as e:
        return {"erro": str(e)}

if __name__ == "__main__":
    print(buscar_wikipedia("Inuyasha"))