from backend.commands import executar_comando

from backend.ollama_client import perguntar_ao_qwen

from backend.intents import identificar_intencao

from backend.intent_ai import identificar_intencao_ai

from backend.conversation_memory import adicionar_mensagem

from backend.context_builder import construir_contexto

from backend.prompt_builder import construir_prompt

from backend.context_manager import ContextManager


# Memória cognitiva

from backend.memory.memory_detector import (
    detectar_memoria,
    identificar_tipo_mensagem
)

from backend.memory.memory_controller import processar_memoria


# Raciocínio cognitivo

from backend.memory.memory_reasoner import raciocinar





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


    intencao = identificar_intencao(
        pergunta
    )



    if intencao == "conversa":


        intencao_ai = identificar_intencao_ai(
            pergunta
        )


        if intencao_ai != "conversa":

            intencao = intencao_ai







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





    if intencao in comandos_diretos:


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


    manager = ContextManager()



    plano_contexto = manager.decidir_contexto(
        pergunta,
        intencao
    )



    print("\n==============================")
    print("PLANO DE CONTEXTO")
    print("==============================")


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


    prompt = construir_prompt(
        contexto
    )







    # =====================================
    # Resposta do modelo
    # =====================================


    resposta = perguntar_ao_qwen(
        prompt
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