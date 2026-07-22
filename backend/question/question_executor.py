"""
Draco AI
Question Executor

Executa decisões cognitivas.

Prioridade:

Tools
Identity
Memory
Graph
RAG
Knowledge
Qwen
"""


from backend.memory.memory_search import (
    buscar_memorias
)

from backend.memory.memory_formatter import (
    formatar_memoria
)

from backend.rag.rag_manager import (
    rag_manager
)

from backend.tools.tool_manager import (
    ToolManager
)



# =====================================
# Perguntas de memória
# =====================================

MEMORY_QUERY_WORDS = [

    "meu nome",

    "o que eu gosto",

    "o que você lembra",

    "quem sou eu",

    "minhas informações",

    "sobre mim"

]



def is_memory_question(text):

    text = text.lower()

    for item in MEMORY_QUERY_WORDS:

        if item in text:

            return True

    return False



# =====================================
# Executor
# =====================================

def execute_question(
    dispatch_data: dict,
    question_data: dict = None
):


    executor = dispatch_data.get(
        "executor",
        "qwen"
    )


    pergunta = ""


    if question_data:

        pergunta = question_data.get(
            "question",
            ""
        )



    result = {


        "success": True,

        "executor": executor,

        "handled": False,

        "response": None,

        "rag_context": None

    }



    # =================================
    # TOOL
    # =================================

    if executor == "tool_manager":


        tool = dispatch_data.get(
            "tool"
        )


        resposta = ToolManager().execute(
            tool
        )


        if resposta:

            result["handled"] = True

            result["response"] = resposta


        return result




    # =================================
    # IDENTITY
    # =================================

    if executor == "identity":


        result["handled"] = True


        result["response"] = (
            "Meu nome é Draco. "
            "Sou um Dragão Guardião do Conhecimento. "
            "Fui criado por Lucas Palmer."
        )


        return result





    # =================================
    # MEMORY
    # =================================


    if executor == "memory" or is_memory_question(pergunta):


        try:


            memoria = buscar_memorias(
                "usuario"
            )


            if memoria:


                texto = formatar_memoria(
                    memoria
                )


                result["handled"] = True

                result["response"] = texto



        except Exception as e:

            result["error"] = str(e)



        return result





    # =================================
    # RAG
    # =================================


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





    return result