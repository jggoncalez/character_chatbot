# core/tools/declarations.py

from google.genai import types

TOOL_DECLARATIONS: dict[str, types.FunctionDeclaration] = {

    # ── UNIVERSAIS ────────────────────────────────────────
    "clima_atual": types.FunctionDeclaration(
        name="clima_atual",
        description=(
            "Retorna o clima atual de uma cidade. "
            "Use quando perguntarem sobre tempo, temperatura, "
            "se vai chover, se está frio ou quente."
        ),
        parameters={
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Nome da cidade. Ex: 'Guariba', 'São Paulo'"
                }
            }
        }
    ),

    "data_hora_atual": types.FunctionDeclaration(
        name="data_hora_atual",
        description=(
            "Retorna a data e hora atual. "
            "Use quando perguntarem que horas são, "
            "que dia é hoje, qual o dia da semana."
        ),
        parameters={
            "type": "object",
            "properties": {}
        }
    ),

    # ── WIKIPEDIA ─────────────────────────────────────────
    "buscar_wikipedia": types.FunctionDeclaration(
        name="buscar_wikipedia",
        description=(
            "Busca informações reais na Wikipedia em português. "
            "Use para perguntas sobre pessoas, lugares, "
            "eventos históricos, conceitos."
        ),
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Termo a buscar. Ex: 'fotossíntese', 'Idade Média'"
                }
            },
            "required": ["query"]
        }
    ),

    "curiosidade_aleatoria": types.FunctionDeclaration(
        name="curiosidade_aleatoria",
        description=(
            "Traz uma curiosidade aleatória da Wikipedia. "
            "Use quando pedirem algo interessante, "
            "uma curiosidade, um fato aleatório."
        ),
        parameters={
            "type": "object",
            "properties": {}
        }
    ),

    # ── ARXIV ─────────────────────────────────────────────
    "buscar_papers_arxiv": types.FunctionDeclaration(
        name="buscar_papers_arxiv",
        description=(
            "Busca papers científicos recentes no ArXiv. "
            "Use para perguntas sobre pesquisas, avanços científicos, "
            "machine learning, física, matemática, computação."
        ),
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "Termo de busca em inglês. "
                        "Ex: 'large language models', "
                        "'reinforcement learning 2025'"
                    )
                },
                "max_results": {
                    "type": "integer",
                    "description": "Quantidade de papers. Padrão 3, máximo 5."
                }
            },
            "required": ["query"]
        }
    ),

    "papers_ia_recentes": types.FunctionDeclaration(
        name="papers_ia_recentes",
        description=(
            "Busca os papers mais recentes de IA e Machine Learning. "
            "Use quando perguntarem sobre novidades em IA, "
            "últimos avanços, pesquisas recentes."
        ),
        parameters={
            "type": "object",
            "properties": {}
        }
    ),

    # ── FINANCEIRO ────────────────────────────────────────
    "cotacao_acao": types.FunctionDeclaration(
        name="cotacao_acao",
        description=(
            "Busca cotação atual de uma ação na B3. "
            "Use quando perguntarem sobre preço de ações específicas."
        ),
        parameters={
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Código da ação. Ex: PETR4, VALE3, ITUB4"
                }
            },
            "required": ["ticker"]
        }
    ),

    "cotacao_fii": types.FunctionDeclaration(
        name="cotacao_fii",
        description=(
            "Busca cotação atual de um FII na B3. "
            "Retorna preço, variação, dividend yield e P/VP."
        ),
        parameters={
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Código do FII. Ex: HGLG11, MXRF11, KNRI11"
                }
            },
            "required": ["ticker"]
        }
    ),

    "listar_fiis_populares": types.FunctionDeclaration(
        name="listar_fiis_populares",
        description=(
            "Lista cotações dos FIIs mais negociados da B3. "
            "Use quando perguntarem sobre o mercado de FIIs em geral."
        ),
        parameters={
            "type": "object",
            "properties": {}
        }
    ),

    "selic_atual": types.FunctionDeclaration(
        name="selic_atual",
        description=(
            "Retorna a taxa Selic atual do Banco Central. "
            "Use quando perguntarem sobre juros, renda fixa, "
            "Tesouro Direto, CDI."
        ),
        parameters={
            "type": "object",
            "properties": {}
        }
    ),

    "buscar_noticias_financeiras": types.FunctionDeclaration(
        name="buscar_noticias_financeiras",
        description=(
            "Busca as últimas notícias do mercado financeiro brasileiro. "
            "Use quando perguntarem sobre o mercado hoje, "
            "Ibovespa, economia, bolsa."
        ),
        parameters={
            "type": "object",
            "properties": {}
        }
    ),

    # ── EDUCAÇÃO ──────────────────────────────────────────
    "noticias_educacao": types.FunctionDeclaration(
        name="noticias_educacao",
        description=(
            "Busca notícias recentes sobre educação no Brasil. "
            "Use quando perguntarem sobre ensino, MEC, "
            "ENEM, universidades, políticas educacionais."
        ),
        parameters={
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer",
                    "description": "Quantidade de notícias. Padrão 5."
                }
            }
        }
    ),

    "noticias_tecnologia_educacao": types.FunctionDeclaration(
        name="noticias_tecnologia_educacao",
        description=(
            "Busca notícias sobre tecnologia aplicada à educação. "
            "Use quando perguntarem sobre EdTech, ensino online, "
            "IA na educação."
        ),
        parameters={
            "type": "object",
            "properties": {}
        }
    ),

    # ── LINUX / TECH ──────────────────────────────────────
    "kernel_changelog": types.FunctionDeclaration(
        name="kernel_changelog",
        description=(
            "Busca as últimas atualizações do Kernel Linux. "
            "Use quando perguntarem sobre novidades no Linux, "
            "versões recentes do kernel, patches."
        ),
        parameters={
            "type": "object",
            "properties": {}
        }
    ),

    "trending_github": types.FunctionDeclaration(
        name="trending_github",
        description=(
            "Busca repositórios em alta no GitHub. "
            "Use quando perguntarem sobre projetos populares, "
            "tendências de tecnologia, bibliotecas novas."
        ),
        parameters={
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "description": (
                        "Linguagem de programação para filtrar. "
                        "Ex: 'python', 'rust', 'typescript'. "
                        "Deixe vazio para todas."
                    )
                }
            }
        }
    ),

    # ── MÉDICO ────────────────────────────────────────────
    "buscar_pubmed": types.FunctionDeclaration(
        name="buscar_pubmed",
        description=(
            "Busca artigos médicos recentes no PubMed. "
            "Use quando perguntarem sobre doenças, tratamentos, "
            "pesquisas médicas, medicamentos."
        ),
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "Termo médico em inglês ou português. "
                        "Ex: 'diabetes treatment 2025', 'cancer immunotherapy'"
                    )
                }
            },
            "required": ["query"]
        }
    ),

    # ── JURÍDICO ──────────────────────────────────────────
    "buscar_legislacao_brasileira": types.FunctionDeclaration(
        name="buscar_legislacao_brasileira",
        description=(
            "Busca leis e legislação brasileira no Planalto. "
            "Use quando perguntarem sobre leis, decretos, "
            "direitos, legislação específica."
        ),
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "Termo jurídico a buscar. "
                        "Ex: 'Código de Defesa do Consumidor', "
                        "'CLT artigo 482'"
                    )
                }
            },
            "required": ["query"]
        }
    ),
}