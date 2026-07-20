import json
import os

from .config import (
    MEMORY_FILE,
    PERSONALITY_FILE
)



# =====================================
# Estrutura padrão da memória
# =====================================

def estrutura_memoria_padrao():

    return {

        "usuario": {

            "perfil": {},

            "preferencias": {},

            "projetos": [],

            "objetivos": [],

            "conhecimentos": []

        },


        "draco": {}

    }




# =====================================
# Carregar memória
# =====================================

def carregar_memoria():


    if not os.path.exists(MEMORY_FILE):

        memoria = estrutura_memoria_padrao()

        salvar_memoria(memoria)

        return memoria



    with open(
        MEMORY_FILE,
        "r",
        encoding="utf-8"
    ) as arquivo:

        memoria = json.load(arquivo)



    return migrar_memoria(memoria)





# =====================================
# Migração da memória antiga
# =====================================

def migrar_memoria(memoria):


    nova_memoria = estrutura_memoria_padrao()



    if "draco" in memoria:

        nova_memoria["draco"] = memoria["draco"]



    usuario_antigo = memoria.get(
        "usuario",
        {}
    )



    # Migração do formato antigo

    if "nome" in usuario_antigo:

        nova_memoria["usuario"]["perfil"]["nome"] = (
            usuario_antigo["nome"]
        )



    # Mantém estrutura nova caso exista

    if "perfil" in usuario_antigo:

        nova_memoria["usuario"]["perfil"].update(
            usuario_antigo["perfil"]
        )



    for campo in [

        "preferencias",
        "projetos",
        "objetivos",
        "conhecimentos"

    ]:

        if campo in usuario_antigo:

            nova_memoria["usuario"][campo] = (
                usuario_antigo[campo]
            )



    salvar_memoria(nova_memoria)


    return nova_memoria





# =====================================
# Salvar memória
# =====================================

def salvar_memoria(memoria):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            memoria,
            arquivo,
            indent=4,
            ensure_ascii=False
        )





# =====================================
# Memória genérica
# =====================================

def guardar_informacao(categoria, chave, valor):

    memoria = carregar_memoria()


    if categoria not in memoria:

        memoria[categoria] = {}



    memoria[categoria][chave] = valor


    salvar_memoria(memoria)


    print("Informacao salva!")





def buscar_informacao(categoria, chave):

    memoria = carregar_memoria()



    try:

        # Compatibilidade antiga:
        # usuario.nome

        if categoria == "usuario":

            if chave == "nome":

                return (
                    memoria
                    ["usuario"]
                    ["perfil"]
                    .get("nome")
                )



        return memoria[categoria][chave]



    except KeyError:

        return None





def ver_memoria():

    return carregar_memoria()





# =====================================
# Perfil do usuário
# =====================================

def aprender_usuario(chave, valor):

    memoria = carregar_memoria()



    memoria["usuario"]["perfil"][chave] = valor



    salvar_memoria(memoria)


    print(
        "Aprendi uma nova informacao!"
    )





def buscar_perfil(chave):

    memoria = carregar_memoria()


    return (
        memoria
        ["usuario"]
        ["perfil"]
        .get(chave)
    )





# =====================================
# Projetos
# =====================================

def salvar_projeto(projeto):

    memoria = carregar_memoria()



    projetos = memoria["usuario"]["projetos"]



    if projeto not in projetos:

        projetos.append(projeto)



    salvar_memoria(memoria)





# =====================================
# Objetivos
# =====================================

def salvar_objetivo(objetivo):

    memoria = carregar_memoria()



    objetivos = memoria["usuario"]["objetivos"]



    if objetivo not in objetivos:

        objetivos.append(objetivo)



    salvar_memoria(memoria)





# =====================================
# Conhecimentos
# =====================================

def salvar_conhecimento(conhecimento):

    memoria = carregar_memoria()



    conhecimentos = memoria["usuario"]["conhecimentos"]



    if conhecimento not in conhecimentos:

        conhecimentos.append(conhecimento)



    salvar_memoria(memoria)





# =====================================
# Personalidade
# =====================================

def carregar_personalidade():


    if not os.path.exists(PERSONALITY_FILE):

        return {

            "resposta": {},
            "codigo": {},
            "comunicacao": {},
            "interesses": {}

        }



    with open(
        PERSONALITY_FILE,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(arquivo)





def salvar_personalidade(personalidade):

    with open(
        PERSONALITY_FILE,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            personalidade,
            arquivo,
            indent=4,
            ensure_ascii=False
        )





def aprender_personalidade(categoria, chave, valor):

    personalidade = carregar_personalidade()



    if categoria not in personalidade:

        personalidade[categoria] = {}



    personalidade[categoria][chave] = valor



    salvar_personalidade(personalidade)


    print(
        "Preferencia de personalidade salva!"
    )





def buscar_personalidade():

    return carregar_personalidade()





# =====================================
# Visualização da memória
# =====================================

def ver_memoria_completa():

    memoria_usuario = carregar_memoria()

    memoria_personalidade = carregar_personalidade()



    return {

        "usuario": memoria_usuario.get(
            "usuario",
            {}
        ),

        "draco": memoria_usuario.get(
            "draco",
            {}
        ),

        "personalidade": memoria_personalidade

    }





def formatar_memoria():

    memoria = ver_memoria_completa()



    resposta = "Minhas memorias atuais:\n\n"



    resposta += "Perfil do usuario:\n"



    perfil = memoria["usuario"]["perfil"]



    if perfil:

        for chave, valor in perfil.items():

            resposta += f"- {chave}: {valor}\n"

    else:

        resposta += "- Nenhuma informacao salva\n"




    resposta += "\nProjetos:\n"



    for projeto in memoria["usuario"]["projetos"]:

        resposta += f"- {projeto}\n"



    resposta += "\nObjetivos:\n"



    for objetivo in memoria["usuario"]["objetivos"]:

        resposta += f"- {objetivo}\n"




    resposta += "\nConhecimentos:\n"



    for conhecimento in memoria["usuario"]["conhecimentos"]:

        resposta += f"- {conhecimento}\n"




    resposta += "\nPersonalidade:\n"



    personalidade = memoria["personalidade"]



    encontrou = False



    for categoria, dados in personalidade.items():

        if dados:

            encontrou = True

            resposta += f"\n{categoria.capitalize()}:\n"



            for chave, valor in dados.items():

                resposta += f"- {chave}: {valor}\n"



    if not encontrou:

        resposta += "- Nenhuma preferencia salva\n"



    return resposta





# =====================================
# Esquecer informações
# =====================================

def esquecer_usuario(chave):

    memoria = carregar_memoria()



    perfil = memoria["usuario"]["perfil"]



    if chave in perfil:

        del perfil[chave]

        salvar_memoria(memoria)

        return True



    return False





def esquecer_personalidade(categoria, chave):

    personalidade = carregar_personalidade()



    if categoria in personalidade:

        if chave in personalidade[categoria]:

            del personalidade[categoria][chave]

            salvar_personalidade(personalidade)

            return True



    return False





def alterar_personalidade(categoria, chave, valor):

    personalidade = carregar_personalidade()



    if categoria not in personalidade:

        personalidade[categoria] = {}



    personalidade[categoria][chave] = valor



    salvar_personalidade(personalidade)



    return True