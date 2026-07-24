"""
Draco AI
RAG Context Builder

Responsável por montar o contexto
proveniente da base de conhecimento.

--------------------------------------------------------
Mudança principal
--------------------------------------------------------

Antes: `contexto += item["texto"]` injetava o texto
COMPLETO de cada chunk recuperado, sem limite. Com 3
resultados, isso sozinho já podia dobrar o tamanho do
prompt.

Agora: recebe `max_chars` (decidido pelo Context
Attention Manager) e corta cada chunk nesse limite,
preservando a legibilidade (corte em texto + "...").
"""

from backend.rag.retriever import (
    buscar_conhecimento
)


def construir_contexto_rag(
    pergunta,
    limite=3,
    max_chars=700
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

        texto = item["texto"]

        if max_chars and len(texto) > max_chars:

            texto = texto[:max_chars].rstrip() + "..."

        contexto += (
            f"Fonte: {item['origem']}\n"
        )


        contexto += (
            texto
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
