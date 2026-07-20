"""
Draco AI - Graph Query

Interpreta perguntas relacionadas ao
modelo de mundo e consulta o memory_graph.
"""


from backend.memory.memory_graph import (
    listar_entidades,
    buscar_relacoes
)



# =====================================
# Encontrar entidades na pergunta
# =====================================

def encontrar_entidades(pergunta):

    entidades = listar_entidades()

    encontradas = []


    pergunta_lower = pergunta.lower()


    for entidade in entidades:

        if entidade.lower() in pergunta_lower:

            encontradas.append(entidade)


    return encontradas



# =====================================
# Consultar grafo
# =====================================

def consultar_grafo(pergunta):

    entidades = encontrar_entidades(
        pergunta
    )


    if not entidades:

        return None


    contexto = []


    for entidade in entidades:

        relacoes = buscar_relacoes(
            entidade
        )


        for relacao in relacoes:


            frase = (
                f"{relacao['origem']} "
                f"{relacao['relacao']} "
                f"{relacao['destino']}."
            )


            # Evita relações duplicadas

            if frase not in contexto:

                contexto.append(
                    frase
                )


    if not contexto:

        return None


    return "\n".join(contexto)



# =====================================
# Teste manual
# =====================================

if __name__ == "__main__":


    pergunta = (
        "Explique a relação "
        "entre Lucas e Draco AI"
    )


    resposta = consultar_grafo(
        pergunta
    )


    print(resposta)