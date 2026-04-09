import httpx

def buscar_legislacao_brasileira(query: str) -> list[dict]:
    """
    Busca leis e normas no Portal da Legislação do Planalto.
    API pública — sem chave.
    """
    try:
        res = httpx.get(
            "https://www4.planalto.gov.br/legislacao/portal-legis/legislacao-1/leis-ordinarias/api/leis",
            params={
                "termo": query,
                "quantidade": 5
            },
            headers={
                "Accept": "application/json",
                "User-Agent": "character_chatbot/1.0"
            },
            timeout=10
        )

        if res.status_code != 200:
            # fallback — busca no LexML que é mais estável
            return _buscar_lexml(query)

        data = res.json()
        leis = data.get("leis", data if isinstance(data, list) else [])

        if not leis:
            return _buscar_lexml(query)

        return [
            {
                "titulo": lei.get("titulo", ""),
                "numero": lei.get("numero", ""),
                "data": lei.get("data", ""),
                "ementa": lei.get("ementa", "")[:300],
                "url": lei.get("url", "")
            }
            for lei in leis[:5]
        ]

    except Exception:
        return _buscar_lexml(query)


def _buscar_lexml(query: str) -> list[dict]:
    """
    Fallback — LexML é o repositório oficial
    de legislação brasileira. API pública, sem chave.
    """
    try:
        res = httpx.get(
            "https://www.lexml.gov.br/busca/SRU",
            params={
                "operation": "searchRetrieve",
                "query": query,
                "maximumRecords": 5,
                "recordSchema": "opendocument"
            },
            timeout=10
        )

        if res.status_code != 200:
            return [{"erro": f"LexML retornou HTTP {res.status_code}"}]

        # LexML retorna XML
        import xml.etree.ElementTree as ET
        root = ET.fromstring(res.text)

        ns = {
            "srw": "http://www.loc.gov/zing/srw/",
            "lexml": "http://www.lexml.gov.br/oai/oaidc"
        }

        resultados = []
        for record in root.findall(".//srw:record", ns):
            data_node = record.find(".//srw:recordData", ns)
            if data_node is None:
                continue

            # extrai texto dos filhos
            titulo = ""
            ementa = ""
            url    = ""
            data   = ""

            for child in data_node.iter():
                tag = child.tag.lower()
                text = (child.text or "").strip()

                if "title" in tag and not titulo:
                    titulo = text
                if "description" in tag and not ementa:
                    ementa = text[:300]
                if "identifier" in tag and "http" in text:
                    url = text
                if "date" in tag and not data:
                    data = text

            if titulo:
                resultados.append({
                    "titulo": titulo,
                    "ementa": ementa,
                    "data": data,
                    "url": url
                })

        return resultados if resultados else [
            {"erro": f"Nenhuma legislação encontrada para '{query}'"}
        ]

    except Exception as e:
        return [{"erro": str(e)}]