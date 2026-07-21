"""
Draco AI
Entity Resolver

Responsável por identificar e validar entidades
presentes nas perguntas do usuário.

Exemplo:

Pergunta:
"Quem é Aldorion?"

Analyzer:
{
    "question_type": "person",
    "entity": "aldorion"
}

Resolver:
{
    "entity": "aldorion",
    "exists": True,
    "source": "rag"
}

"""


# =====================================
# Importações
# =====================================

from backend.memory.memory_search import buscar_memorias


# Futuramente:
# from backend.rag.retriever import buscar_conhecimento



# =====================================
# Entidades conhecidas do Draco
# =====================================


KNOWN_ENTITIES = [

    "draco",

    "lucas",

    "python",

    "inteligência artificial",

]



# =====================================
# Normalização
# =====================================

def normalize_entity(entity):

    if not entity:
        return ""

    return entity.lower().strip()



# =====================================
# Resolver entidade
# =====================================

def resolve_entity(entity):

    """
    Recebe uma entidade e verifica
    possíveis fontes de conhecimento.
    """

    entity = normalize_entity(entity)


    resultado = {

        "entity": entity,

        "exists": False,

        "source": None

    }



    if not entity:

        return resultado





    # =====================================
    # Verificar entidades internas
    # =====================================

    for known in KNOWN_ENTITIES:


        if entity == known:


            resultado["exists"] = True

            resultado["source"] = "internal"

            return resultado





    # =====================================
    # Verificar memória
    # =====================================


    try:


        memoria = buscar_memorias(
            entity
        )


        if memoria:


            resultado["exists"] = True

            resultado["source"] = "memory"

            return resultado



    except Exception:


        pass





    # =====================================
    # Caso não encontre
    # =====================================


    return resultado