"""
Draco AI
RAG Context Builder

Responsável por montar o contexto
proveniente da base de conhecimento.
"""


from backend.rag.retriever import (
    buscar_conhecimento
)



def construir_contexto_rag(
    pergunta,
    limite=3
):

    resultados = buscar_conhecimento(
        pergunta,
        quantidade=limite
    )


    if not resultados:

        return ""


    contexto = (
        "\n\n"
        "=== CONHECIMENTO RECUPERADO ===\n\n"
    )


    for item in resultados:

        contexto += (
            f"Fonte: {item['origem']}\n"
        )


        contexto += (
            item["texto"]
            +
            "\n\n"
        )


    contexto += (
        "=== FIM DO CONHECIMENTO ===\n"
    )


    return contexto



# Teste isolado

if __name__ == "__main__":


    pergunta = (
        "Me explique Python"
    )


    contexto = construir_contexto_rag(
        pergunta
    )


    print(contexto)