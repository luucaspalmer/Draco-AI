from backend.memory.memory_manager import (
    obter_memoria_contexto
)

import requests

from backend.config import OLLAMA_MODEL


# =====================================
# Usage Logger (fase 2 - inteligência)
#
# Import protegido: se o módulo intelligence não
# existir ainda no projeto, ou falhar por qualquer
# motivo, o memory_search continua funcionando
# exatamente como antes, sem log nenhum.
# =====================================

try:

    from backend.intelligence.usage_logger import (
        registrar_uso
    )

except Exception:

    registrar_uso = None




# =====================================
# Categorias de memória
# =====================================


CATEGORIAS = {


    "permanente": [

        "nome",
        "idade",
        "quem sou",
        "perfil",
        "usuário",
        "usuario"

    ],



    "projeto": [

        "projeto",
        "projetos",
        "desenvolvendo",
        "criando",
        "trabalhando"

    ],



    "objetivo": [

        "objetivo",
        "objetivos",
        "meta",
        "metas",
        "planejo",
        "quero"

    ],



    "conhecimento": [

        "aprendi",
        "sei",
        "conhecimento",
        "habilidade",
        "linguagem",
        "estudo"

    ],



    "preferencia": [

        "preferência",
        "preferencia",
        "estilo",
        "resposta",
        "gosto",
        "comportamento"

    ]

}




# =====================================
# Busca por regras
# =====================================


def identificar_categoria_regras(pergunta):


    pergunta = pergunta.lower()


    pontuacao = {}



    for categoria, palavras in CATEGORIAS.items():


        pontos = 0


        for palavra in palavras:

            if palavra in pergunta:

                pontos += 1



        if pontos:

            pontuacao[categoria] = pontos



    if not pontuacao:

        return None, 0




    categoria = max(
        pontuacao,
        key=pontuacao.get
    )



    confianca = min(
        pontuacao[categoria] / 3,
        1
    )



    return categoria, round(
        confianca,
        2
    )





# =====================================
# Classificação Qwen
# =====================================


def identificar_categoria_ai(pergunta):


    prompt = f"""

Você é um classificador de memória do Draco AI.

Escolha qual memória deve ser consultada.

Retorne somente uma opção.


Opções:

permanente

projeto

objetivo

conhecimento

preferencia

geral



Pergunta:

{pergunta}



Retorne somente a categoria.

"""



    try:

        resposta = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model": OLLAMA_MODEL,

                "prompt": prompt,

                "stream": False

            },

            timeout=30

        )



        categoria = (
            resposta
            .json()
            .get(
                "response",
                ""
            )
            .strip()
            .lower()
        )



    except Exception:

        return "geral"



    validas = [

        "permanente",
        "projeto",
        "objetivo",
        "conhecimento",
        "preferencia",
        "geral"

    ]



    if categoria in validas:

        return categoria



    return "geral"






# =====================================
# Escolha final
# =====================================


def identificar_categoria(pergunta):


    categoria, confianca = identificar_categoria_regras(
        pergunta
    )


    if categoria:


        return {

            "categoria": categoria,

            "confianca": confianca,

            "origem": "regras"

        }




    categoria = identificar_categoria_ai(
        pergunta
    )


    return {


        "categoria": categoria,

        "confianca": 0.70,

        "origem": "qwen"

    }



# =====================================
# Buscar memória hierárquica
# =====================================


def buscar_contexto(categoria):


    memoria = obter_memoria_contexto() or {}



    if categoria == "permanente":

        return {

            "PERMANENTE":
                memoria.get(
                    "PERMANENTE",
                    {}
                )

        }




    if categoria == "projeto":

        return {

            "PROJETO":
                memoria.get(
                    "PROJETO",
                    {}
                )

        }




    if categoria == "objetivo":

        projeto = memoria.get(
            "PROJETO",
            {}
        )


        return {

            "PROJETO":

                {

                    "objetivos":
                    projeto.get(
                        "objetivos",
                        []
                    )

                }

        }




    if categoria == "conhecimento":

        return {

            "CONHECIMENTO":
                memoria.get(
                    "CONHECIMENTO",
                    {}
                )

        }




    if categoria == "preferencia":

        return {

            "PREFERENCIA":
                memoria.get(
                    "PREFERENCIA",
                    {}
                )

        }




    return memoria




# =====================================
# Extrair chaves recuperadas
#
# Usado apenas para alimentar o log de
# uso (fase 2). Não afeta o retorno de
# buscar_memorias.
# =====================================


def _extrair_chaves_recuperadas(memoria_dict):

    chaves = []


    if not isinstance(memoria_dict, dict):

        return chaves


    for camada, dados in memoria_dict.items():

        if isinstance(dados, dict):

            chaves.extend(dados.keys())


    return chaves




# =====================================
# Função principal
# =====================================


def buscar_memorias(pergunta):


    analise = identificar_categoria(
        pergunta
    )


    categoria = analise["categoria"]


    memoria = buscar_contexto(
        categoria
    )



    # =================================
    # Log de uso (fase 2)
    #
    # Não altera o comportamento nem o
    # retorno desta função. Se o logger
    # não existir ou falhar, é ignorado
    # silenciosamente.
    # =================================

    if registrar_uso:

        try:

            registrar_uso(
                pergunta=pergunta,
                categoria=categoria,
                chaves=_extrair_chaves_recuperadas(memoria),
                origem=analise["origem"],
                confianca=analise["confianca"]
            )

        except Exception:

            pass



    return {


        "categoria":
            categoria,


        "confianca":
            analise["confianca"],


        "origem":
            analise["origem"],



        "memoria":

            memoria

    }
