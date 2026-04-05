# core/tools/registry.py
from core.tools.universal import (
    clima_atual,
    data_hora_atual,
    web_search,
)
from core.tools.academic_research import (
    buscar_wikipedia,
    noticias_educacao,
)
from core.tools.academic_research.buscar_papers_arxiv import (
    buscar_papers_arxiv,
    papers_ia_recentes,
)

from core.tools.finance import (
    cotacao_acao,
    selic_atual,
    buscar_noticias_financeiras
)

from tools.finance.cotacao_fii import (cotacao_fii, listar_fiis_populares)

# mapeia nome (string) → função Python real
TOOL_REGISTRY = {
    "clima_atual": clima_atual,
    "data_hora_atual": data_hora_atual,
    "web_search": web_search,
    "buscar_papers_arxiv": buscar_papers_arxiv,
    "buscar_wikipedia": buscar_wikipedia,
    "noticias_educacao": noticias_educacao,
    "papers_ia_recente": papers_ia_recentes,
    "cotacao_acao": cotacao_acao,
    "cotacao_fii": cotacao_fii,
    "selic_atual": selic_atual,
    "buscar_noticias_financeiras": buscar_noticias_financeiras,
    "listar_fiis_populares": listar_fiis_populares
}