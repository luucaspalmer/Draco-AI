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
    quantidade=3,
    limite_distancia=1.40
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


    textos = resultado["documents"][0]

    metadados = resultado["metadatas"][0]

    distancias = resultado["distances"][0]



    print("\n====== DISTÂNCIA DOS RESULTADOS ======")



    for i, texto in enumerate(textos):


        distancia = distancias[i]


        print(
            f"{i+1} - {metadados[i]} | Distância: {distancia:.4f}"
        )


        # =====================================
        # Filtro de relevância
        # =====================================

        if distancia > limite_distancia:

            print(
                "Ignorado por baixa relevância"
            )

            continue



        documentos.append(
            {
                "texto": texto,
                "origem": metadados[i],
                "distancia": distancia
            }
        )



    print(
        "====================================\n"
    )



    # =====================================
    # DEBUG TAMANHO DOS DOCUMENTOS
    # =====================================

    print("\n===== TAMANHO DOS DOCUMENTOS =====")

    for i, doc in enumerate(documentos):

        print(
            f"Documento {i+1}: {len(doc['texto'])} caracteres"
        )

    print(
        "===============================\n"
    )



    # =====================================
    # DEBUG RESULTADOS FINAIS DO RAG
    # =====================================

    print("\n====== RESULTADOS DO RAG ======")


    for i, doc in enumerate(documentos):

        print(
            f"\nCHUNK {i+1}"
        )


        print(
            "Origem:",
            doc["origem"]
        )


        print(
            "Distância:",
            round(
                doc["distancia"],
                4
            )
        )


        print(
            "Tamanho:",
            len(doc["texto"]),
            "caracteres"
        )


        print(
            "-" * 50
        )


        print(
            doc["texto"][:500]
        )


    print(
        "===============================\n"
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
            "Distância:",
            item["distancia"]
        )


        print(
            item["texto"]
        )


        print(
            "-" * 50
        )