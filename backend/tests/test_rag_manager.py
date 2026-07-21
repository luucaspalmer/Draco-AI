import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


from backend.rag.rag_manager import rag_manager



def run_test():


    print()
    print("=" * 70)
    print("TESTE RAG MANAGER - DRACO AI")
    print("=" * 70)



    pergunta = "Quem é Aldorion?"



    print()
    print("Pergunta:")
    print(pergunta)



    contexto = rag_manager.buscar_contexto(
        pergunta
    )



    print()
    print("Resultado:")
    print(contexto)



    if contexto:

        print()
        print("STATUS: RAG ENCONTROU CONTEXTO")

    else:

        print()
        print("STATUS: RAG NÃO ENCONTROU CONTEXTO")



if __name__ == "__main__":

    run_test()