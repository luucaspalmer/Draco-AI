"""
Draco AI - Intelligence / Intent Analyzer

Não reclassifica a intenção do zero. O Draco já possui:

- question_analyzer.analyze_question
- intents.identificar_intencao
- intent_ai.identificar_intencao_ai (fallback via Qwen)

Este módulo recebe a intenção FINAL já resolvida pelo brain.py
(evitando uma segunda chamada ao Qwen) e adiciona duas camadas
que hoje não existem em lugar nenhum do sistema:

- complexidade da pergunta
- objetivo cognitivo por trás da intenção
"""


# =====================================
# Palavras que indicam alta complexidade
# =====================================

PALAVRAS_ALTA_COMPLEXIDADE = (

    "compare",

    "comparar",

    "diferença entre",

    "diferenca entre",

    "passo a passo",

    "explique detalhadamente",

    "explique em detalhes",

    "analise",

    "analisar",

    "vantagens e desvantagens",

    "prós e contras",

    "pros e contras"

)


# =====================================
# Objetivo cognitivo por intenção
# =====================================

OBJETIVOS_POR_INTENCAO = {

    "identidade_nome": "Consultar identidade do Draco",
    "identidade_criador": "Consultar identidade do Draco",
    "identidade_origem": "Consultar identidade do Draco",
    "identidade_proposito": "Consultar identidade do Draco",
    "identidade_missao": "Consultar identidade do Draco",
    "identidade_valores": "Consultar identidade do Draco",
    "identidade_capacidades": "Consultar identidade do Draco",
    "identidade_arquitetura": "Consultar identidade do Draco",

    "memoria_nome": "Registrar informação pessoal",
    "memoria_preferencia": "Registrar preferência do usuário",
    "memoria_projeto": "Registrar projeto do usuário",
    "memoria_objetivo": "Registrar objetivo do usuário",
    "memoria_conhecimento": "Registrar conhecimento do usuário",

    "consultar_nome": "Consultar memória pessoal",
    "consultar_memoria": "Consultar memória pessoal",

    "alterar_estilo": "Ajustar comportamento do Draco",

    "conversa": "Conversar / obter informação geral"

}


# =====================================
# Complexidade
# =====================================

def calcular_complexidade(pergunta):

    texto = pergunta.lower().strip()

    palavras = texto.split()

    for termo in PALAVRAS_ALTA_COMPLEXIDADE:

        if termo in texto:

            return "alta"

    if len(palavras) <= 4:

        return "baixa"

    if len(palavras) >= 25:

        return "alta"

    return "media"


# =====================================
# Objetivo
# =====================================

def identificar_objetivo(intencao):

    return OBJETIVOS_POR_INTENCAO.get(

        intencao,

        "Obter informação ou realizar uma ação solicitada"

    )


# =====================================
# Análise principal
# =====================================

def analisar_intencao(pergunta, dados_pergunta, intencao):
    """
    Args:
        pergunta: texto original do usuário
        dados_pergunta: saída de question_analyzer.analyze_question
        intencao: intenção final já resolvida pelo brain.py
            (backend.intents + fallback backend.intent_ai)

    Returns:
        dict com intenção, tipo de pergunta, entidade,
        complexidade e objetivo.
    """

    dados_pergunta = dados_pergunta or {}

    complexidade = calcular_complexidade(pergunta)

    objetivo = identificar_objetivo(intencao)

    return {

        "intencao": intencao,

        "tipo_pergunta": dados_pergunta.get(
            "question_type",
            "unknown"
        ),

        "entidade": dados_pergunta.get(
            "entity",
            ""
        ),

        "is_question": dados_pergunta.get(
            "is_question",
            False
        ),

        "complexidade": complexidade,

        "objetivo": objetivo

    }


# =====================================
# Teste manual
# =====================================

if __name__ == "__main__":

    exemplo = analisar_intencao(

        "Compare Python e JavaScript para IA",

        {
            "question_type": "list",
            "entity": "python e javascript",
            "is_question": True
        },

        "conversa"

    )

    print(exemplo)
