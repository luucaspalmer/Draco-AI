"""
Draco AI
Question Executor

Executa a decisão tomada pelo Question Dispatcher.

Responsável por chamar os núcleos:

- Identity
- Memory
- Graph
- RAG
- Knowledge
- Qwen
"""


# ==========================================================
# Memória
# ==========================================================

from backend.memory.memory_search import (
    buscar_memorias
)



# ==========================================================
# RAG
# ==========================================================

from backend.rag.rag_manager import (
    rag_manager
)



# ==========================================================
# Executor principal
# ==========================================================

def execute_question(
    dispatch_data: dict,
    question_data: dict = None
) -> dict:


    executor = dispatch_data.get(
        "executor",
        "qwen"
    )


    route = dispatch_data.get(
        "route",
        "conversation"
    )


    module = dispatch_data.get(
        "module",
        "conversation"
    )



    pergunta = ""

    entity = ""



    if question_data:


        pergunta = question_data.get(
            "question",
            ""
        )


        entity = question_data.get(
            "entity",
            ""
        )



    result = {


        "success": True,

        "executor": executor,

        "module": module,

        "route": route,

        "handled": False,

        "response": None,

        "rag_context": None

    }





    # ======================================================
    # Identity
    # ======================================================

    if executor == "identity":

        return result






    # ======================================================
    # Memory
    # ======================================================

    if executor == "memory":


        try:


            memoria = buscar_memorias(
                entity
            )


            if memoria:


                result["handled"] = True


                result["response"] = memoria



        except Exception as e:


            result["error"] = str(e)



        return result







    # ======================================================
    # Memory Graph
    # ======================================================

    if executor == "graph":

        return result







    # ======================================================
    # Knowledge
    # ======================================================

    if executor == "knowledge":

        return result




    # ======================================================
    # RAG
    # ======================================================

    if executor == "rag":

        try:

            contexto = rag_manager.buscar_contexto(
                pergunta
            )


            if contexto:

                result["rag_context"] = contexto


        except Exception as e:

            result["error"] = str(e)


        return result




    # ======================================================
    # Conversa / Qwen
    # ======================================================

    return result