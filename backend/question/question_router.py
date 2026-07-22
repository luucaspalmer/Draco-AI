"""
Draco AI
Question Router

Responsável por decidir qual núcleo do Draco
deve responder uma pergunta.

Fluxo:

question_analyzer
        │
        ▼
entity_resolver
        │
        ▼
entity_classifier
        │
        ▼
question_router
        │
        ▼
memory / identity / rag / graph / knowledge / tool
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
# ROTAS POR INTENÇÃO
# ==========================================================

INTENT_ROUTES = {

    "identity": "identity",

    "weather": "tool",

    "conversation": "conversation",

    "relationship": "graph"

}



# ==========================================================
# INTENÇÕES DE MEMÓRIA
# ==========================================================

MEMORY_INTENTS = [

    "memoria_nome",

    "memoria_preferencia",

    "memoria_projeto",

    "memoria_objetivo",

    "memoria_conhecimento",

    "consultar_nome",

    "consultar_memoria"

]



# ==========================================================
# INTENÇÕES DE IDENTIDADE
# ==========================================================

IDENTITY_INTENTS = [

    "identidade_nome",

    "identidade_criador",

    "identidade_origem",

    "identidade_proposito",

    "identidade_missao",

    "identidade_valores",

    "identidade_capacidades",

    "identidade_arquitetura"

]



# ==========================================================
# TIPOS DE PERGUNTA QUE INDICAM RELAÇÃO
# ==========================================================

RELATIONSHIP_TYPES = [

    "relationship"

]



# ==========================================================
# CRIADOR DE RESPOSTA
# ==========================================================

def build_route(
    route,
    source,
    intent,
    question_type,
    entity,
    entity_type
):

    return {

        "route": route,

        "source": source,

        "intent": intent,

        "question_type": question_type,

        "entity": entity,

        "entity_type": entity_type

    }



# ==========================================================
# ROUTER PRINCIPAL
# ==========================================================

def route_question(
    question_data: dict,
    entity_data: dict = None
) -> dict:


    question_type = question_data.get(
        "question_type",
        "unknown"
    )


    entity = question_data.get(
        "entity",
        ""
    )


    intent = question_data.get(
        "intent",
        "unknown"
    )


    tool = question_data.get(
        "tool"
    )



    entity_type = "unknown"

    resolver_route = None



    if entity_data:


        entity_type = entity_data.get(
            "entity_type",
            "unknown"
        )


        resolver_route = entity_data.get(
            "route"
        )




    # ======================================================
    # Não é pergunta
    # ======================================================

    if not question_data.get(
        "is_question",
        False
    ):


        return build_route(

            "conversation",

            "conversation",

            intent,

            question_type,

            entity,

            entity_type

        )





    # ======================================================
    # PRIORIDADE 0
    # Ferramentas
    # ======================================================

    if tool:


        return {

            "route": "tool",

            "source": "tool_manager",

            "tool": tool,

            "intent": intent,

            "question_type": question_type,

            "entity": entity,

            "entity_type": entity_type

        }




    # ======================================================
    # PRIORIDADE 1
    # Relacionamentos
    #
    # IMPORTANTE:
    # "Qual a relação entre Lucas e Draco?"
    #
    # Não pode cair em identity
    # ======================================================

    if question_type in RELATIONSHIP_TYPES:


        return build_route(

            "graph",

            "relationship",

            intent,

            question_type,

            entity,

            entity_type

        )





    # ======================================================
    # PRIORIDADE 2
    # Memória do usuário
    # ======================================================

    if intent in MEMORY_INTENTS:


        return build_route(

            "memory",

            "memory_intent",

            intent,

            question_type,

            entity,

            entity_type

        )





    # ======================================================
    # PRIORIDADE 3
    # Identidade Draco
    # ======================================================

    if intent in IDENTITY_INTENTS:


        return build_route(

            "identity",

            "identity_intent",

            intent,

            question_type,

            entity,

            entity_type

        )





    # ======================================================
    # PRIORIDADE 4
    # Tipo da pergunta
    #
    # Antes da entidade
    # ======================================================

    if question_type in QUESTION_ROUTES:


        return build_route(

            QUESTION_ROUTES[question_type],

            "question_type",

            intent,

            question_type,

            entity,

            entity_type

        )





    # ======================================================
    # PRIORIDADE 5
    # Entity Resolver
    # ======================================================

    if (
        resolver_route
        and
        entity_type != "unknown"
    ):


        return build_route(

            resolver_route,

            "entity_resolver",

            intent,

            question_type,

            entity,

            entity_type

        )





    # ======================================================
    # PRIORIDADE 6
    # Tipo entidade
    # ======================================================

    if entity_type in ENTITY_ROUTES:


        return build_route(

            ENTITY_ROUTES[entity_type],

            "entity_classifier",

            intent,

            question_type,

            entity,

            entity_type

        )





    # ======================================================
    # PRIORIDADE 7
    # Intenção simples
    # ======================================================

    if intent in INTENT_ROUTES:


        return build_route(

            INTENT_ROUTES[intent],

            "intent",

            intent,

            question_type,

            entity,

            entity_type

        )





    # ======================================================
    # FALLBACK
    # ======================================================

    return build_route(

        "general",

        "fallback",

        intent,

        question_type,

        entity,

        entity_type

    )