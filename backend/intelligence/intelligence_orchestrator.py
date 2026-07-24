"""
Draco AI - Intelligence Orchestrator

Fachada única da camada de Intelligence. É o único ponto que
brain.py precisa conhecer: por baixo dele, orquestra:

- intent_analyzer      (intenção, complexidade, objetivo)
- ambiguity_detector    (pergunta de esclarecimento, se preciso)
- source_planner        (memória? RAG? identidade? combinação?)
- response_strategy     (como a resposta deve ser estruturada)
- context_relevance_selector (filtra memória antes do prompt)

A Intelligence NÃO gera respostas. Ela decide como o Draco
deve pensar antes de responder.
"""

from backend.intelligence.intent_analyzer import analisar_intencao
from backend.intelligence.ambiguity_detector import detectar_ambiguidade
from backend.intelligence.source_planner import planejar_fontes
from backend.intelligence.response_strategy import escolher_estrategia
from backend.intelligence.context_relevance_selector import (
    filtrar_memoria_relevante
)


class IntelligenceOrchestrator:

    # =====================================
    # Análise cognitiva completa
    # =====================================

    def analisar(self, pergunta, dados_pergunta, rota_pergunta, intencao):
        """
        Args:
            pergunta: texto original do usuário
            dados_pergunta: saída de question_analyzer.analyze_question
            rota_pergunta: saída de question_router.route_question
            intencao: intenção final já resolvida pelo brain.py

        Returns:
            {
                "precisa_esclarecimento": bool,
                "pergunta_esclarecimento": str | None,
                "analise_intencao": dict,
                "plano_contexto": dict | None,
                "estrategia_resposta": str | None
            }
        """

        analise_intencao = analisar_intencao(

            pergunta,

            dados_pergunta,

            intencao

        )

        ambiguo, pergunta_esclarecimento = detectar_ambiguidade(

            pergunta,

            dados_pergunta

        )

        if ambiguo:

            return {

                "precisa_esclarecimento": True,

                "pergunta_esclarecimento": pergunta_esclarecimento,

                "analise_intencao": analise_intencao,

                "plano_contexto": None,

                "estrategia_resposta": None

            }

        plano_contexto = planejar_fontes(

            pergunta,

            intencao,

            rota_pergunta,

            analise_intencao

        )

        estrategia_resposta = escolher_estrategia(

            intencao,

            analise_intencao.get("tipo_pergunta", "unknown"),

            analise_intencao.get("complexidade", "media")

        )

        return {

            "precisa_esclarecimento": False,

            "pergunta_esclarecimento": None,

            "analise_intencao": analise_intencao,

            "plano_contexto": plano_contexto,

            "estrategia_resposta": estrategia_resposta

        }

    # =====================================
    # Filtragem de memória relevante
    # =====================================

    def filtrar_memoria(self, memoria_hierarquica, pergunta):

        return filtrar_memoria_relevante(

            memoria_hierarquica,

            pergunta

        )


# =====================================
# Teste manual
# =====================================

if __name__ == "__main__":

    orquestrador = IntelligenceOrchestrator()

    resultado = orquestrador.analisar(

        "Qual meu nome?",

        {
            "question_type": "owner",
            "entity": "meu nome",
            "is_question": True
        },

        {"route": "memory"},

        "consultar_nome"

    )

    print(resultado)
