# core/tools/declarations.py

from google.genai import types

def schema(definition: dict) -> types.Schema:
    return types.Schema.model_validate(definition)

TOOL_DECLARATIONS: dict[str, types.FunctionDeclaration] = {

    # ── UNIVERSAIS ────────────────────────────────────────
    "clima_atual": types.FunctionDeclaration(
        name="clima_atual",
        description=(
            "Retorna o clima atual de uma cidade. "
            "Use quando perguntarem sobre tempo, temperatura, "
            "se vai chover, se está frio ou quente."
        ),
        parameters=schema({
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Nome da cidade. Ex: 'Guariba', 'São Paulo'"
                }
            }
        })
    ),

    "data_hora_atual": types.FunctionDeclaration(
        name="data_hora_atual",
        description=(
            "Retorna a data e hora atual. "
            "Use quando perguntarem que horas são, "
            "que dia é hoje, qual o dia da semana."
        ),
        parameters=schema({
            "type": "object",
            "properties": {}
        })
    ),

    "web_search": types.FunctionDeclaration(
        name="web_search",
        description=(
            "Realiza busca na web por informações atuais. "
            "Use quando a pergunta exigir fatos recentes, "
            "notícias ou dados fora da base local."
        ),
        parameters=schema({
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Termo de busca. Ex: 'cotação dólar hoje', 'notícias IA Brasil'"
                }
            },
            "required": ["query"]
        })
    ),

    # ── WIKIPEDIA ─────────────────────────────────────────
    "buscar_wikipedia": types.FunctionDeclaration(
        name="buscar_wikipedia",
        description=(
            "Busca informações reais na Wikipedia em português. "
            "Use para perguntas sobre pessoas, lugares, "
            "eventos históricos, conceitos."
        ),
        parameters=schema({
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Termo a buscar. Ex: 'fotossíntese', 'Idade Média'"
                }
            },
            "required": ["query"]
        })
    ),

    # ── ARXIV ─────────────────────────────────────────────
    "buscar_papers_arxiv": types.FunctionDeclaration(
        name="buscar_papers_arxiv",
        description=(
            "Busca papers científicos recentes no ArXiv. "
            "Use para perguntas sobre pesquisas, avanços científicos, "
            "machine learning, física, matemática, computação."
        ),
        parameters=schema({
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
        })
    ),

    "papers_ia_recente": types.FunctionDeclaration(
        name="papers_ia_recente",
        description=(
            "Busca os papers mais recentes de IA e Machine Learning. "
            "Use quando perguntarem sobre novidades em IA, "
            "últimos avanços, pesquisas recentes."
        ),
        parameters=schema({
            "type": "object",
            "properties": {}
        })
    ),

    # ── FINANCEIRO ────────────────────────────────────────
    "cotacao_acao": types.FunctionDeclaration(
        name="cotacao_acao",
        description=(
            "Busca cotação atual de uma ação na B3. "
            "Use quando perguntarem sobre preço de ações específicas."
        ),
        parameters=schema({
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Código da ação. Ex: PETR4, VALE3, ITUB4"
                }
            },
            "required": ["ticker"]
        })
    ),

    "cotacao_fii": types.FunctionDeclaration(
        name="cotacao_fii",
        description=(
            "Busca cotação atual de um FII na B3. "
            "Retorna preço, variação, dividend yield e P/VP."
        ),
        parameters=schema({
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Código do FII. Ex: HGLG11, MXRF11, KNRI11"
                }
            },
            "required": ["ticker"]
        })
    ),

    "listar_fiis_populares": types.FunctionDeclaration(
        name="listar_fiis_populares",
        description=(
            "Lista cotações dos FIIs mais negociados da B3. "
            "Use quando perguntarem sobre o mercado de FIIs em geral."
        ),
        parameters=schema({
            "type": "object",
            "properties": {}
        })
    ),

    "selic_atual": types.FunctionDeclaration(
        name="selic_atual",
        description=(
            "Retorna a taxa Selic atual do Banco Central. "
            "Use quando perguntarem sobre juros, renda fixa, "
            "Tesouro Direto, CDI."
        ),
        parameters=schema({
            "type": "object",
            "properties": {}
        })
    ),

    "buscar_noticias_financeiras": types.FunctionDeclaration(
        name="buscar_noticias_financeiras",
        description=(
            "Busca as últimas notícias do mercado financeiro brasileiro. "
            "Use quando perguntarem sobre o mercado hoje, "
            "Ibovespa, economia, bolsa."
        ),
        parameters=schema({
            "type": "object",
            "properties": {}
        })
    ),

    # ── EDUCAÇÃO ──────────────────────────────────────────
    "noticias_educacao": types.FunctionDeclaration(
        name="noticias_educacao",
        description=(
            "Busca notícias recentes sobre educação no Brasil. "
            "Use quando perguntarem sobre ensino, MEC, "
            "ENEM, universidades, políticas educacionais."
        ),
        parameters=schema({
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer",
                    "description": "Quantidade de notícias. Padrão 5."
                }
            }
        })
    ),

    # ── LINUX / TECH ──────────────────────────────────────
    "kernel_changelog": types.FunctionDeclaration(
        name="kernel_changelog",
        description=(
            "Busca as últimas atualizações do Kernel Linux. "
            "Use quando perguntarem sobre novidades no Linux, "
            "versões recentes do kernel, patches."
        ),
        parameters=schema({
            "type": "object",
            "properties": {}
        })
    ),

    "buscar_docs_python": types.FunctionDeclaration(
        name="buscar_docs_python",
        description=(
            "Busca referências na documentação oficial do Python. "
            "Use para dúvidas sobre funções, módulos, sintaxe e recursos da linguagem."
        ),
        parameters=schema({
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Termo técnico para buscar na documentação do Python."
                }
            },
            "required": ["query"]
        })
    ),

    "buscar_docs_rust": types.FunctionDeclaration(
        name="buscar_docs_rust",
        description=(
            "Busca referências na documentação e ecossistema Rust. "
            "Use para dúvidas sobre crates, módulos e recursos da linguagem."
        ),
        parameters=schema({
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Termo técnico para buscar na documentação do Rust."
                }
            },
            "required": ["query"]
        })
    ),

    "noticias_ia": types.FunctionDeclaration(
        name="noticias_ia",
        description=(
            "Busca notícias recentes sobre Inteligência Artificial em múltiplas fontes. "
            "Use quando perguntarem sobre novidades e tendências em IA."
        ),
        parameters=schema({
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer",
                    "description": "Quantidade de notícias. Padrão 5."
                }
            }
        })
    ),

    "trending_github": types.FunctionDeclaration(
        name="trending_github",
        description=(
            "Busca repositórios em alta no GitHub. "
            "Use quando perguntarem sobre projetos populares, "
            "tendências de tecnologia, bibliotecas novas."
        ),
        parameters=schema({
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
        })
    ),

    # ── MÉDICO ────────────────────────────────────────────
    "buscar_pubmed": types.FunctionDeclaration(
        name="buscar_pubmed",
        description=(
            "Busca artigos médicos recentes no PubMed. "
            "Use quando perguntarem sobre doenças, tratamentos, "
            "pesquisas médicas, medicamentos."
        ),
        parameters=schema({
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
        })
    ),

    "buscar_anvisa": types.FunctionDeclaration(
        name="buscar_anvisa",
        description=(
            "Busca medicamentos e produtos na base pública da ANVISA. "
            "Use para validar registro, fabricante e situação regulatória."
        ),
        parameters=schema({
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Nome do medicamento ou produto para consulta na ANVISA."
                }
            },
            "required": ["query"]
        })
    ),

    "buscar_remedios": types.FunctionDeclaration(
        name="buscar_remedios",
        description=(
            "Busca informações de medicamentos em base pública regulatória. "
            "Use para consultar nome comercial, princípio ativo e laboratório."
        ),
        parameters=schema({
            "type": "object",
            "properties": {
                "medicamento": {
                    "type": "string",
                    "description": "Nome do medicamento. Ex: 'dipirona', 'amoxicilina'"
                }
            },
            "required": ["medicamento"]
        })
    ),

    "noticias_saude": types.FunctionDeclaration(
        name="noticias_saude",
        description=(
            "Busca notícias recentes de saúde em fontes públicas. "
            "Use para novidades de saúde pública, ciência e medicina."
        ),
        parameters=schema({
            "type": "object",
            "properties": {}
        })
    ),

    # ── VAREJO ────────────────────────────────────────────
    "ipca_atual": types.FunctionDeclaration(
        name="ipca_atual",
        description=(
            "Retorna o IPCA mais recente via Banco Central. "
            "Use para inflação, preços e análise macroeconômica no Brasil."
        ),
        parameters=schema({
            "type": "object",
            "properties": {}
        })
    ),

    "buscar_noticias_varejo": types.FunctionDeclaration(
        name="buscar_noticias_varejo",
        description=(
            "Busca notícias do setor de varejo e supermercados. "
            "Use para tendências de consumo, mercado varejista e trade."
        ),
        parameters=schema({
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer",
                    "description": "Quantidade de notícias. Padrão 5."
                }
            }
        })
    ),

    # ── JURÍDICO ──────────────────────────────────────────
    "buscar_legislacao_brasileira": types.FunctionDeclaration(
        name="buscar_legislacao_brasileira",
        description=(
            "Busca leis e legislação brasileira no Planalto. "
            "Use quando perguntarem sobre leis, decretos, "
            "direitos, legislação específica."
        ),
        parameters=schema({
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
        })
    ),

    "buscar_jurisprudencia_stj": types.FunctionDeclaration(
        name="buscar_jurisprudencia_stj",
        description=(
            "Busca jurisprudência do STJ por termo jurídico. "
            "Use para precedentes, acórdãos e entendimento dos tribunais superiores."
        ),
        parameters=schema({
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Termo jurídico para pesquisa no STJ."
                }
            },
            "required": ["query"]
        })
    ),

    "noticias_juridicas": types.FunctionDeclaration(
        name="noticias_juridicas",
        description=(
            "Busca notícias jurídicas recentes em fontes especializadas. "
            "Use para novidades legislativas, decisões e atualizações do Judiciário."
        ),
        parameters=schema({
            "type": "object",
            "properties": {}
        })
    ),
}