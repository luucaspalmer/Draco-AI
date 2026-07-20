# =====================================
# Camadas de memória do Draco AI
# =====================================


MEMORY_LAYERS = {


    "SHORT_TERM":

        {

            "nome":
            "Memória de curto prazo",


            "descricao":
            "Informações temporárias da conversa atual.",


            "persistente":
            False

        },



    "WORKING":

        {

            "nome":
            "Memória de trabalho",


            "descricao":
            "Contexto usado durante o processamento da resposta.",


            "persistente":
            False

        },



    "LONG_TERM":

        {

            "nome":
            "Memória de longo prazo",


            "descricao":
            "Informações permanentes aprendidas pelo Draco.",


            "persistente":
            True

        }

}




def listar_camadas():

    return list(
        MEMORY_LAYERS.keys()
    )




def obter_camada(nome):

    return MEMORY_LAYERS.get(
        nome
    )




def camada_eh_permanente(nome):

    camada = obter_camada(nome)


    if camada:

        return camada["persistente"]


    return False