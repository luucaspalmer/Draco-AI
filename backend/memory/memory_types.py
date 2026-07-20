# =====================================
# Tipos de memória do Draco AI
# =====================================


MEMORY_TYPES = {


    "PERMANENTE":

        {
            "descricao":
            "Informações estáveis e importantes sobre o usuário."
        },



    "PROJETO":

        {
            "descricao":
            "Projetos, trabalhos e atividades em desenvolvimento."
        },



    "PREFERENCIA":

        {
            "descricao":
            "Preferências de interação e comportamento."
        },



    "CONHECIMENTO":

        {
            "descricao":
            "Conhecimentos, habilidades e assuntos aprendidos."
        },



    "CONVERSA":

        {
            "descricao":
            "Informações temporárias da conversa atual."
        }

}




def listar_tipos_memoria():

    return list(
        MEMORY_TYPES.keys()
    )




def obter_tipo_memoria(tipo):

    return MEMORY_TYPES.get(
        tipo
    )