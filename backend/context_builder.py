from backend.identity import get_identity

from backend.memory.memory_manager import (
    obter_memoria_contexto
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
    # Memória
    # =====================================

    resultado_memoria = {}

    if plano.get("usar_memoria", False):

        memoria_hierarquica = obter_memoria_contexto() or {}

        contexto["memoria_hierarquica"] = memoria_hierarquica

        contexto["personalidade"] = memoria_hierarquica.get(
            "PREFERENCIA",
            {}
        )

        resultado_memoria = buscar_memorias(
            pergunta
        ) or {}

        contexto["memorias"] = resultado_memoria.get(
            "memoria",
            {}
        )

        contexto["memoria_info"] = {

            "categoria": resultado_memoria.get(
                "categoria"
            ),

            "confianca": resultado_memoria.get(
                "confianca",
                0
            ),

            "origem": resultado_memoria.get(
                "origem"
            )

        }

        print(
            f"Categorias da memória: {list(memoria_hierarquica.keys())}"
        )

        print(
            f"Memória encontrada: {resultado_memoria.get('categoria')}"
        )

        print(
            f"Confiança: {resultado_memoria.get('confianca', 0)}"
        )

    else:

        print("Memória: Ignorada")

    # =====================================
    # Projetos
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
    # =====================================

    if plano.get("usar_conversa", False):

        historico = obter_historico()[-10:]

        contexto["historico"] = historico

        print(
            f"Histórico: {len(historico)} mensagens"
        )

    else:

        print("Histórico: Ignorado")

    # =====================================
    # RAG
    # =====================================

    if plano.get("usar_rag", False):

        try:

            contexto_rag = rag_manager.buscar_contexto(
                pergunta
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