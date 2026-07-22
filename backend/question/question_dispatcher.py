"""
Draco AI
Question Dispatcher

Responsável por decidir qual módulo do Draco
deverá responder uma pergunta.
"""


def dispatch_question(route_data: dict) -> dict:

    route = route_data.get("route", "conversation")

    dispatch = {

        "executor": "qwen",

        "module": "conversation",

        "route": route

    }

    if route == "tool":

        dispatch["executor"] = "tool_manager"

        dispatch["module"] = "tools"

        dispatch["tool"] = route_data.get("tool")

    elif route == "identity":

        dispatch["executor"] = "identity"

        dispatch["module"] = "identity"

    elif route == "memory":

        dispatch["executor"] = "memory"

        dispatch["module"] = "memory"

    elif route == "graph":

        dispatch["executor"] = "graph"

        dispatch["module"] = "memory_graph"

    elif route == "knowledge":

        dispatch["executor"] = "knowledge"

        dispatch["module"] = "knowledge"

    elif route == "rag":

        dispatch["executor"] = "rag"

        dispatch["module"] = "rag"

    elif route == "conversation":

        dispatch["executor"] = "qwen"

        dispatch["module"] = "conversation"

    return dispatch