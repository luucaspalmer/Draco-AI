"""
Draco AI - Memory Attention V4

Sistema de atenção cognitiva contextual.

Decide quais memórias devem receber
prioridade baseado em:

- importância histórica
- pergunta atual
- intenção da pergunta
- frequência de uso
- grafo cognitivo
- camada da memória

Não altera memória.
Apenas calcula relevância.
"""


from backend.intelligence.regression_predictor import (
    predictor
)


# =====================================
# Usage Logger
# =====================================

try:

    from backend.intelligence.usage_logger import (
        contar_recuperacoes
    )

except Exception:

    def contar_recuperacoes(chave):
        return 0



# =====================================
# Grafo cognitivo
# =====================================

try:

    from backend.memory.memory_graph import (
        buscar_relacoes
    )

except Exception:

    def buscar_relacoes(entidade):
        return []



# =====================================
# Intent
#
# FIX: intent_ai.py expõe "identificar_intencao_ai",
# não "classificar_intencao". Sem este ajuste, o import
# sempre falhava e o bônus de intenção ficava inerte
# (sempre neutro, valor 1).
# =====================================

try:

    from backend.intent_ai import (
        identificar_intencao_ai as classificar_intencao
    )

except Exception:

    def classificar_intencao(pergunta):

        return None



# =====================================
# Pesos das camadas
# =====================================


LAYER_WEIGHTS = {

    "PERMANENTE": 1.30,

    "PROJETO": 1.25,

    "PREFERENCIA": 1.20,

    "CONHECIMENTO": 1.10,

    "CONVERSA": 0.90

}



# =====================================
# Intenção -> camada
# =====================================


INTENT_WEIGHTS = {


    "pessoal": {

        "PERMANENTE": 1.3,
        "PREFERENCIA": 1.2

    },


    "projeto": {

        "PROJETO": 1.4

    },


    "conhecimento": {

        "CONHECIMENTO": 1.3

    },


    "conversa": {

        "CONVERSA": 1.2

    }

}




# =====================================
# Similaridade simples
# =====================================


def calcular_similaridade(
        pergunta,
        valor
):

    """
    Similaridade lexical simples.

    Futuramente pode trocar por embeddings.
    """

    if not pergunta or not valor:

        return 0



    pergunta = str(pergunta).lower()

    valor = str(valor).lower()



    palavras_pergunta = set(
        pergunta.split()
    )


    palavras_valor = set(
        valor.split()
    )


    intersecao = (
        palavras_pergunta
        &
        palavras_valor
    )


    if not palavras_valor:

        return 0



    return min(
        len(intersecao)
        /
        len(palavras_valor),

        1
    )



# =====================================
# Frequência
# =====================================


def calcular_frequencia(
        chave
):


    try:

        usos = contar_recuperacoes(
            chave
        )

    except Exception:

        usos = 0



    return min(
        usos / 100,
        1
    )



# =====================================
# Grafo
# =====================================


def calcular_bonus_grafo(
        valor
):


    try:

        relacoes = buscar_relacoes(
            valor
        )


        if relacoes:

            return 1


    except Exception:

        pass


    return 0




# =====================================
# Peso intenção
# =====================================


def calcular_bonus_intencao(
        camada,
        pergunta
):


    try:

        intencao = classificar_intencao(
            pergunta
        )


    except Exception:

        return 1



    regras = INTENT_WEIGHTS.get(
        intencao,
        {}
    )


    return regras.get(
        camada,
        1
    )




# =====================================
# Score V4
# =====================================


def calcular_atencao_v4(
        camada,
        chave,
        registro,
        pergunta
):


    valor = registro.get(
        "valor",
        ""
    )



    # -----------------------------
    # Modelo ML
    # -----------------------------

    try:

        score_modelo = predictor.prever_relevancia(
            registro
        )

    except Exception:

        score_modelo = 0



    # -----------------------------
    # Pergunta
    # -----------------------------

    score_pergunta = calcular_similaridade(
        pergunta,
        valor
    )



    # -----------------------------
    # Camada
    # -----------------------------

    score_camada = min(
        LAYER_WEIGHTS.get(
            camada,
            1
        )
        /
        1.30,

        1
    )



    # -----------------------------
    # Uso
    # -----------------------------

    score_uso = calcular_frequencia(
        chave
    )



    # -----------------------------
    # Grafo
    # -----------------------------

    score_grafo = calcular_bonus_grafo(
        valor
    )



    # -----------------------------
    # Intenção
    # -----------------------------

    bonus_intencao = calcular_bonus_intencao(
        camada,
        pergunta
    )



    # -----------------------------
    # Combinação final
    # -----------------------------

    score = (

        score_modelo * 0.35

        +

        score_pergunta * 0.25

        +

        score_camada * 0.15

        +

        score_uso * 0.10

        +

        score_grafo * 0.10

    )


    score *= bonus_intencao



    return round(
        min(score,1),
        3
    )




# =====================================
# Analisa camada
# =====================================


def analisar_camada(
        camada,
        memoria,
        pergunta
):


    resultado = {}


    if not isinstance(
        memoria,
        dict
    ):

        return resultado



    for chave, registro in memoria.items():


        # ignora formatos inválidos

        if not isinstance(
            registro,
            dict
        ):

            continue



        resultado[chave] = {


            "valor":
                registro.get(
                    "valor",
                    ""
                ),


            "relevancia":
                calcular_atencao_v4(
                    camada,
                    chave,
                    registro,
                    pergunta
                )

        }


    return resultado




# =====================================
# Aplicar Attention
# =====================================


def aplicar_memory_attention(
        memoria_total,
        pergunta=""
):


    resultado = {}



    for camada, memoria in memoria_total.items():


        resultado.update(

            analisar_camada(
                camada,
                memoria,
                pergunta
            )

        )



    return dict(

        sorted(

            resultado.items(),

            key=lambda item:
                item[1]["relevancia"],

            reverse=True

        )

    )




# =====================================
# Compatibilidade
# =====================================


def selecionar_memorias_relevantes(
        memoria_total,
        pergunta="",
        limite=10
):


    ranking = aplicar_memory_attention(
        memoria_total,
        pergunta
    )


    return dict(
        list(
            ranking.items()
        )[:limite]
    )




# =====================================
# Teste
# =====================================


if __name__ == "__main__":


    teste = {


        "PERMANENTE": {


            "nome": {

                "valor":
                    "Lucas",

                "importancia":
                    10,

                "confianca":
                    1

            }

        },


        "PROJETO": {


            "draco": {


                "valor":
                    "Draco AI",

                "importancia":
                    9,

                "confianca":
                    1

            }

        }

    }



    print(
        aplicar_memory_attention(
            teste,
            "Qual meu nome?"
        )
    )
