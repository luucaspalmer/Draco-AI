"""
question_analyzer.py

Responsável por identificar, classificar e direcionar
perguntas feitas ao Draco.

Versão:
- Classificação de perguntas
- Extração de entidade
- Detecção de intenção
- Roteamento para ferramentas
"""


import re


# ==========================================================
# TIPOS DE PERGUNTAS
# ==========================================================

QUESTION_TYPES = {

    "definition",
    "person",
    "time",
    "location",
    "list",
    "reason",
    "event",
    "relationship",
    "quantity",
    "owner",
    "unknown"

}


# ==========================================================
# INTENÇÕES DO DRACO
# ==========================================================

INTENTS = {


    # --------------------------
    # Ferramenta de clima
    # --------------------------

    "weather": (

        "clima",
        "tempo",
        "temperatura",
        "chuva",
        "chover",
        "previsão",
        "meteorologia"

    ),


    # --------------------------
    # Identidade do Draco
    # --------------------------

    "identity": (

        "draco",
        "você",
        "seu nome",
        "quem criou você"

    ),


    # --------------------------
    # Conversação normal
    # --------------------------

    "conversation": (

        "olá",
        "oi",
        "bom dia",
        "boa tarde",
        "boa noite"

    )

}



# ==========================================================
# MAPA DE FERRAMENTAS
# ==========================================================


TOOL_MAP = {


    "weather": "weather"


}



# ==========================================================
# INÍCIOS CONHECIDOS DE PERGUNTAS
# ==========================================================


QUESTION_STARTERS = (

    "quem",
    "quem é",
    "quem foi",
    "quem são",

    "o que",
    "o que é",
    "o que são",
    "o que aconteceu",

    "quando",

    "onde",
    "onde fica",

    "qual",
    "qual é",
    "qual foi",

    "quais",
    "quais são",

    "como",

    "por que",
    "porque",

    "de quem",

    "quantos",
    "quantas"

)



# ==========================================================
# PADRÕES POR TIPO DE PERGUNTA
# ==========================================================


QUESTION_PATTERNS = {


    "definition": (

        "o que significa",
        "o que são",
        "o que é",
        "defina",
        "explique"

    ),


    "person": (

        "quem são",
        "quem foi",
        "quem é"

    ),


    "time": (

        "quando nasceu",
        "quando aconteceu",
        "quando foi",
        "em que data",
        "em que ano",
        "quando"

    ),


    "location": (

        "onde nasceu",
        "onde fica",
        "onde está",
        "onde"

    ),


    "list": (

        "quais são",
        "quais",
        "liste",
        "cite"

    ),


    "reason": (

        "por que",
        "porque"

    ),


    "event": (

        "o que aconteceu",
        "como aconteceu"

    ),


    "relationship": (

        "qual é a relação",
        "qual a relação"

    ),


    "quantity": (

        "quantos",
        "quantas"

    ),


    "owner": (

        "quem é o dono",
        "quem pertence",
        "de quem é"

    )

}



# ==========================================================
# NORMALIZAÇÃO
# ==========================================================


def normalize_text(text: str) -> str:
    """
    Normaliza texto para análise.
    """

    text = text.lower()

    text = text.strip()

    text = re.sub(
        r"[?!.,;:]+",
        "",
        text
    )

    text = " ".join(
        text.split()
    )

    return text



# ==========================================================
# DETECÇÃO DE PERGUNTA
# ==========================================================


def is_question(text: str) -> bool:
    """
    Verifica se mensagem parece uma pergunta.
    """

    text = normalize_text(text)


    for starter in QUESTION_STARTERS:

        if text.startswith(starter):

            return True


    return False



# ==========================================================
# IDENTIFICA TIPO DA PERGUNTA
# ==========================================================


def get_question_type(text: str) -> str:
    """
    Identifica categoria da pergunta.
    """

    text = normalize_text(text)


    for question_type, patterns in QUESTION_PATTERNS.items():

        for pattern in patterns:

            if text.startswith(pattern):

                return question_type


    return "unknown"



# ==========================================================
# EXTRAÇÃO DE ENTIDADE
# ==========================================================


def extract_entity(text: str) -> str:
    """
    Extrai assunto principal.
    """

    text = normalize_text(text)


    all_patterns = []


    for patterns in QUESTION_PATTERNS.values():

        all_patterns.extend(patterns)


    all_patterns.sort(
        key=len,
        reverse=True
    )


    for pattern in all_patterns:


        if text.startswith(pattern):

            entity = text[len(pattern):].strip()

            return entity


    return ""



# ==========================================================
# DETECÇÃO DE INTENÇÃO
# ==========================================================


def detect_intent(text: str) -> str:
    """
    Identifica intenção da mensagem.
    """

    text = normalize_text(text)


    for intent, keywords in INTENTS.items():


        for keyword in keywords:


            if keyword in text:

                return intent



    return "unknown"



# ==========================================================
# IDENTIFICA FERRAMENTA NECESSÁRIA
# ==========================================================


def get_tool(intent: str):
    """
    Retorna ferramenta associada à intenção.
    """

    return TOOL_MAP.get(
        intent
    )



# ==========================================================
# ANALISADOR PRINCIPAL
# ==========================================================


def analyze_question(text: str) -> dict:
    """
    Analisa mensagem enviada ao Draco.
    """


    text = normalize_text(text)


    question_result = is_question(text)


    question_type = "unknown"

    entity = ""


    if question_result:

        question_type = get_question_type(text)

        entity = extract_entity(text)



    intent = detect_intent(text)


    tool = get_tool(intent)



    return {


        "is_question": question_result,


        "question_type": question_type,


        "entity": entity,


        "intent": intent,


        "tool": tool

    }