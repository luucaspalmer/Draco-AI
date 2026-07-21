"""
Draco AI
Entity Classifier

Responsável por classificar entidades encontradas
pelo Entity Resolver.

Transforma:

"existe uma entidade chamada Aldorion"

em:

"tipo de entidade: personagem do universo Draco"
"rota correta: RAG"


Exemplos:

Draco
→ system_identity
→ identity


Lucas
→ user
→ memory


Aldorion
→ lore_character
→ rag


Python
→ knowledge
→ knowledge
"""


# ==========================================================
# TIPOS DE ENTIDADE
# ==========================================================


ENTITY_TYPES = {


    "draco": {

        "type": "system_identity",

        "route": "identity",

        "description": "Identidade principal do Draco AI"

    },


    "lucas": {

        "type": "user",

        "route": "memory",

        "description": "Usuário principal do sistema"

    },


    "python": {

        "type": "knowledge",

        "route": "knowledge",

        "description": "Conhecimento técnico"

    },


    "aldorion": {

        "type": "lore_character",

        "route": "rag",

        "description": "Personagem do universo Draco"

    }

}





# ==========================================================
# CLASSIFICADOR PRINCIPAL
# ==========================================================


def classify_entity(entity_data: dict) -> dict:
    """
    Recebe:

    {
        "entity": "aldorion",
        "exists": True,
        "source": "memory"
    }


    Retorna:

    {
        "entity": "aldorion",
        "exists": True,
        "entity_type": "lore_character",
        "route": "rag",
        "source": "memory"
    }

    """



    entity = entity_data.get(
        "entity",
        ""
    ).lower().strip()



    exists = entity_data.get(
        "exists",
        False
    )



    source = entity_data.get(
        "source",
        None
    )





    # ======================================================
    # Entidade vazia
    # ======================================================


    if not entity:


        return {


            "entity": "",


            "exists": False,


            "entity_type": "unknown",


            "route": "conversation",


            "source": None


        }





    # ======================================================
    # Entidade conhecida
    # ======================================================


    if entity in ENTITY_TYPES:


        data = ENTITY_TYPES[entity]


        return {


            "entity": entity,


            "exists": exists,


            "entity_type": data["type"],


            "route": data["route"],


            "source": source,


            "description": data["description"]


        }





    # ======================================================
    # Entidade desconhecida
    # ======================================================


    return {


        "entity": entity,


        "exists": exists,


        "entity_type": "unknown",


        "route": "knowledge",


        "source": source,


        "description": "Entidade sem classificação conhecida"


    }