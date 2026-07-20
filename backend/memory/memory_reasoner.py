"""
Draco AI - Memory Reasoner

Motor de raciocínio sobre memória.

Responsabilidades:
- Consultar relações do memory_graph
- Transformar relações em conhecimento
- Aplicar regras cognitivas
"""


from backend.memory.memory_graph import buscar_relacoes

from backend.memory.memory_reasoning_rules import aplicar_regras





# =====================================
# Analisar relações da memória
# =====================================

def analisar_relacoes(entidade):


    relacoes = buscar_relacoes(
        entidade
    )


    if not relacoes:

        return []



    conhecimentos = []



    for relacao in relacoes:


        conhecimentos.append({

            "origem": relacao["origem"],

            "relacao": relacao["relacao"],

            "destino": relacao["destino"]

        })


    return conhecimentos





# =====================================
# Gerar explicações diretas
# =====================================

def gerar_expressoes(entidade):


    relacoes = analisar_relacoes(
        entidade
    )


    if not relacoes:

        return []



    respostas = []



    for item in relacoes:


        origem = item["origem"]

        relacao = item["relacao"]

        destino = item["destino"]



        if relacao == "criador":


            respostas.append(

                f"{origem} criou {destino}."

            )



        elif relacao == "objetivo":


            respostas.append(

                f"O objetivo de {origem} é {destino}."

            )



        elif relacao == "desenvolvimento_atual":


            respostas.append(

                f"{origem} está desenvolvendo {destino}."

            )



        else:


            respostas.append(

                f"{origem} possui relação "
                f"{relacao} com {destino}."

            )



    return respostas





# =====================================
# Criar inferências usando regras
# =====================================

def criar_inferencias(entidade):


    relacoes = analisar_relacoes(
        entidade
    )


    if not relacoes:

        return []



    inferencias = aplicar_regras(
        relacoes
    )


    return inferencias





# =====================================
# Raciocínio completo
# =====================================

def raciocinar(entidade):


    resultado = []



    # Conhecimento direto

    expressoes = gerar_expressoes(
        entidade
    )


    if expressoes:

        resultado.extend(
            expressoes
        )



    # Conhecimento inferido

    inferencias = criar_inferencias(
        entidade
    )


    if inferencias:

        resultado.extend(
            inferencias
        )



    return "\n".join(resultado)





# =====================================
# Teste manual
# =====================================

if __name__ == "__main__":


    resposta = raciocinar(
        "Draco AI"
    )


    print(resposta)