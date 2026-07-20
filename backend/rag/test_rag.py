from sentence_transformers import SentenceTransformer


print("Carregando modelo de embeddings...")


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


texto = "Draco AI é um assistente pessoal inteligente"


vetor = model.encode(texto)


print("Texto:")
print(texto)


print("\nTamanho do vetor:")
print(len(vetor))


print("\nPrimeiros valores:")
print(vetor[:5])