from backend.memory.memory_manager import (
    obter_memoria_contexto
)

from backend.intelligence.memory_attention import (
    selecionar_memorias_relevantes
)



print("==============================")
print("TESTE MEMORY ATTENTION REAL")
print("==============================")



memoria_total = obter_memoria_contexto()



for camada, memoria in memoria_total.items():


    print()

    print(
        "CAMADA:",
        camada
    )


    resultado = selecionar_memorias_relevantes(
        {
            camada: memoria
        },
        limite=10
    )


    if not resultado:

        print("Nenhuma memória encontrada")

        continue



    for chave, item in resultado.items():


        print()

        print(
            "Memória:",
            chave
        )


        print(
            "Valor:",
            item.get(
                "valor"
            )
        )


        print(
            "Score:",
            item.get(
                "relevancia"
            )
        )



print()

print("==============================")
print("TESTE FINALIZADO")
print("==============================")