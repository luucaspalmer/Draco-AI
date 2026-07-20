"""
Draco AI - Graph Reasoner

Interpreta relações do memory_graph
e transforma em contexto cognitivo.
"""


from backend.memory.memory_graph import buscar_relacoes



def gerar_contexto_grafo(entidade):

    relacoes = buscar_relacoes(entidade)


    if not relacoes:
        return None


    contexto = []


    for item in relacoes:

        origem = item["origem"]
        relacao = item["relacao"]
        destino = item["destino"]


        frase = (
            f"{origem} possui relação "
            f"'{relacao}' com {destino}."
        )


        contexto.append(frase)


    return "\n".join(contexto)



if __name__ == "__main__":


    resultado = gerar_contexto_grafo(
        "Draco AI"
    )


    print(resultado)