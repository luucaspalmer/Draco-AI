"""
Draco AI - Intelligence / Source Planner

Decide quais fontes de contexto devem ser usadas
(identidade, memória, projetos, RAG) e se é necessário
combinar mais de uma fonte na mesma resposta.

Não reimplementa a lógica de decisão por palavras-chave:
reutiliza o ContextManager já existente e apenas enriquece
o resultado, mantendo o mesmo formato de dicionário que
context_builder.construir_contexto já espera.
"""

from backend.context_manager import ContextManager


_context_manager = ContextManager()


CHAVES_FONTE = (

    "usar_identidade",

    "usar_memoria",

    "usar_projetos",

    "usar_rag"

)


def planejar_fontes(pergunta, intencao, rota_pergunta, analise_intencao=None):
    """
    Args:
        pergunta: texto original do usuário
        intencao: intenção final já resolvida
        rota_pergunta: saída do question_router
        analise_intencao: saída do intent_analyzer (opcional)

    Returns:
        dict no mesmo formato de ContextManager.decidir_contexto,
        acrescido de "fontes_combinadas".
    """

    plano = _context_manager.decidir_contexto(

        pergunta,

        intencao,

        rota_pergunta

    )

    fontes_ativas = [

        chave

        for chave in CHAVES_FONTE

        if plano.get(chave)

    ]

    plano["fontes_combinadas"] = len(fontes_ativas) > 1

    if (

        analise_intencao

        and analise_intencao.get("complexidade") == "alta"

    ):

        plano["motivo"] = (

            plano.get("motivo", "")

            + " + Intelligence: complexidade alta"

        )

    return plano


# =====================================
# Teste manual
# =====================================

if __name__ == "__main__":

    resultado = planejar_fontes(

        "Qual meu nome e qual meu projeto?",

        "consultar_memoria",

        {"route": "memory"},

        {"complexidade": "media"}

    )

    print(resultado)
