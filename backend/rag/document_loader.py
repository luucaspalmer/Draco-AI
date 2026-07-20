from pathlib import Path


KNOWLEDGE_PATH = Path(
    "data/knowledge/documents"
)


def carregar_documentos():

    documentos = []

    for arquivo in KNOWLEDGE_PATH.glob("*.txt"):

        texto = arquivo.read_text(
            encoding="utf-8"
        )

        documentos.append(
            {
                "nome": arquivo.name,
                "texto": texto
            }
        )

    return documentos



if __name__ == "__main__":

    docs = carregar_documentos()

    print(
        f"{len(docs)} documentos encontrados"
    )

    for doc in docs:

        print("\nArquivo:")
        print(doc["nome"])

        print(
            doc["texto"]
        )