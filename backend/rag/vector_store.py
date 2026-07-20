from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from backend.rag.document_loader import carregar_documentos



# =====================================
# Configuração
# =====================================

VECTOR_DB_PATH = Path(
    "data/knowledge/vector_db"
)


COLLECTION_NAME = "draco_knowledge"



# =====================================
# Modelo de embedding
# =====================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



# =====================================
# Banco vetorial
# =====================================

client = chromadb.PersistentClient(
    path=str(VECTOR_DB_PATH)
)


collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)



# =====================================
# Adicionar documentos
# =====================================

def adicionar_documentos():

    documentos = carregar_documentos()


    textos = []
    ids = []
    embeddings = []
    metadados = []


    for index, doc in enumerate(documentos):

        texto = doc["texto"]


        vetor = embedding_model.encode(
            texto
        ).tolist()


        textos.append(texto)

        embeddings.append(vetor)

        ids.append(
            str(index)
        )

        metadados.append(
            {
                "origem": doc["nome"]
            }
        )


    collection.add(
        documents=textos,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadados
    )


    print(
        f"{len(textos)} documentos adicionados ao Draco"
    )



# =====================================
# Teste
# =====================================

if __name__ == "__main__":

    adicionar_documentos()