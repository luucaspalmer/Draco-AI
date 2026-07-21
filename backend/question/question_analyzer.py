"""
question_analyzer.py

Responsável por identificar e classificar perguntas feitas ao Draco.
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
        "qual a relação",
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
# NORMALIZAÇÃO DE TEXTO
# ==========================================================

def normalize_text(text: str) -> str:
    """
    Normaliza um texto para facilitar comparações.
    """

    text = text.lower()
    text = text.strip()
    text = re.sub(r"[?!.,;:]+", "", text)
    text = " ".join(text.split())

    return text


# ==========================================================
# DETECÇÃO DE PERGUNTAS
# ==========================================================

def is_question(text: str) -> bool:
    """
    Verifica se uma mensagem parece ser uma pergunta.
    """

    text = normalize_text(text)

    for starter in QUESTION_STARTERS:
        if text.startswith(starter):
            return True

    return False


# ==========================================================
# IDENTIFICAÇÃO DO TIPO DA PERGUNTA
# ==========================================================

def get_question_type(text: str) -> str:
    """
    Identifica o tipo da pergunta.
    """

    text = normalize_text(text)

    for question_type, patterns in QUESTION_PATTERNS.items():

        for pattern in patterns:

            if text.startswith(pattern):
                return question_type

    return "unknown"


# ==========================================================
# EXTRAÇÃO DA ENTIDADE PRINCIPAL
# ==========================================================

def extract_entity(text: str) -> str:
    """
    Extrai a entidade principal da pergunta.
    """

    text = normalize_text(text)

    all_patterns = []

    for patterns in QUESTION_PATTERNS.values():
        all_patterns.extend(patterns)

    # Procura primeiro os padrões maiores
    all_patterns.sort(key=len, reverse=True)

    for pattern in all_patterns:

        if text.startswith(pattern):

            entity = text[len(pattern):].strip()

            return entity

    return ""


# ==========================================================
# ANALISADOR PRINCIPAL
# ==========================================================

def analyze_question(text: str) -> dict:
    """
    Analisa uma mensagem enviada pelo usuário.
    """

    text = normalize_text(text)

    is_question_result = is_question(text)

    question_type = "unknown"
    entity = ""

    if is_question_result:
        question_type = get_question_type(text)
        entity = extract_entity(text)

    return {
        "is_question": is_question_result,
        "question_type": question_type,
        "entity": entity
    }