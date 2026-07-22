"""
Draco AI
Entity Resolver

Responsável por identificar e validar entidades
presentes nas perguntas do usuário.

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


Fontes consultadas:

1. Banco interno
2. RAG
3. Memória
4. Desconhecido
"""


import re


from backend.memory.memory_search import (
    buscar_memorias
)



# =====================================
# RAG
# =====================================

try:

    from backend.rag.rag_manager import (
        rag_manager
    )

except Exception:

    rag_manager = None





# =====================================
# Banco interno
# =====================================


ENTITY_DATABASE = {


    "draco": {

        "entity_type": "system_identity",
        "source": "internal"

    },


    "draco ai": {

        "entity_type": "system_identity",
        "source": "internal"

    },


    "assistente draco": {

        "entity_type": "system_identity",
        "source": "internal"

    },


    "lucas": {

        "entity_type": "user",
        "source": "memory"

    },


    "lucas rafael palmer da silva": {

        "entity_type": "user",
        "source": "memory"

    },


    "python": {

        "entity_type": "knowledge",
        "source": "internal"

    },


    "inteligência artificial": {

        "entity_type": "knowledge",
        "source": "internal"

    },


    "ia": {

        "entity_type": "knowledge",
        "source": "internal"

    }

}





# =====================================
# Normalização
# =====================================


def normalize_entity(entity):


    if not entity:

        return ""


    entity = entity.lower().strip()


    entity = re.sub(

        r"[?!.,;:]",

        "",

        entity

    )


    return " ".join(
        entity.split()
    )







# =====================================
# Entidade interna
# =====================================


def find_known_entity(entity):


    return ENTITY_DATABASE.get(
        entity
    )







# =====================================
# Buscar RAG
# =====================================


def search_rag_entity(entity):


    if not rag_manager:

        return None



    try:


        contexto = rag_manager.buscar_contexto(
            entity
        )


        if contexto:


            return contexto



    except Exception:


        pass



    return None








# =====================================
# Resolver entidade
# =====================================


def resolve_entity(entity):


    entity = normalize_entity(
        entity
    )


    resultado = {


        "entity": entity,

        "exists": False,

        "entity_type": "unknown",

        "source": None,

        "route_hint": None,

        "rag_context_found": False,

        "rag_context": None


    }




    if not entity:


        return resultado






    # =================================
    # 1 - Banco interno
    # =================================


    entidade = find_known_entity(
        entity
    )


    if entidade:


        resultado.update({


            "exists": True,

            "entity_type":
                entidade["entity_type"],


            "source":
                entidade["source"],


            "route_hint":
                (
                    "identity"
                    if entidade["entity_type"]
                    ==
                    "system_identity"
                    else
                    "memory"
                )


        })


        return resultado








    # =================================
    # 2 - RAG
    #
    # Projetos, personagens,
    # conhecimento interno
    # =================================


    rag_context = search_rag_entity(
        entity
    )



    if rag_context:


        resultado.update({


            "exists": True,


            "entity_type":
                "knowledge",


            "source":
                "rag",


            "route_hint":
                "rag",


            "rag_context_found":
                True,


            "rag_context":
                rag_context


        })


        return resultado








    # =================================
    # 3 - Memória usuário
    # =================================


    try:


        memoria = buscar_memorias(
            entity
        )


        if memoria:


            resultado.update({


                "exists": True,


                "entity_type":
                    "user",


                "source":
                    "memory",


                "route_hint":
                    "memory"


            })


            return resultado



    except Exception:


        pass






    # =================================
    # 4 - Desconhecido
    # =================================


    return resultado