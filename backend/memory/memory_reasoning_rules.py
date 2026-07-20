"""
Draco AI - Memory Reasoning Rules

Biblioteca de regras cognitivas.

Contém padrões de inferência
usados pelo Memory Reasoner.
"""




# =====================================
# Regra:
# Criador + Objetivo
# =====================================

def regra_criador_objetivo(relacoes):


    criador = None

    objetivo = None



    for relacao in relacoes:


        if relacao["relacao"] == "criador":

            criador = relacao



        if relacao["relacao"] == "objetivo":

            objetivo = relacao





    if criador and objetivo:


        return (

            f"{criador['origem']} criou "
            f"{criador['destino']} com o objetivo "
            f"de desenvolver "
            f"{objetivo['destino']}."

        )


    return None





# =====================================
# Executar todas as regras
# =====================================

def aplicar_regras(relacoes):


    inferencias = []



    regras = [

        regra_criador_objetivo

    ]



    for regra in regras:


        resultado = regra(
            relacoes
        )


        if resultado:

            inferencias.append(
                resultado
            )



    return inferencias