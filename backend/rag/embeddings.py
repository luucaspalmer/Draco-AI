"""
Draco AI
Embedding Manager

Responsável por transformar textos
em vetores semânticos.
"""


from sentence_transformers import SentenceTransformer


# =====================================
# Configuração do modelo
# =====================================

MODEL_NAME = "all-MiniLM-L6-v2"


# =====================================
# Carregamento do modelo
# =====================================

_model = SentenceTransformer(
    MODEL_NAME
)



# =====================================
# Gerar embedding de um texto
# =====================================

def gerar_embedding(texto):

    vetor = _model.encode(
        texto
    )

    return vetor.tolist()



# =====================================
# Gerar embeddings de vários textos
# =====================================

def gerar_embeddings(textos):

    vetores = _model.encode(
        textos
    )

    return vetores.tolist()



# =====================================
# Teste
# =====================================

if __name__ == "__main__":

    texto = (
        "O Draco AI é um assistente pessoal."
    )


    vetor = gerar_embedding(
        texto
    )


    print(
        "Texto:"
    )

    print(
        texto
    )


    print(
        "\nTamanho do vetor:"
    )

    print(
        len(vetor)
    )


    print(
        "\nPrimeiros valores:"
    )

    print(
        vetor[:5]
    )