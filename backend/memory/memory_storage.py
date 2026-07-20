import json
import os



BASE_PATH = os.path.dirname(__file__)



PERMANENT_MEMORY = os.path.join(
    BASE_PATH,
    "permanent_memory.json"
)


PROJECT_MEMORY = os.path.join(
    BASE_PATH,
    "project_memory.json"
)


PREFERENCE_MEMORY = os.path.join(
    BASE_PATH,
    "preference_memory.json"
)


KNOWLEDGE_MEMORY = os.path.join(
    BASE_PATH,
    "knowledge_memory.json"
)


CONVERSATION_MEMORY = os.path.join(
    BASE_PATH,
    "conversation_memory.json"
)





# =====================================
# Leitura e escrita genérica
# =====================================


def carregar_arquivo(caminho, padrao):


    if not os.path.exists(caminho):

        salvar_arquivo(
            caminho,
            padrao
        )

        return padrao



    with open(
        caminho,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(arquivo)






def salvar_arquivo(caminho, dados):


    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as arquivo:


        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )






# =====================================
# Carregar memórias individuais
# =====================================



def carregar_memoria_permanente():


    return carregar_arquivo(

        PERMANENT_MEMORY,

        {}

    )






def carregar_memoria_projeto():


    return carregar_arquivo(

        PROJECT_MEMORY,

        {}

    )






def carregar_memoria_preferencia():


    return carregar_arquivo(

        PREFERENCE_MEMORY,

        {}

    )






def carregar_memoria_conhecimento():


    return carregar_arquivo(

        KNOWLEDGE_MEMORY,

        {}

    )






def carregar_memoria_conversa():


    return carregar_arquivo(

        CONVERSATION_MEMORY,

        {
            "history":[]
        }

    )








# =====================================
# Contexto completo Draco
# =====================================


def obter_memoria_contexto():


    return {


        "PERMANENTE":

            carregar_memoria_permanente(),



        "PROJETO":

            carregar_memoria_projeto(),



        "PREFERENCIA":

            carregar_memoria_preferencia(),



        "CONHECIMENTO":

            carregar_memoria_conhecimento(),



        "CONVERSA":

            carregar_memoria_conversa()

    }









# =====================================
# Salvar memória genérica
# =====================================


def salvar_memoria_permanente(
    chave,
    valor
):


    memoria = carregar_memoria_permanente()



    memoria[chave] = valor



    salvar_arquivo(

        PERMANENT_MEMORY,

        memoria

    )









# =====================================
# Buscar memória permanente
# =====================================


def buscar_memoria_permanente():


    return carregar_memoria_permanente()







# =====================================
# Projetos
# =====================================


def salvar_projeto(nome_projeto):


    memoria = carregar_memoria_projeto()



    memoria[nome_projeto] = {


        "valor":

            nome_projeto

    }



    salvar_arquivo(

        PROJECT_MEMORY,

        memoria

    )






def buscar_projetos():


    memoria = carregar_memoria_projeto()


    return memoria










# =====================================
# Conhecimento
# =====================================


def salvar_conhecimento(conhecimento):


    memoria = carregar_memoria_conhecimento()



    memoria[conhecimento] = {


        "valor":

            conhecimento

    }



    salvar_arquivo(

        KNOWLEDGE_MEMORY,

        memoria

    )






def buscar_conhecimentos():


    return carregar_memoria_conhecimento()










# =====================================
# Preferências
# =====================================


def salvar_preferencia(
    categoria,
    chave,
    valor
):


    memoria = carregar_memoria_preferencia()



    if categoria not in memoria:

        memoria[categoria] = {}




    memoria[categoria][chave] = valor




    salvar_arquivo(

        PREFERENCE_MEMORY,

        memoria

    )







def buscar_preferencias():


    return carregar_memoria_preferencia()










# =====================================
# Conversas
# =====================================


def salvar_conversa(
    usuario,
    resposta
):


    memoria = carregar_memoria_conversa()



    if "history" not in memoria:

        memoria["history"] = []




    memoria["history"].append(

        {

            "user":
                usuario,


            "assistant":
                resposta

        }

    )




    memoria["history"] = memoria["history"][-20:]




    salvar_arquivo(

        CONVERSATION_MEMORY,

        memoria

    )







def buscar_conversa():


    memoria = carregar_memoria_conversa()


    return memoria.get(

        "history",

        []

    )