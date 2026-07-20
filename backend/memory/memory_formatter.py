"""
Draco AI - Memory Formatter

Transforma memória estrutural do Draco
em contexto cognitivo legível pelo modelo.

Entrada:
JSON de memória

Saída:
Texto interpretável pelo LLM
"""


# =====================================
# Formatar um registro individual
# =====================================

def formatar_registro(
    chave,
    registro
):


    if not isinstance(registro, dict):

        return None



    valor = registro.get(
        "valor"
    )



    if valor is None:

        return None



    chave = chave.lower()



    # -------------------------------
    # Informações pessoais
    # -------------------------------


    if chave == "idade":

        return (
            f"O usuário tem {valor} anos."
        )



    if chave == "localizacao":

        return (
            f"O usuário mora em {valor}."
        )



    if chave == "nome":

        return (
            f"O nome do usuário é {valor}."
        )





    # -------------------------------
    # Projetos
    # -------------------------------


    if chave.startswith(
        "projeto"
    ):

        return (
            f"O usuário possui o projeto: {valor}."
        )





    # -------------------------------
    # Conhecimentos
    # -------------------------------


    if (
        "interesse" in chave
        or
        "conhecimento" in chave
        or
        "outras_memoria" in chave
    ):

        return (
            f"O usuário possui conhecimento ou interesse em {valor}."
        )





    # -------------------------------
    # Geral
    # -------------------------------


    return (
        f"Informação conhecida sobre o usuário: {valor}."
    )









# =====================================
# Formatar uma camada
# =====================================

def formatar_camada(
    nome_camada,
    dados
):


    resultado = []



    if not dados:

        return resultado



    for chave, registro in dados.items():


        frase = formatar_registro(
            chave,
            registro
        )



        if frase:

            resultado.append(
                frase
            )



    return resultado







# =====================================
# Formatar memória completa
# =====================================

def formatar_memoria(
    memoria
):


    contexto = []



    if not memoria:

        return ""





    contexto.append(
        "=== FATOS CONHECIDOS SOBRE O USUÁRIO ==="
    )


    contexto.append(
        """
As informações abaixo foram aprendidas
pelo Draco durante conversas anteriores.

Elas representam conhecimento persistente
sobre o usuário.

Quando uma pergunta estiver relacionada
ao usuário, utilize essas informações.
"""
    )





    for camada, dados in memoria.items():


        if camada == "CONVERSA":

            continue



        contexto.append(
            f"\n[{camada}]"
        )



        frases = formatar_camada(
            camada,
            dados
        )



        for frase in frases:


            contexto.append(
                "- " + frase
            )





    return "\n".join(
        contexto
    )