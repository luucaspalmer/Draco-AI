"""
Draco AI
Document Loader

Responsável por carregar todos os documentos
da base de conhecimento.
"""

from pathlib import Path


# =====================================
# Caminho da base de conhecimento
# =====================================

KNOWLEDGE_PATH = Path(
    "data/knowledge/documents"
)


# =====================================
# Carregar documentos
# =====================================

def carregar_documentos():

    documentos = []

    # Procura arquivos .txt em todas as subpastas
    for arquivo in sorted(
        KNOWLEDGE_PATH.rglob("*.txt")
    ):

        texto = arquivo.read_text(
            encoding="utf-8"
        ).strip()

        # Ignora arquivos vazios
        if not texto:
            continue

        documentos.append(
            {
                "nome": arquivo.name,
                "caminho": str(
                    arquivo.relative_to(KNOWLEDGE_PATH)
                ),
                "texto": texto
            }
        )

    return documentos


# =====================================
# Teste
# =====================================

if __name__ == "__main__":

    docs = carregar_documentos()

    print(
        f"\n{len(docs)} documentos encontrados.\n"
    )

    for doc in docs:

        print("=" * 60)
        print(f"Arquivo : {doc['nome']}")
        print(f"Caminho : {doc['caminho']}")
        print("-" * 60)
        print(doc["texto"])
        print()