import json
import os


from .config import (
    CONVERSATION_MEMORY_FILE,
    MAX_HISTORY
)





# =====================================
# Estrutura padrão
# =====================================

def estrutura_conversa_padrao():

    return {

        "history": []

    }







# =====================================
# Carregar histórico
# =====================================

def carregar_historico():


    if not os.path.exists(
        CONVERSATION_MEMORY_FILE
    ):


        historico = estrutura_conversa_padrao()

        salvar_historico(
            historico
        )

        return historico






    with open(
        CONVERSATION_MEMORY_FILE,
        "r",
        encoding="utf-8"
    ) as arquivo:


        return json.load(
            arquivo
        )







# =====================================
# Salvar histórico
# =====================================

def salvar_historico(historico):


    with open(
        CONVERSATION_MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as arquivo:


        json.dump(

            historico,

            arquivo,

            indent=4,

            ensure_ascii=False

        )








# =====================================
# Adicionar mensagem
# =====================================

def adicionar_mensagem(
    role,
    content
):


    memoria = carregar_historico()



    memoria["history"].append({

        "role": role,

        "content": content

    })



    # mantém somente memória recente

    memoria["history"] = (
        memoria["history"]
        [-MAX_HISTORY:]
    )



    salvar_historico(
        memoria
    )







# =====================================
# Obter histórico
# =====================================

def obter_historico():


    memoria = carregar_historico()


    return memoria.get(
        "history",
        []
    )







# =====================================
# Limpar conversa
# =====================================

def limpar_historico():


    salvar_historico(

        estrutura_conversa_padrao()

    )








# =====================================
# Construir contexto textual
# =====================================

def montar_contexto():


    historico = obter_historico()



    contexto = ""



    for mensagem in historico:



        if mensagem["role"] == "user":


            contexto += (

                f"Usuário: "
                f"{mensagem['content']}\n"

            )



        else:


            contexto += (

                f"Draco: "
                f"{mensagem['content']}\n"

            )



    return contexto