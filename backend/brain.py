from backend.commands import executar_comando

from backend.ollama_client import perguntar_ao_qwen

from backend.intents import identificar_intencao

from backend.intent_ai import identificar_intencao_ai

from backend.conversation_memory import adicionar_mensagem

from backend.context_builder import construir_contexto

from backend.prompt_builder import construir_prompt

from backend.intelligence.intelligence_orchestrator import (
    IntelligenceOrchestrator
)

from backend.tools.tool_manager import ToolManager


# Question Analyzer

from backend.question.question_analyzer import (
    analyze_question
)


# Question Router

from backend.question.question_router import (
    route_question
)


# Question Dispatcher

from backend.question.question_dispatcher import (
    dispatch_question
)


# Question Executor

from backend.question.question_executor import (
    execute_question
)


# Entity Resolver

from backend.question.entity_resolver import (
    resolve_entity
)


# Entity Classifier

from backend.question.entity_classifier import (
    classify_entity
)


# Response Planner

from backend.question.response_planner import (
    planejar_resposta
)


# Memória cognitiva

from backend.memory.memory_detector import (
    detectar_memoria,
    identificar_tipo_mensagem
)

from backend.memory.memory_controller import processar_memoria


# Raciocínio cognitivo

from backend.memory.memory_reasoner import raciocinar


# System Actions API

from backend.system.system_actions import process_text



# =====================================
# Aprendizado automático
# =====================================

def aprender_durante_conversa(pergunta):


    memoria_detectada = detectar_memoria(
        pergunta
    )


    if not memoria_detectada:

        return None



    print("\n====== MEMÓRIA DETECTADA ======")

    print(memoria_detectada)

    print("===============================\n")



    resultado = processar_memoria(
        pergunta
    )


    print("\n====== MEMÓRIA PROCESSADA ======")

    print(resultado)

    print("================================\n")


    return resultado




# =====================================
# Pensamento principal
# =====================================

def pensar(pergunta):


    pergunta = pergunta.strip()



    if not pergunta:

        return "Não recebi nenhuma mensagem."




    # =====================================
    # System Actions API
    #
    # Comandos de controle do sistema
    # operacional (abrir programas, etc.)
    # são interceptados aqui e NUNCA
    # chegam ao LLM.
    # =====================================

    resultado_sistema = process_text(
        pergunta
    )

    if resultado_sistema:

        print("\n====== SYSTEM ACTION DETECTADA ======")

        print(resultado_sistema)

        print("======================================\n")

        resposta_sistema = resultado_sistema.message

        adicionar_mensagem(
            "user",
            pergunta
        )

        adicionar_mensagem(
            "assistant",
            resposta_sistema
        )

        return resposta_sistema



    # =====================================
    # Question Analyzer
    # =====================================


    dados_pergunta = analyze_question(
        pergunta
    )




    # =====================================
    # Verificação de ferramentas
    # =====================================

    # =====================================
    # Entity Resolver
    # =====================================


    entidade_resolvida = resolve_entity(
        dados_pergunta["entity"]
    )


    print("\n====== ENTITY RESOLVER ======")

    print(entidade_resolvida)

    print("=============================\n")





# =====================================
# Entity Classifier
# =====================================


    classificacao_entidade = classify_entity(
        entidade_resolvida
    )


    print("\n====== ENTITY CLASSIFIER ======")

    print(classificacao_entidade)

    print("===============================\n")





# =====================================
# Question Router
# =====================================


    rota_pergunta = route_question(
        dados_pergunta,
        classificacao_entidade
    )


    print("\n====== QUESTION ROUTER ======")

    print(rota_pergunta)

    print("=============================\n")




# =====================================
# Response Planner
#
# Decide o ESTILO da resposta (DIRETA,
# EXPLICATIVA ou APROFUNDADA) antes de
# montar o contexto e o prompt.
#
# Perguntas que serão respondidas de forma
# imediata (identity/memory/tool "handled")
# não usam esse plano, pois nem chegam
# a montar prompt para o Qwen.
# =====================================

    # Resolve intent before Intelligence so every decision uses the same
    # intent selected by the main pipeline.
    intencao = identificar_intencao(
        pergunta
    )

    if intencao == "conversa":

        intencao_ai = identificar_intencao_ai(
            pergunta
        )

        if intencao_ai != "conversa":

            intencao = intencao_ai

    dados_pergunta["intent"] = intencao

    intelligence = IntelligenceOrchestrator()

    resultado_intelligence = intelligence.analisar(
        pergunta,
        dados_pergunta,
        rota_pergunta,
        intencao
    )

    if resultado_intelligence["precisa_esclarecimento"]:

        resposta_esclarecimento = resultado_intelligence[
            "pergunta_esclarecimento"
        ]

        adicionar_mensagem(
            "user",
            pergunta
        )

        adicionar_mensagem(
            "assistant",
            resposta_esclarecimento
        )

        return resposta_esclarecimento

    # Response Planner keeps the num_predict contract. Intelligence adds
    # the complementary response strategy to the prompt.
    plano_resposta = planejar_resposta(
        pergunta,
        dados_pergunta,
        rota_pergunta
    )


    print("\n====== RESPONSE PLANNER ======")

    print(plano_resposta)

    print("==============================\n")


    # =====================================
    # Ferramentas
    #
    # Ambiguity has already been handled. Tools run only when the request
    # has enough reference information.
    # =====================================

    tool_name = dados_pergunta.get(
        "tool"
    )

    if tool_name:

        print("\n====== TOOL DETECTADA ======")

        print(tool_name)

        print("============================\n")

        tool_manager = ToolManager()

        resposta_tool = tool_manager.execute(
            tool_name
        )

        if resposta_tool:

            adicionar_mensagem(
                "user",
                pergunta
            )

            adicionar_mensagem(
                "assistant",
                resposta_tool
            )

            return resposta_tool




# =====================================
# Question Dispatcher
# =====================================

    dispatcher = dispatch_question(
        rota_pergunta
    )

    print("\n====== QUESTION DISPATCHER ======")

    print(dispatcher)

    print("=================================\n")


# =====================================
# Question Executor
# =====================================

    dados_pergunta["question"] = pergunta

    executor = execute_question(
        dispatcher,
        dados_pergunta
    )


    print("\nRAG CONTEXT EXISTE?")
    print(bool(executor.get("rag_context")))

    print("HANDLED:")
    print(executor.get("handled"))

    print("RESPONSE:")
    print(executor.get("response"))



# =====================================
# Inserir contexto RAG no contexto cognitivo
# =====================================

    if executor.get("rag_context"):

        print("\n====== RAG CONTEXTO INSERIDO ======")

        print(executor["rag_context"])

        print("===================================\n")





    # =====================================
    # Resposta imediata
    # =====================================

    if executor["handled"]:

        resposta = executor["response"]

        adicionar_mensagem(
            "user",
            pergunta
        )

        adicionar_mensagem(
            "assistant",
            resposta
        )

        return resposta





    # =====================================
    # Identificação cognitiva da mensagem
    # =====================================


    tipo_mensagem = identificar_tipo_mensagem(
        pergunta
    )



    print("\n====== TIPO DE MENSAGEM ======")

    print(tipo_mensagem)

    print("==============================\n")







    # =====================================
    # Aprender somente afirmações
    # =====================================


    memoria_aprendida = None



    if tipo_mensagem == "APRENDER_MEMORIA":


        memoria_aprendida = aprender_durante_conversa(
            pergunta
        )




    # =====================================
    # Identificação de intenção
    # =====================================



    # =====================================
    # Comandos diretos
    # =====================================


    comandos_diretos = [

        "identidade_nome",

        "identidade_criador",

        "identidade_origem",

        "identidade_proposito",

        "identidade_missao",

        "identidade_valores",

        "identidade_capacidades",

        "identidade_arquitetura",


        "memoria_nome",

        "memoria_preferencia",

        "memoria_projeto",

        "memoria_objetivo",

        "memoria_conhecimento",


        "consultar_nome",

        "esquecer_nome",

        "alterar_estilo"

    ]




# =====================================
# Comandos diretos
# Bloqueia conflito com RAG
# =====================================


    if intencao in comandos_diretos:


        # Se a pergunta foi direcionada para RAG,
        # não permitir que identidade roube a resposta

        if rota_pergunta.get("route") == "rag":

            print(
                "\n====== COMANDO BLOQUEADO PELO RAG ======"
            )

            print(
                "Intenção:",
                intencao
            )

            print(
                "Motivo: pergunta possui conhecimento externo."
            )

            print(
                "========================================\n"
            )


        else:


            resposta = executar_comando(
                intencao,
                pergunta
            )


            if resposta:


                adicionar_mensagem(
                    "user",
                    pergunta
                )


                adicionar_mensagem(
                    "assistant",
                    resposta
                )


                return resposta






    # =====================================
    # Planejamento de contexto
    # =====================================


    plano_contexto = resultado_intelligence[
        "plano_contexto"
    ]




    for chave, valor in plano_contexto.items():

        print(
            f"{chave}: {valor}"
        )


    print("==============================\n")









    # =====================================
    # Construção do contexto
    # =====================================


    contexto = construir_contexto(
        pergunta,
        plano_contexto
    )

    memoria_hierarquica = contexto.get(
        "memoria_hierarquica"
    )

    if memoria_hierarquica:

        contexto["memoria_hierarquica"] = intelligence.filtrar_memoria(
            memoria_hierarquica,
            pergunta
        )




    # =====================================
    # Adicionar análise cognitiva
    # =====================================


    contexto[
        "analise_pergunta"
    ] = dados_pergunta


    contexto[
        "entidade_resolvida"
    ] = entidade_resolvida

    contexto[
        "classificacao_entidade"
    ] = classificacao_entidade


    contexto[
        "rota_pergunta"
    ] = rota_pergunta



    contexto[
        "dispatcher"
    ] = dispatcher


    contexto[
        "executor"
    ] = executor


    contexto[
        "plano_resposta"
    ] = plano_resposta

    contexto[
        "estrategia_resposta"
    ] = resultado_intelligence["estrategia_resposta"]

    contexto[
        "intelligence"
    ] = resultado_intelligence





    # =====================================
    # Raciocínio da memória
    # =====================================


    raciocinio_memoria = raciocinar(
        pergunta
    )



    if raciocinio_memoria:


        contexto[
            "memoria_cognitiva"
        ] = raciocinio_memoria



    elif memoria_aprendida:


        contexto[
            "memoria_cognitiva"
        ] = memoria_aprendida







    # =====================================
    # Consulta sobre usuário
    # =====================================


    if tipo_mensagem == "CONSULTA_MEMORIA":


        contexto[
            "consulta_usuario"
        ] = True



        contexto[
            "forcar_memoria_usuario"
        ] = True




    # =====================================
    # Construção do prompt
    # =====================================

    if executor.get("rag_context"):

        contexto["rag"] = executor["rag_context"]


    prompt = construir_prompt(
        contexto
    )





    # =====================================
    # Resposta do modelo
    # =====================================

    print("\n====== CHAMANDO QWEN ======")
    print("Pergunta:", pergunta)
    print("============================\n")

    print("\n====== TAMANHO DO PROMPT ======")
    print("Caracteres:", len(prompt))
    print("Palavras:", len(prompt.split()))
    print("===============================\n")


    print("\n====== LIMITE DE RESPOSTA ======")
    print("Estilo:", plano_resposta["estilo"])
    print("num_predict:", plano_resposta["num_predict"])
    print("================================\n")



    resposta = perguntar_ao_qwen(
        prompt,
        num_predict=plano_resposta["num_predict"]
    )



    # =====================================
    # Registrar conversa
    # =====================================


    adicionar_mensagem(
        "user",
        pergunta
    )


    adicionar_mensagem(
        "assistant",
        resposta
    )





    return resposta
