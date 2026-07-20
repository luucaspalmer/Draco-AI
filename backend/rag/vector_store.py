"""
=====================================
Draco AI
Vector Store
=====================================

Responsável pelo armazenamento
do conhecimento vetorial no ChromaDB.

Fluxo:

Documentos
    ↓
Embeddings
    ↓
ChromaDB

Modo atual:
- Reconstrói a base automaticamente
- Remove duplicatas
- Mantém sincronização com arquivos
"""

from pathlib import Path

import chromadb


from backend.rag.document_loader import (
    carregar_documentos
)


from backend.rag.embeddings import (
    gerar_embedding
)



# =====================================
# Configuração
# =====================================

VECTOR_DB_PATH = Path(
    "data/knowledge/vector_db"
)


COLLECTION_NAME = (
    "draco_knowledge"
)



# =====================================
# Banco vetorial
# =====================================

client = chromadb.PersistentClient(
    path=str(VECTOR_DB_PATH)
)



# =====================================
# Criar / recriar coleção
# =====================================

def criar_collection():

    try:

        client.delete_collection(
            name=COLLECTION_NAME
        )

        print(
            "Coleção antiga removida"
        )


    except Exception:

        pass



    collection = client.create_collection(
        name=COLLECTION_NAME
    )


    print(
        "Nova coleção criada"
    )


    return collection



# =====================================
# Indexar documentos
# =====================================

def adicionar_documentos():


    collection = criar_collection()


    documentos = carregar_documentos()


    textos = []

    ids = []

    embeddings = []

    metadados = []



    for doc in documentos:


        nome = doc["nome"]

        texto = doc["texto"]



        print(
            f"Indexando: {nome}"
        )



        vetor = gerar_embedding(
            texto
        )



        textos.append(
            texto
        )


        embeddings.append(
            vetor
        )


        # ID estável baseado no arquivo
        ids.append(
            nome
        )


        metadados.append(
            {
                "origem": nome
            }
        )



    collection.add(

        documents=textos,

        embeddings=embeddings,

        ids=ids,

        metadatas=metadados

    )



    print(
        f"\n{len(textos)} documentos adicionados ao Draco"
    )



# =====================================
# Teste
# =====================================

if __name__ == "__main__":

    adicionar_documentos()