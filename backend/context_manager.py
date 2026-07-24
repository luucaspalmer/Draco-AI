"""
Draco AI
Context Manager

Ponto de entrada usado por brain.py para obter o
plano de contexto de uma pergunta:

    ContextManager().decidir_contexto(pergunta, intencao, rota_pergunta)

--------------------------------------------------------
IMPORTANTE
--------------------------------------------------------

A partir desta versão, a decisão real de QUAIS blocos
usar e EM QUE QUANTIDADE é feita pelo Context Attention
Manager (backend/memory/context_attention.py), que é
mais granular: escolhe a categoria de memória certa,
limita o histórico e limita tamanho/quantidade do RAG.

Este arquivo foi mantido (mesmo nome de classe e mesma
assinatura de método) apenas para não exigir nenhuma
alteração em brain.py nem em nenhum outro chamador
existente. Toda a arquitetura anterior continua
funcionando; apenas a decisão ficou mais inteligente.
"""

from backend.memory.context_attention import decidir_atencao


class ContextManager:

    def decidir_contexto(
        self,
        pergunta,
        intencao,
        rota_pergunta=None
    ):

        plano = decidir_atencao(
            pergunta,
            intencao,
            rota_pergunta
        )

        print("\n====== CONTEXT ATTENTION ======")

        print(f"Motivo: {plano.get('motivo')}")

        print(
            "Identidade:", plano.get("usar_identidade"),
            "| Memória:", plano.get("usar_memoria"),
            plano.get("memoria_categorias"),
            "| Histórico:", plano.get("historico_limite"),
            "| RAG:", plano.get("usar_rag"),
            plano.get("rag_limite")
        )

        print("================================\n")

        return plano
