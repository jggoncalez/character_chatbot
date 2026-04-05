import os
from types import SimpleNamespace

import pytest

from core.tools.academic_research.buscar_papers_arxiv import (
    buscar_papers_arxiv,
    papers_ia_recente,
)
from core.tools.academic_research.buscar_wikipedia import buscar_wikipedia
from core.tools.academic_research.noticias_educacao import noticias_educacao
from core.tools.finance.buscar_noticias_financeiras import buscar_noticias_financeiras
from core.tools.finance.cotacao_acao import cotacao_acao
from core.tools.finance.cotacao_fii import cotacao_fii, listar_fiis_populares
from core.tools.finance.selic_atual import selic_atual
from core.tools.legal.buscar_jurisprudencia_stj import (
    buscar_jurisprudencia as buscar_jurisprudencia_stj,
)
from core.tools.legal.buscar_legislacao_brasileira import buscar_legislacao_brasileira
from core.tools.legal.noticias_juridicas import noticias_juridicas
from core.tools.medical.buscar_anvisa import buscar_anvisa
from core.tools.medical.buscar_pubmed import buscar_pubmed
from core.tools.medical.buscar_remedios import buscar_remedios
from core.tools.medical.noticias_saude import noticias_saude
from core.tools.retail.buscar_noticias_varejo import buscar_noticias_varejo
from core.tools.retail.ipca_atual import ipca_atual
from core.tools.tech.buscar_docs_python import buscar_docs_python
from core.tools.tech.buscar_docs_rust import buscar_docs_rust
from core.tools.tech.kernel_changelog import kernel_changelog
from core.tools.tech.noticias_ia import noticias_ia
from core.tools.tech.trending_github import trending_github
from core.tools.universal.clima_atual import clima_atual
from core.tools.universal.data_hora_atual import data_hora_atual


class FakeResponse:
    def __init__(self, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json_data = json_data
        self.text = text

    def json(self):
        return self._json_data


class AttrDict(dict):
    """Dict com acesso por atributo para simular entradas do feedparser."""

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(name)


@pytest.fixture(autouse=True)
def mock_external_dependencies(monkeypatch):
    import feedparser
    import httpx

    monkeypatch.setenv("BRAPI_KEY", "test-token")

    def fake_httpx_get(url, params=None, headers=None, timeout=None, follow_redirects=False):
        if "wttr.in" in url:
            return FakeResponse(
                json_data={
                    "current_condition": [
                        {
                            "temp_C": "25",
                            "FeelsLikeC": "26",
                            "weatherDesc": [{"value": "Ensolarado"}],
                            "humidity": "50",
                        }
                    ]
                }
            )

        if "pt.wikipedia.org/w/api.php" in url:
            return FakeResponse(json_data={"query": {"search": [{"title": "Python"}]}})

        if "pt.wikipedia.org/api/rest_v1/page/summary/" in url:
            return FakeResponse(
                json_data={
                    "title": "Python",
                    "extract": "Python e uma linguagem de programacao.",
                    "content_urls": {"desktop": {"page": "https://pt.wikipedia.org/wiki/Python"}},
                }
            )

        if "export.arxiv.org/api/query" in url:
            xml = """
            <feed xmlns=\"http://www.w3.org/2005/Atom\">
              <entry>
                <title>Paper Teste</title>
                <summary>Resumo do paper.</summary>
                <published>2026-04-01T00:00:00Z</published>
                <id>https://arxiv.org/abs/0000.00000</id>
                <author><name>Autor 1</name></author>
              </entry>
            </feed>
            """.strip()
            return FakeResponse(text=xml)

        if "brapi.dev/api/quote/" in url:
            tickers = url.rsplit("/", 1)[-1]
            if "," in tickers:
                symbols = tickers.split(",")
                results = [
                    {
                        "symbol": s,
                        "longName": f"FII {s}",
                        "regularMarketPrice": 100.0,
                        "regularMarketChangePercent": 0.5,
                        "dividendYield": 0.9,
                        "priceToBook": 0.95,
                    }
                    for s in symbols
                ]
                return FakeResponse(json_data={"results": results})

            return FakeResponse(
                json_data={
                    "results": [
                        {
                            "symbol": tickers,
                            "longName": f"Ativo {tickers}",
                            "regularMarketPrice": 10.0,
                            "regularMarketChangePercent": 1.2,
                            "regularMarketOpen": 9.9,
                            "regularMarketDayLow": 9.8,
                            "regularMarketDayHigh": 10.2,
                            "regularMarketVolume": 123456,
                            "dividendYield": 0.8,
                            "priceToBook": 1.1,
                        }
                    ]
                }
            )

        if "bcdata.sgs.11" in url:
            return FakeResponse(json_data=[{"valor": "10.50", "data": "01/04/2026"}])

        if "bcdata.sgs.433" in url:
            return FakeResponse(
                json_data=[
                    {"data": "01/01/2026", "valor": "0.10"},
                    {"data": "01/02/2026", "valor": "0.20"},
                    {"data": "01/03/2026", "valor": "0.30"},
                ]
            )

        if "docs.python.org/3/search-index.json" in url:
            return FakeResponse(
                json_data={
                    "objects": [
                        ["str.join", "function", "library/stdtypes", "str.join", "Join strings"]
                    ]
                }
            )

        if "docs.rs/search" in url:
            return FakeResponse(json_data={})

        if "crates.io/api/v1/crates" in url:
            return FakeResponse(
                json_data={
                    "crates": [
                        {
                            "name": "serde",
                            "description": "Serialization framework",
                            "newest_version": "1.0.0",
                            "downloads": 1000000,
                        }
                    ]
                }
            )

        if "api.github.com/search/repositories" in url:
            return FakeResponse(
                json_data={
                    "items": [
                        {
                            "full_name": "org/projeto",
                            "description": "Projeto em alta",
                            "language": "Python",
                            "stargazers_count": 999,
                            "html_url": "https://github.com/org/projeto",
                        }
                    ]
                }
            )

        if "eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi" in url:
            return FakeResponse(json_data={"esearchresult": {"idlist": ["123"]}})

        if "eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi" in url:
            return FakeResponse(
                json_data={
                    "result": {
                        "123": {
                            "title": "Medical paper",
                            "authors": [{"name": "Author A"}],
                            "source": "Journal",
                            "pubdate": "2026",
                        }
                    }
                }
            )

        if "consultas.anvisa.gov.br/api/consulta/medicamentos/" in url:
            return FakeResponse(
                json_data={
                    "content": [
                        {
                            "nomeProduto": "Dipirona",
                            "nomeTitular": "Lab X",
                            "categoriaProduto": "Medicamento",
                            "situacaoRegistro": "V",
                            "dataVencimentoRegistro": "2030-01-01",
                            "classeTerapeutica": "Analgesico",
                            "principioAtivo": "Dipirona",
                            "tipoProduto": "Generico",
                        }
                    ]
                }
            )

        if "planalto.gov.br/legislacao" in url:
            return FakeResponse(
                json_data={
                    "leis": [
                        {
                            "titulo": "Lei Teste",
                            "numero": "1234",
                            "data": "2020-01-01",
                            "ementa": "Ementa da lei",
                            "url": "https://planalto.gov.br/lei1234",
                        }
                    ]
                }
            )

        if "lexml.gov.br/busca/SRU" in url:
            xml = """
            <srw:searchRetrieveResponse xmlns:srw=\"http://www.loc.gov/zing/srw/\">
              <srw:records>
                <srw:record>
                  <srw:recordData>
                    <title>Norma X</title>
                    <description>Descricao da norma</description>
                    <identifier>https://lexml.gov.br/norma-x</identifier>
                    <date>2025-01-01</date>
                  </srw:recordData>
                </srw:record>
              </srw:records>
            </srw:searchRetrieveResponse>
            """.strip()
            return FakeResponse(text=xml)

        if "scon.stj.jus.br/SCON/pesquisar.jsp" in url:
            return FakeResponse(status_code=200, text="<html>ok</html>")

        raise AssertionError(f"URL nao mockada no teste: {url}")

    def fake_feedparser_parse(url):
        if "infomoney.com.br" in url:
            entries = [
                SimpleNamespace(title="Noticia Financeira", link="https://example.com/finance")
            ]
            return SimpleNamespace(entries=entries)

        common_entries = [
            AttrDict(
                {
                    "title": "Titulo",
                    "summary": "Resumo",
                    "link": "https://example.com/noticia",
                    "published": "2026-04-01",
                }
            )
        ]
        return SimpleNamespace(entries=common_entries)

    monkeypatch.setattr(httpx, "get", fake_httpx_get)
    monkeypatch.setattr(feedparser, "parse", fake_feedparser_parse)


TOOL_CASES = [
    ("clima_atual", clima_atual, {"city": "Sao Paulo"}, dict),
    ("data_hora_atual", data_hora_atual, {}, dict),
    ("buscar_papers_arxiv", buscar_papers_arxiv, {"query": "llm", "max_results": 1}, list),
    ("buscar_wikipedia", buscar_wikipedia, {"query": "Python"}, dict),
    ("noticias_educacao", noticias_educacao, {"max_results": 1}, list),
    ("papers_ia_recente", papers_ia_recente, {}, list),
    ("cotacao_acao", cotacao_acao, {"ticker": "PETR4"}, dict),
    ("cotacao_fii", cotacao_fii, {"ticker": "HGLG11"}, dict),
    ("selic_atual", selic_atual, {}, dict),
    ("buscar_noticias_financeiras", buscar_noticias_financeiras, {}, list),
    ("listar_fiis_populares", listar_fiis_populares, {}, list),
    ("kernel_changelog", kernel_changelog, {}, list),
    ("buscar_docs_python", buscar_docs_python, {"query": "join"}, list),
    ("buscar_docs_rust", buscar_docs_rust, {"query": "serde"}, list),
    ("noticias_ia", noticias_ia, {"max_results": 1}, list),
    ("trending_github", trending_github, {"language": "python"}, list),
    ("buscar_pubmed", buscar_pubmed, {"query": "diabetes", "max_results": 1}, list),
    ("buscar_anvisa", buscar_anvisa, {"query": "dipirona"}, list),
    ("buscar_remedios", buscar_remedios, {"medicamento": "dipirona"}, list),
    ("noticias_saude", noticias_saude, {}, list),
    ("ipca_atual", ipca_atual, {}, dict),
    ("buscar_noticias_varejo", buscar_noticias_varejo, {"max_results": 1}, list),
    ("buscar_legislacao_brasileira", buscar_legislacao_brasileira, {"query": "LGPD"}, list),
    ("buscar_jurisprudencia_stj", buscar_jurisprudencia_stj, {"query": "habeas corpus"}, list),
    ("noticias_juridicas", noticias_juridicas, {}, list),
]


@pytest.mark.integration
@pytest.mark.parametrize("tool_name, tool_fn, kwargs, expected_type", TOOL_CASES)
def test_all_tools_return_expected_type(tool_name, tool_fn, kwargs, expected_type):
    result = tool_fn(**kwargs)

    assert isinstance(result, expected_type), f"{tool_name} retornou tipo invalido"

    if expected_type is dict:
        assert "erro" not in result, f"{tool_name} retornou erro: {result}"

    if expected_type is list:
        assert result, f"{tool_name} retornou lista vazia"
        assert isinstance(result[0], dict), f"{tool_name} deve retornar lista de dict"
        assert "erro" not in result[0], f"{tool_name} retornou erro: {result[0]}"


@pytest.mark.integration
def test_web_search_not_in_tool_cases():
    tested_tools = {name for name, _, _, _ in TOOL_CASES}
    assert "web_search" not in tested_tools


@pytest.mark.integration
def test_tool_count_excluding_web_search():
    # Total atual de tools funcionais: 25 (todas menos web_search).
    assert len(TOOL_CASES) == 25
