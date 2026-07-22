"""
Draco AI
Entity Classifier

Classifica entidades encontradas pelo Entity Resolver.

Responsabilidade:

Resolver encontra:
    Jhoricka
    source: rag

Classifier transforma:

    entity_type:
        knowledge

    route:
        rag


O classifier não deve limitar crescimento do Draco.

Ele deve confiar nas fontes:
- internal
- memory
- rag
"""


# ==========================================================
# ENTIDADES FIXAS IMPORTANTES
# ==========================================================


ENTITY_OVERRIDES = {


    "draco": {

        "entity_type": "system_identity",

        "route": "identity",

        "description":
            "Identidade principal do Draco AI"

    },


    "lucas": {

        "entity_type": "user",

        "route": "memory",

        "description":
            "Usuário principal do Draco"

    },


}





# ==========================================================
# MAPA DE ROTAS POR TIPO
# ==========================================================


TYPE_ROUTES = {


    "system_identity":
        "identity",


    "user":
        "memory",


    "lore_character":
        "rag",


    "knowledge":
        "rag",


    "project":
        "rag",


    "unknown":
        "knowledge"

}





# ==========================================================
# CLASSIFICADOR PRINCIPAL
# ==========================================================


def classify_entity(entity_data: dict) -> dict:


    entity = entity_data.get(
        "entity",
        ""
    ).lower().strip()



    exists = entity_data.get(
        "exists",
        False
    )


    source = entity_data.get(
        "source"
    )


    resolver_type = entity_data.get(
        "entity_type"
    )



    resolver_route = entity_data.get(
        "route_hint"
    )





    resultado = {


        "entity": entity,


        "exists": exists,


        "entity_type": "unknown",


        "route": "knowledge",


        "source": source,


        "description":
            "Entidade classificada pelo Draco"

    }





    # ======================================================
    # Entidade vazia
    # ======================================================


    if not entity:


        return resultado





    # ======================================================
    # Override interno
    # ======================================================


    if entity in ENTITY_OVERRIDES:


        dados = ENTITY_OVERRIDES[entity]


        resultado.update({

            "entity_type":
                dados["entity_type"],


            "route":
                dados["route"],


            "description":
                dados["description"]

        })


        return resultado





    # ======================================================
    # Respeitar Entity Resolver
    # ======================================================


    if resolver_type and resolver_type != "unknown":


        resultado["entity_type"] = resolver_type



        if resolver_route:

            resultado["route"] = resolver_route


        else:

            resultado["route"] = TYPE_ROUTES.get(

                resolver_type,

                "knowledge"

            )


        resultado["description"] = (

            "Classificação herdada do Entity Resolver"

        )


        return resultado





    # ======================================================
    # Inferência pela fonte
    # ======================================================


    if source == "rag":


        resultado.update({

            "entity_type":
                "knowledge",

            "route":
                "rag",

            "description":
                "Entidade encontrada no conhecimento RAG"

        })


        return resultado





    if source == "memory":


        resultado.update({

            "entity_type":
                "user_memory",

            "route":
                "memory",

            "description":
                "Entidade encontrada na memória do usuário"

        })


        return resultado





    if source == "internal":


        resultado.update({

            "entity_type":
                "knowledge",

            "route":
                "knowledge"

        })


        return resultado





    # ======================================================
    # Desconhecida
    # ======================================================


    return resultado