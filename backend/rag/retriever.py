from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer



# =====================================
# Configuração
# =====================================

VECTOR_DB_PATH = Path(
    "data/knowledge/vector_db"
)


COLLECTION_NAME = "draco_knowledge"



# =====================================
# Modelo de embeddings
# =====================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



# =====================================
# Conectar ao banco
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

    vetor_pergunta = embedding_model.encode(
        pergunta
    ).tolist()


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
        "O que é Python?"
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