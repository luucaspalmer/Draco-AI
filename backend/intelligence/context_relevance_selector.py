"""
Draco AI - Intelligence / Context Relevance Selector

Adapta o memory_attention.py já existente (V4) para reduzir
o contexto de memória enviado ao prompt, mantendo o MESMO
formato hierárquico que memory_manager / context_builder /
memory_formatter já esperam:

    { "PERMANENTE": {chave: registro}, "PROJETO": {...}, ... }

Não recria o cálculo de relevância: usa
memory_attention.analisar_camada apenas para pontuar, e filtra
o dicionário original (com "valor", "importancia", "confianca",
"criado_em" etc. intactos) mantendo só as chaves mais
relevantes por camada.

Também fecha o ciclo do usage_logger.py: registra quais
chaves foram selecionadas para a pergunta atual, alimentando
a "fase 2" de treino com dados reais já prevista nesse módulo.
"""

from backend.intelligence.memory_attention import analisar_camada

try:

    from backend.intelligence.usage_logger import registrar_uso

except Exception:

    def registrar_uso(*args, **kwargs):

        return False


# Camadas que possuem o formato {chave: registro} e podem
# ser pontuadas pelo memory_attention. "CONVERSA" tem outro
# formato (lista de mensagens) e não é tocada aqui.
CAMADAS_FILTRAVEIS = (

    "PERMANENTE",

    "PROJETO",

    "PREFERENCIA",

    "CONHECIMENTO"

)


def filtrar_memoria_relevante(

    memoria_hierarquica,

    pergunta="",

    limite_por_camada=5,

    origem_log="intelligence"

):
    """
    Args:
        memoria_hierarquica: dict no formato retornado por
            memory_manager.obter_memoria_contexto()
        pergunta: pergunta atual do usuário
        limite_por_camada: quantos registros manter por camada
        origem_log: valor gravado no usage_logger

    Returns:
        dict no mesmo formato de entrada, com cada camada
        filtrável reduzida às chaves mais relevantes.
    """

    if not isinstance(memoria_hierarquica, dict):

        return memoria_hierarquica

    # Preserva camadas não filtráveis (ex: CONVERSA) intactas
    resultado = dict(memoria_hierarquica)

    for camada in CAMADAS_FILTRAVEIS:

        registros_originais = memoria_hierarquica.get(camada)

        if not isinstance(registros_originais, dict) or not registros_originais:

            continue

        try:

            scores = analisar_camada(

                camada,

                registros_originais,

                pergunta

            )

        except Exception:

            # Se o cálculo de relevância falhar por qualquer
            # motivo, preserva a camada original sem filtrar.
            continue

        chaves_ordenadas = sorted(

            scores.keys(),

            key=lambda chave: scores[chave]["relevancia"],

            reverse=True

        )

        chaves_selecionadas = chaves_ordenadas[:limite_por_camada]

        camada_filtrada = {

            chave: registros_originais[chave]

            for chave in chaves_selecionadas

            if chave in registros_originais

        }

        resultado[camada] = camada_filtrada

        try:

            registrar_uso(

                pergunta=pergunta,

                categoria=camada,

                chaves=chaves_selecionadas,

                origem=origem_log

            )

        except Exception:

            pass

    return resultado


# =====================================
# Teste manual
# =====================================

if __name__ == "__main__":

    exemplo = {

        "PERMANENTE": {

            "nome": {
                "valor": "Lucas",
                "importancia": 10,
                "confianca": 1.0
            },

            "localizacao": {
                "valor": "Araucária, Paraná",
                "importancia": 8,
                "confianca": 1.0
            }

        },

        "CONVERSA": {

            "history": []

        }

    }

    print(

        filtrar_memoria_relevante(

            exemplo,

            "Qual meu nome?",

            limite_por_camada=1

        )

    )
