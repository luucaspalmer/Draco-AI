"""
Draco AI - Intelligence / Response Strategy

Decide COMO o Draco deve estruturar a resposta antes da
chamada à LLM (curta, técnica, didática, passo a passo etc).

A estratégia escolhida é apenas uma instrução textual que o
prompt_builder anexa ao prompt final. Este módulo não gera
texto de resposta, apenas a diretriz de formato.
"""


ESTRATEGIAS_POR_TIPO_PERGUNTA = {

    "definition": (
        "Responda de forma didática, como se estivesse explicando "
        "o conceito para alguém que está aprendendo o assunto agora. "
        "Comece pela ideia central antes de entrar em detalhes."
    ),

    "list": (
        "Responda organizando os itens em uma lista clara."
    ),

    "reason": (
        "Responda explicando a causa ou motivo de forma lógica e "
        "sequencial."
    ),

    "quantity": (
        "Responda de forma direta e objetiva, destacando o número "
        "ou quantidade solicitada."
    ),

    "location": (
        "Responda de forma curta e direta."
    ),

    "time": (
        "Responda de forma curta e direta."
    ),

    "event": (
        "Responda contando o que aconteceu de forma organizada, "
        "na ordem em que os fatos ocorreram."
    ),

    "relationship": (
        "Responda explicando a relação entre as entidades de forma "
        "clara."
    ),

    "owner": (
        "Responda de forma curta e direta, identificando o "
        "responsável."
    )

}


PREFIXOS_INTENCAO_CURTA = (

    "identidade_",

    "memoria_",

    "consultar_"

)


def escolher_estrategia(intencao, tipo_pergunta, complexidade):
    """
    Args:
        intencao: intenção final resolvida
        tipo_pergunta: question_type (definition/list/reason/...)
        complexidade: "baixa" | "media" | "alta"

    Returns:
        str com a instrução de estratégia, ou None quando não há
        nada relevante a acrescentar (resposta livre/conversa).
    """

    if intencao and any(

        intencao.startswith(prefixo)

        for prefixo in PREFIXOS_INTENCAO_CURTA

    ):

        return (
            "Responda de forma direta e objetiva, sem rodeios "
            "e sem se estender além do necessário."
        )

    estrategia = ESTRATEGIAS_POR_TIPO_PERGUNTA.get(tipo_pergunta)

    if complexidade == "alta":

        passo_a_passo = (
            "A pergunta é complexa: estruture a resposta em passo "
            "a passo ou em tópicos, cobrindo os pontos principais "
            "antes de aprofundar."
        )

        if estrategia:

            return estrategia + " " + passo_a_passo

        return passo_a_passo

    if estrategia:

        return estrategia

    if complexidade == "baixa":

        return "Responda de forma curta e natural."

    return None


# =====================================
# Teste manual
# =====================================

if __name__ == "__main__":

    print(escolher_estrategia("conversa", "definition", "media"))

    print(escolher_estrategia("identidade_nome", "person", "baixa"))

    print(escolher_estrategia("conversa", "unknown", "alta"))
