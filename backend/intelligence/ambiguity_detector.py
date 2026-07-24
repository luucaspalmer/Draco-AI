"""
Draco AI - Intelligence / Ambiguity Detector

Identifica perguntas ou instruções incompletas, onde falta
um referente claro (pronomes soltos, pedidos vagos de
melhoria/correção etc).

Atua apenas em casos claramente vagos, para não interromper
conversas normais com perguntas de esclarecimento
desnecessárias.
"""

import re


# =====================================
# Pronomes/referências sem antecedente
# =====================================

PRONOMES_SEM_REFERENCIA = (

    "isso",

    "aquilo",

    "isso ai",

    "isso aí",

    "ele",

    "ela",

    "eles",

    "elas",

    "aquele",

    "aquela",

    "esse lance",

    "essa parada",

    "esse negocio",

    "esse negócio",

    "aquilo que",

    "aquilo la",

    "aquilo lá"

)


# =====================================
# Pedidos vagos de ação
# =====================================

PEDIDOS_VAGOS = (

    "pode melhorar",

    "melhora isso",

    "conserta isso",

    "corrige isso",

    "faz de novo",

    "tenta de novo",

    "não ficou bom",

    "nao ficou bom",

    "não gostei",

    "nao gostei",

    "faz melhor"

)


LIMITE_PALAVRAS_CURTAS = 6


# =====================================
# Normalização
# =====================================

def normalizar(texto):

    texto = texto.lower().strip()

    texto = re.sub(
        r"[?!.,;:]+",
        "",
        texto
    )

    return texto


def contem_referencia_vaga(texto):

    for termo in PRONOMES_SEM_REFERENCIA:

        if termo in texto:

            return True

    return False


def contem_pedido_vago(texto):

    for termo in PEDIDOS_VAGOS:

        if termo in texto:

            return True

    return False


# =====================================
# Pergunta de esclarecimento
# =====================================

def gerar_pergunta_esclarecimento(pergunta_original):

    return (
        "Só para eu não te responder algo errado: "
        "você pode me dizer especificamente a que ou a quem "
        "você está se referindo?"
    )


# =====================================
# Detector principal
# =====================================

def detectar_ambiguidade(pergunta, dados_pergunta=None):
    """
    Retorna (ambiguo: bool, pergunta_esclarecimento: str | None)
    """

    if not pergunta or not pergunta.strip():

        return False, None

    texto = normalizar(pergunta)

    palavras = texto.split()

    entidade = ""

    if dados_pergunta:

        entidade = dados_pergunta.get("entity", "") or ""

    # Já existe uma entidade resolvida pelo Question Analyzer,
    # então não tratamos como ambíguo.
    if entidade.strip():

        return False, None

    pedido_vago = contem_pedido_vago(texto)

    referencia_vaga = contem_referencia_vaga(texto)

    if not pedido_vago and not referencia_vaga:

        return False, None

    # Mensagens longas normalmente trazem contexto suficiente,
    # a não ser que sejam um pedido vago de correção/melhoria.
    if len(palavras) > LIMITE_PALAVRAS_CURTAS and not pedido_vago:

        return False, None

    return True, gerar_pergunta_esclarecimento(pergunta)


# =====================================
# Teste manual
# =====================================

if __name__ == "__main__":

    testes = [

        "Como faço isso?",

        "Ele falou aquilo.",

        "Pode melhorar?",

        "Qual meu nome?",

        "Explique inteligência artificial para uma criança."

    ]

    for teste in testes:

        print(teste, "->", detectar_ambiguidade(teste))
