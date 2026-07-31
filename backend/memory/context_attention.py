"""
Draco AI - Context Attention Manager
=====================================

Responsável por decidir, ANTES da montagem do prompt,
quais blocos de contexto realmente precisam ser
enviados ao modelo de linguagem.

--------------------------------------------------------
Problema que este módulo resolve
--------------------------------------------------------

O Question Router já sabe QUAL núcleo cognitivo deve
responder a pergunta (identity / memory / rag / graph / ...).

Porém, antes desta mudança, o ContextManager continuava
marcando vários blocos como "necessários" (memória
completa das 4 camadas, 10 mensagens de histórico, RAG
sem limite de tamanho por chunk) independente da rota
escolhida.

Resultado: um prompt de ~5.200 caracteres / 765 palavras
para perguntas que precisavam de uma fração disso, e
respostas do Qwen levando ~180s.

Este módulo centraliza a decisão "quanto contexto usar"
em um único lugar, granular e fácil de expandir.

--------------------------------------------------------
Fluxo
--------------------------------------------------------

Pergunta
    |
    v
Intenção + Rota (Question Router)
    |
    v
Context Attention Manager        <-- este módulo
    |
    v
Plano de atenção
(quais blocos, quantos itens, quantos caracteres)
    |
    v
Context Builder (carrega só o necessário)
    |
    v
Prompt Builder (monta o prompt mínimo)

--------------------------------------------------------
Como expandir
--------------------------------------------------------

Para adicionar uma nova fonte de contexto no futuro
(ex: agenda, e-mails, arquivos):

1. Adicione a chave no `plano_vazio()`.
2. Adicione uma regra de decisão em `decidir_atencao()`.
3. Consuma a nova chave no `context_builder.py`.

Nenhuma outra parte do sistema precisa mudar.
"""

from backend.memory.memory_search import identificar_categoria


# =====================================
# Mapa: categoria de memória -> camada física
# =====================================
#
# Evita carregar as 4 camadas de memória
# quando a pergunta só precisa de uma.

CATEGORIA_PARA_CAMADA = {

    "permanente": ["PERMANENTE"],

    "projeto": ["PROJETO"],

    "objetivo": ["PROJETO"],

    "conhecimento": ["CONHECIMENTO"],

    "preferencia": ["PREFERENCIA"],

    "geral": ["PERMANENTE", "PROJETO", "PREFERENCIA", "CONHECIMENTO"]

}


# =====================================
# Palavras-chave leves (fallback heurístico)
#
# Usadas somente quando a rota do Question Router
# não é conclusiva (conversa geral / fallback).
# =====================================

PROJETO_KEYWORDS = (

    "projeto", "backend", "frontend",
    "python", "codigo", "código", "ollama",
    "qwen", "memoria", "memória", "rag"

)

CONHECIMENTO_KEYWORDS = (

    "explique", "como funciona", "o que é",
    "defina", "conceito", "história", "historia"

)


# =====================================
# Plano padrão (tudo desligado)
# =====================================

def plano_vazio(motivo="Sem necessidade identificada"):

    return {

        # Identidade oficial do Draco (nome, criador, propósito...)
        "usar_identidade": False,

        # Bloco de personalidade/preferências de estilo (é barato)
        "usar_personalidade": True,

        # Memória do usuário
        "usar_memoria": False,

        # Quais camadas de memória carregar
        # (vazio = decide o context_builder; usado como fallback)
        "memoria_categorias": [],

        # Mantido por compatibilidade com o ContextManager antigo
        "usar_projetos": False,

        # Histórico da conversa atual
        "usar_conversa": False,

        "historico_limite": 0,

        # Base de conhecimento vetorial
        "usar_rag": False,

        "rag_limite": 0,

        "rag_max_chars": 600,

        # Motivo da decisão (debug / observabilidade)
        "motivo": motivo

    }


# =====================================
# Núcleo de decisão
# =====================================

def decidir_atencao(pergunta, intencao, rota_pergunta=None):
    """
    Decide quais blocos de contexto entram no prompt
    e com que limites.

    Não substitui o Question Router: usa a rota já
    calculada por ele como principal sinal de decisão,
    e só recorre a heurísticas por palavra-chave quando
    a rota cai em "conversation"/"general".
    """

    pergunta_lower = (pergunta or "").lower().strip()

    intencao = intencao or ""

    rota = None

    if rota_pergunta:

        rota = rota_pergunta.get("route")

    plano = plano_vazio()




    # =================================
    # Saudações nunca usam memória
    # =================================

    SAUDACOES = (
        "oi",
        "olá",
        "ola",
        "bom dia",
        "boa tarde",
        "boa noite",
        "e aí",
        "eai"
    )

    if pergunta_lower in SAUDACOES:

        plano["usar_conversa"] = True
        plano["historico_limite"] = 2
        plano["motivo"] = "Saudação simples"

        return plano





    # =================================
    # 1 - Identidade do Draco
    #
    # Exemplo: "Me conta a história do Draco"
    #
    # Resultado esperado:
    #   Identidade: SIM | Personalidade: SIM
    #   Histórico / RAG / Memória / Projetos: NÃO
    # =================================

    if rota == "identity" or intencao.startswith("identidade_"):

        plano["usar_identidade"] = True

        plano["usar_conversa"] = False

        plano["motivo"] = "Pergunta sobre identidade do Draco"

        return plano

    # =================================
    # 2 - Memória do usuário
    #
    # Exemplo: "O que eu gosto de programar?"
    #
    # Resultado esperado:
    #   Preferências: SIM | Memória: SIM
    #   Histórico recente: SIM | RAG: NÃO
    # =================================

    if (
        rota == "memory"
        or intencao.startswith("memoria_")
        or intencao in ("consultar_memoria", "consultar_nome")
    ):

        plano["usar_memoria"] = True

        analise = identificar_categoria(pergunta)

        categoria = analise.get("categoria", "geral")

        plano["memoria_categorias"] = CATEGORIA_PARA_CAMADA.get(
            categoria,
            CATEGORIA_PARA_CAMADA["geral"]
        )

        plano["usar_conversa"] = True

        plano["historico_limite"] = 4

        plano["motivo"] = f"Consulta de memória (categoria: {categoria})"

        return plano

    # =================================
    # 3 - Conhecimento externo / RAG
    # =================================

    if rota in ("rag", "knowledge"):

        plano["usar_rag"] = True

        plano["rag_limite"] = 3

        plano["rag_max_chars"] = 700

        plano["usar_conversa"] = True

        plano["historico_limite"] = 3

        plano["motivo"] = "Consulta de conhecimento (RAG)"

        return plano

    # =================================
    # 4 - Relações do grafo cognitivo
    #
    # O raciocínio do memory_graph já é calculado à parte
    # em brain.py (memory_reasoner.raciocinar), então aqui
    # basta garantir memória permanente mínima + histórico
    # curto, para o modelo ter contexto de quem é quem.
    # =================================

    if rota == "graph":

        plano["usar_memoria"] = True

        plano["memoria_categorias"] = ["PERMANENTE"]

        plano["usar_conversa"] = True

        plano["historico_limite"] = 3

        plano["motivo"] = "Consulta de relação (grafo cognitivo)"

        return plano

    # =================================
    # 5 - Fallback heurístico (conversa geral)
    # =================================

    usa_projeto = any(
        palavra in pergunta_lower
        for palavra in PROJETO_KEYWORDS
    )

    usa_conhecimento = any(
        palavra in pergunta_lower
        for palavra in CONHECIMENTO_KEYWORDS
    )

    motivos = []

    if usa_conhecimento:

        plano["usar_rag"] = True

        plano["rag_limite"] = 2

        plano["rag_max_chars"] = 600

        motivos.append("conhecimento (heurística)")

    if usa_projeto:

        plano["usar_memoria"] = True

        plano["memoria_categorias"] = ["PROJETO"]

        motivos.append("projeto (heurística)")

    plano["usar_conversa"] = True

    plano["historico_limite"] = 4

    plano["motivo"] = ", ".join(motivos) if motivos else "Conversa geral"

    return plano


# =====================================
# Teste manual
# =====================================

if __name__ == "__main__":

    exemplos = [

        ("Me conta a história do Draco", "identidade_origem", {"route": "identity"}),

        ("O que eu gosto de programar?", "memoria_preferencia", {"route": "memory"}),

        ("O que é inteligência artificial?", "conversa", {"route": "knowledge"}),

        ("Olá, tudo bem?", "conversa", {"route": "conversation"}),

    ]

    for pergunta, intencao, rota in exemplos:

        print("\nPergunta:", pergunta)

        print(decidir_atencao(pergunta, intencao, rota))
