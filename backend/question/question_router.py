"""
Draco AI
Question Router

Responsável por decidir qual núcleo do Draco
deve responder uma pergunta.

Fluxo:

question_analyzer
        |
        ↓
entity_resolver
        |
        ↓
entity_classifier
        |
        ↓
question_router
        |
        ↓
memory / identity / RAG / graph
"""


# ==========================================================
# ROTAS POR TIPO DE PERGUNTA
# ==========================================================


QUESTION_ROUTES = {


    "definition": "knowledge",


    "event": "rag",


    "location": "rag",


    "list": "rag",


    "relationship": "graph",


    "time": "knowledge",


    "owner": "memory",


    "quantity": "knowledge"


}





# ==========================================================
# ROTAS POR TIPO DE ENTIDADE
# ==========================================================


ENTITY_ROUTES = {


    "system_identity": "identity",


    "user": "memory",


    "lore_character": "rag",


    "knowledge": "knowledge"

}





# ==========================================================
# ROUTER PRINCIPAL
# ==========================================================


def route_question(
    question_data: dict,
    entity_data: dict = None
) -> dict:
    """
    Recebe:

    question_data:

    {
        "is_question": True,
        "question_type": "person",
        "entity": "aldorion"
    }


    entity_data:

    {
        "entity": "aldorion",
        "entity_type": "lore_character",
        "route": "rag"
    }



    Retorna:

    {
        "route": "rag",
        "source": "entity_classifier"
    }

    """



    question_type = question_data.get(
        "question_type",
        "unknown"
    )


    entity = question_data.get(
        "entity",
        ""
    )





    # ======================================================
    # Não é pergunta
    # ======================================================


    if not question_data.get(
        "is_question",
        False
    ):


        return {


            "route": "conversation",


            "source": "conversation",


            "question_type": "unknown",


            "entity": ""

        }





    # ======================================================
    # Prioridade 1:
    # Classificação da entidade
    # ======================================================


    if entity_data:


        entity_type = entity_data.get(
            "entity_type",
            "unknown"
        )


        if entity_type in ENTITY_ROUTES:


            return {


                "route": ENTITY_ROUTES[entity_type],


                "source": "entity_classifier",


                "entity_type": entity_type,


                "question_type": question_type,


                "entity": entity


            }





    # ======================================================
    # Prioridade 2:
    # Tipo da pergunta
    # ======================================================


    if question_type in QUESTION_ROUTES:


        route = QUESTION_ROUTES[
            question_type
        ]


        return {


            "route": route,


            "source": "question_type",


            "question_type": question_type,


            "entity": entity


        }





    # ======================================================
    # Fallback
    # ======================================================


    return {


        "route": "general",


        "source": "qwen",


        "question_type": question_type,


        "entity": entity


    }