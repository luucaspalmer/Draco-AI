"""
Draco AI
Context Builder

Monta o dicionário de contexto que o prompt_builder.py
vai transformar em texto.

--------------------------------------------------------
Mudança principal
--------------------------------------------------------

Antes: quando `usar_memoria=True`, sempre carregava as
4 camadas inteiras de memória via `obter_memoria_contexto()`,
independente da pergunta.

Agora: usa `plano["memoria_categorias"]`, calculado pelo
Context Attention Manager, para carregar só a(s) camada(s)
relevante(s) via `carregar_camada(tipo)`. Se o plano não
especificar categorias (fallback), mantém o comportamento
antigo (memória completa) para não quebrar nenhum caso de uso.

O mesmo princípio se aplica ao histórico (tamanho definido
pelo plano) e ao RAG (quantidade e tamanho por chunk
definidos pelo plano).
"""

from backend.identity import get_identity

from backend.memory.memory_manager import (
    obter_memoria_contexto,
    carregar_camada
)

from backend.memory.memory_search import (
    buscar_memorias
)

from backend.conversation_memory import (
    obter_historico
)

from backend.rag.rag_manager import (
    rag_manager
)


# =====================================
# Construção do contexto
# =====================================

def construir_contexto(pergunta, plano):

    contexto = {
        "pergunta": pergunta
    }

    # =====================================
    # Identidade
    # =====================================

    if plano.get("usar_identidade", False):

        identidade = get_identity()

        contexto["identidade"] = identidade

        print("Identidade: OK")

    else:

        print("Identidade: Ignorada")

    # =====================================
    # Memória (agora seletiva por categoria)
    # =====================================

    resultado_memoria = {}

    if plano.get("usar_memoria", False):

        categorias = plano.get("memoria_categorias") or []

        if categorias:

            memoria_hierarquica = {
                tipo: carregar_camada(tipo)
                for tipo in categorias
            }

        else:

            # Fallback: sem categoria específica -> memória completa
            # (comportamento antigo, preservado para casos como
            # "mostre tudo que você sabe sobre mim")

            memoria_hierarquica = obter_memoria_contexto() or {}

        contexto["memoria_hierarquica"] = memoria_hierarquica

        contexto["personalidade"] = memoria_hierarquica.get(
            "PREFERENCIA",
            {}
        )

        print(
            f"Memória: camadas carregadas -> {list(memoria_hierarquica.keys())}"
        )

    else:

        print("Memória: Ignorada")

    # =====================================
    # Projetos (mantido por compatibilidade)
    #
    # OBS: este bloco não é consumido pelo prompt_builder.py
    # atual (é usado apenas por integrações futuras / debug),
    # então não impacta o tamanho do prompt enviado ao Qwen.
    # =====================================

    if plano.get("usar_projetos", False):

        if not resultado_memoria:

            resultado_memoria = buscar_memorias(
                pergunta
            ) or {}

        contexto["projetos"] = resultado_memoria.get(
            "memoria",
            {}
        )

        print("Projetos: OK")

    else:

        print("Projetos: Ignorados")

    # =====================================
    # Histórico
    #
    # Tamanho decidido pelo Context Attention Manager
    # (plano["historico_limite"]) em vez do valor fixo
    # de 10 mensagens usado anteriormente.
    # =====================================

    if plano.get("usar_conversa", False):

        limite = plano.get("historico_limite", 4)

        historico = obter_historico()[-limite:] if limite else []

        contexto["historico"] = historico

        print(
            f"Histórico: {len(historico)} mensagens (limite {limite})"
        )

    else:

        print("Histórico: Ignorado")

    # =====================================
    # RAG
    #
    # Quantidade de chunks e tamanho máximo por chunk
    # agora são decididos pelo plano de atenção, evitando
    # que documentos inteiros sejam despejados no prompt.
    # =====================================

    if plano.get("usar_rag", False):

        try:

            limite = plano.get("rag_limite", 3)

            max_chars = plano.get("rag_max_chars", 700)

            contexto_rag = rag_manager.buscar_contexto(
                pergunta,
                limite=limite,
                max_chars=max_chars
            )

            contexto["rag"] = contexto_rag

            if contexto_rag:

                print("RAG: Contexto encontrado")

            else:

                print("RAG: Nenhum contexto encontrado")

        except Exception as erro:

            contexto["rag"] = ""

            print(
                f"RAG: Erro ({erro})"
            )

    else:

        contexto["rag"] = ""

        print("RAG: Desativado")

    return contexto
