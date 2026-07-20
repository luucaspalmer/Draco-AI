import requests

from backend.config import OLLAMA_MODEL



def identificar_intencao_ai(pergunta):


    texto = pergunta.lower()


    # =====================================
    # Proteção - Objetivo do Draco AI
    # =====================================

    if (
        "objetivo do draco" in texto
        or
        "objetivo do draco ai" in texto
        or
        "propósito do draco" in texto
        or
        "proposito do draco" in texto
        or
        "para que serve o draco" in texto
        or
        "qual a finalidade do draco" in texto
    ):

        return "identidade_objetivo"



    
    # =====================================
    # Proteção - Tecnologia do Draco AI
    # =====================================

    if (
        "tecnologias do draco" in texto
        or
        "tecnologia do draco" in texto
        or
        "quais tecnologias o draco usa" in texto
        or
        "qual tecnologia o draco usa" in texto
        or
        "como o draco funciona" in texto
        or
        "arquitetura do draco" in texto
    ):

        return "identidade_arquitetura"

    
    
    
    # =====================================
    # Proteção - Propósito do Draco
    # =====================================


    if (
        "qual o objetivo do draco" in texto
        or
        "qual objetivo do draco ai" in texto
        or
        "qual seu propósito" in texto
        or
        "qual seu proposito" in texto
        or
        "para que você existe" in texto
        or
        "para que voce existe" in texto
    ):

        return "identidade_proposito"



    # =====================================
    # Proteção - Origem do Draco AI
    # =====================================


    if (
        "como nasceu o projeto draco ai" in texto
        or
        "como surgiu o draco ai" in texto
        or
        "qual a origem do draco ai" in texto
        or
        "como foi criado o draco ai" in texto
        or
        "história do draco ai" in texto
        or
        "historia do draco ai" in texto
    ):

        return "identidade_origem"



    # =====================================
    # Proteção de intenções críticas
    # =====================================


    if (
        "quem é você" in texto
        or
        "quem e voce" in texto
        or
        "qual seu nome" in texto
        or
        "qual é seu nome" in texto
        or
        "qual e seu nome" in texto
        or
        "como você se chama" in texto
        or
        "como voce se chama" in texto
    ):

        return "identidade_nome"




    if (
        "quem criou você" in texto
        or
        "quem criou voce" in texto
        or
        "quem fez você" in texto
        or
        "quem fez voce" in texto
        or
        "seu criador" in texto
    ):

        return "identidade_criador"




    if (
        "qual meu nome" in texto
        or
        "qual é meu nome" in texto
        or
        "qual e meu nome" in texto
        or
        "você sabe meu nome" in texto
        or
        "voce sabe meu nome" in texto
    ):

        return "consultar_nome"




    # =====================================
    # Classificação por IA
    # =====================================


    prompt = f"""

Você é um classificador de intenção do sistema Draco AI.

Sua função é retornar somente uma intenção.

Nunca responda a pergunta.

Retorne apenas uma opção da lista.



INTENÇÕES:

identidade_nome
identidade_criador
identidade_origem
identidade_proposito
identidade_missao
identidade_valores
identidade_capacidades
identidade_arquitetura

consultar_memoria
consultar_nome

memoria_nome
memoria_preferencia
memoria_projeto
memoria_objetivo
memoria_conhecimento

alterar_estilo

conversa



REGRAS:



Perguntas sobre Draco:

Exemplo:

"Qual seu propósito?"

Resposta:

identidade_proposito



Perguntas sobre Lucas:

Exemplo:

"Qual meu projeto?"

Resposta:

consultar_memoria



Perguntas pedindo para guardar:

Exemplo:

"Guarde que meu projeto é Draco AI"

Resposta:

memoria_projeto



Perguntas gerais:

Resposta:

conversa



Mensagem:

{pergunta}



Retorne somente a intenção.

"""



    url = "http://localhost:11434/api/generate"



    dados = {

        "model": OLLAMA_MODEL,

        "prompt": prompt,

        "stream": False

    }



    resposta = requests.post(
        url,
        json=dados
    )



    resultado = resposta.json()



    intencao = (

        resultado["response"]
        .strip()
        .lower()

    )



    intencoes_validas = [


        "identidade_nome",

        "identidade_criador",

        "identidade_origem",

        "identidade_proposito",

        "identidade_missao",

        "identidade_valores",

        "identidade_capacidades",

        "identidade_arquitetura",

        "consultar_memoria",

        "consultar_nome",

        "memoria_nome",

        "memoria_preferencia",

        "memoria_projeto",

        "memoria_objetivo",

        "memoria_conhecimento",


        "alterar_estilo",


        "conversa"

    ]



    if intencao not in intencoes_validas:

        return "conversa"



    return intencao