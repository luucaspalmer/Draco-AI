from backend.memory.memory_manager import (
    obter_memoria_contexto
)

import requests

from backend.config import OLLAMA_MODEL




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
# Função principal
# =====================================


def buscar_memorias(pergunta):


    analise = identificar_categoria(
        pergunta
    )


    categoria = analise["categoria"]



    return {


        "categoria":
            categoria,


        "confianca":
            analise["confianca"],


        "origem":
            analise["origem"],



        "memoria":

            buscar_contexto(
                categoria
            )

    }