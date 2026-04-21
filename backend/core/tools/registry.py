from core.tools.universal.clima_atual import clima_atual
from core.tools.universal.data_hora_atual import data_hora_atual
from core.tools.academic_research.buscar_wikipedia import buscar_wikipedia
from core.tools.academic_research.noticias_educacao import noticias_educacao
from core.tools.academic_research.buscar_papers_arxiv import (
    buscar_papers_arxiv,
    papers_ia_recente,
)
from core.tools.finance.cotacao_acao import cotacao_acao
from core.tools.finance.selic_atual import selic_atual
from core.tools.finance.buscar_noticias_financeiras import buscar_noticias_financeiras
from core.tools.finance.cotacao_fii import cotacao_fii, listar_fiis_populares
from core.tools.tech.kernel_changelog import kernel_changelog
from core.tools.tech.buscar_docs_python import buscar_docs_python
from core.tools.tech.buscar_docs_rust import buscar_docs_rust
from core.tools.tech.noticias_ia import noticias_ia
from core.tools.tech.trending_github import trending_github
from core.tools.medical.buscar_pubmed import buscar_pubmed
from core.tools.medical.buscar_anvisa import buscar_anvisa
from core.tools.medical.buscar_remedios import buscar_remedios
from core.tools.medical.noticias_saude import noticias_saude
from core.tools.retail.ipca_atual import ipca_atual
from core.tools.retail.buscar_noticias_varejo import buscar_noticias_varejo
from core.tools.legal.buscar_legislacao_brasileira import buscar_legislacao_brasileira
from core.tools.legal.buscar_jurisprudencia_stj import (
    buscar_jurisprudencia as buscar_jurisprudencia_stj,
)
from core.tools.legal.noticias_juridicas import noticias_juridicas

TOOL_REGISTRY = {
    "clima_atual": clima_atual,
    "data_hora_atual": data_hora_atual,
    "buscar_papers_arxiv": buscar_papers_arxiv,
    "buscar_wikipedia": buscar_wikipedia,
    "noticias_educacao": noticias_educacao,
    "papers_ia_recente": papers_ia_recente,
    "cotacao_acao": cotacao_acao,
    "cotacao_fii": cotacao_fii,
    "selic_atual": selic_atual,
    "buscar_noticias_financeiras": buscar_noticias_financeiras,
    "listar_fiis_populares": listar_fiis_populares,
    "kernel_changelog": kernel_changelog,
    "buscar_docs_python": buscar_docs_python,
    "buscar_docs_rust": buscar_docs_rust,
    "noticias_ia": noticias_ia,
    "trending_github": trending_github,
    "buscar_pubmed": buscar_pubmed,
    "buscar_anvisa": buscar_anvisa,
    "buscar_remedios": buscar_remedios,
    "noticias_saude": noticias_saude,
    "ipca_atual": ipca_atual,
    "buscar_noticias_varejo": buscar_noticias_varejo,
    "buscar_legislacao_brasileira": buscar_legislacao_brasileira,
    "buscar_jurisprudencia_stj": buscar_jurisprudencia_stj,
    "noticias_juridicas": noticias_juridicas
}