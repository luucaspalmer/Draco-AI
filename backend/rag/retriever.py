"""
Draco AI
Retriever

Responsável por buscar conhecimento
semântico no banco vetorial.
"""


from pathlib import Path

import chromadb


from backend.rag.embeddings import (
    gerar_embedding
)



# =====================================
# Configuração
# =====================================

VECTOR_DB_PATH = Path(
    "data/knowledge/vector_db"
)


COLLECTION_NAME = "draco_knowledge"



# =====================================
# Conectar ao banco vetorial
# =====================================

client = chromadb.PersistentClient(
    path=str(VECTOR_DB_PATH)
)


collection = client.get_collection(
    name=COLLECTION_NAME
)



# =====================================
# Buscar conhecimento
# =====================================

def buscar_conhecimento(
    pergunta,
    quantidade=3
):

    # Transformar pergunta em vetor
    vetor_pergunta = gerar_embedding(
        pergunta
    )


    resultado = collection.query(
        query_embeddings=[
            vetor_pergunta
        ],
        n_results=quantidade
    )


    documentos = []


    for i, texto in enumerate(
        resultado["documents"][0]
    ):

        documentos.append(
            {
                "texto": texto,
                "origem": resultado["metadatas"][0][i]
            }
        )


    return documentos



# =====================================
# Teste
# =====================================

if __name__ == "__main__":


    pergunta = (
        "O que é o Projeto Eclipse?"
    )


    resultados = buscar_conhecimento(
        pergunta
    )


    print(
        "\nResultados encontrados:\n"
    )


    for item in resultados:

        print(
            "Origem:",
            item["origem"]
        )


        print(
            item["texto"]
        )


        print(
            "-" * 50
        )