
# core/tools/arxiv.py

import httpx
import xml.etree.ElementTree as ET

def buscar_papers_arxiv(query: str, max_results: int = 3) -> list[dict]:
    """Busca papers científicos recentes no ArXiv."""
    try:
        res = httpx.get(
            "https://export.arxiv.org/api/query",
            params={
                "search_query": query,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
                "max_results": max_results
            },
            timeout=10
        )

        # ArXiv retorna XML — precisa parsear
        root = ET.fromstring(res.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        papers = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns)
            summary = entry.find("atom:summary", ns)
            published = entry.find("atom:published", ns)
            link = entry.find("atom:id", ns)

            # autores
            authors = [
                name_elem.text
                for a in entry.findall("atom:author", ns)
                for name_elem in [a.find("atom:name", ns)]
                if name_elem is not None
            ]

            papers.append({
                "titulo": title.text.strip() if title is not None and title.text else "",
                "resumo": summary.text.strip()[:300] if summary is not None and summary.text else "",
                "autores": authors[:3],  # máximo 3 autores
                "publicado": published.text[:10] if published is not None and published.text else "",
                "url": link.text.strip() if link is not None and link.text else ""
            })

        return papers if papers else [{"erro": f"Nenhum paper encontrado para '{query}'"}]

    except Exception as e:
        return [{"erro": str(e)}]


def papers_ia_recentes() -> list[dict]:
    """Atalho — busca papers recentes de IA sem precisar de query."""
    return buscar_papers_arxiv(
        "cat:cs.AI OR cat:cs.LG OR cat:cs.CL",
        max_results=3
    )
    
if __name__ == "__main__":
    papers = papers_ia_recentes()
    for p in papers:
        print(f"{p['titulo']} por {', '.join(p['autores'])}\nPublicado em: {p['publicado']}\n{p['resumo']}\n{p['url']}\n")