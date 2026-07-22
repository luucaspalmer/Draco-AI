"""
Draco AI
Question Dispatcher

Responsável por converter uma rota lógica em um
executor que será utilizado pelo Question Executor.
"""


# ==========================================================
# MAPA DE DISPATCH
# ==========================================================

DISPATCH_TABLE = {

    "tool": {
        "executor": "tool_manager",
        "module": "tools"
    },

    "identity": {
        "executor": "identity",
        "module": "identity"
    },

    "memory": {
        "executor": "memory",
        "module": "memory"
    },

    "graph": {
        "executor": "graph",
        "module": "memory_graph"
    },

    "knowledge": {
        "executor": "knowledge",
        "module": "knowledge"
    },

    "rag": {
        "executor": "rag",
        "module": "rag"
    },

    "conversation": {
        "executor": "qwen",
        "module": "conversation"
    },

    "general": {
        "executor": "qwen",
        "module": "conversation"
    }

}


# ==========================================================
# DISPATCHER PRINCIPAL
# ==========================================================

def dispatch_question(route_data: dict) -> dict:
    """
    Converte uma rota lógica em um executor.

    Entrada:

    {
        "route": "rag",
        "entity": "Jhoricka",
        "question_type": "definition",
        "intent": "knowledge"
    }

    Retorno:

    {
        "executor": "rag",
        "module": "rag",
        "route": "rag",
        "entity": "Jhoricka",
        "question_type": "definition",
        "intent": "knowledge"
    }
    """

    route = route_data.get(
        "route",
        "general"
    )

    config = DISPATCH_TABLE.get(
        route,
        DISPATCH_TABLE["general"]
    )

    dispatch = {

        "executor": config["executor"],

        "module": config["module"],

        "route": route,

        "source": route_data.get("source"),

        "intent": route_data.get("intent"),

        "entity": route_data.get("entity"),

        "entity_type": route_data.get("entity_type"),

        "question_type": route_data.get("question_type")

    }

    if route == "tool":

        dispatch["tool"] = route_data.get(
            "tool"
        )

    return dispatch