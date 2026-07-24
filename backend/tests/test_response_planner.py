"""
test_response_planner.py

Teste do módulo Response Planner do Draco AI.

Executar:

python backend/tests/test_response_planner.py
"""


import sys
import os


# ==========================================================
# AJUSTE DE CAMINHO DO PROJETO
# ==========================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

sys.path.insert(
    0,
    BASE_DIR
)


# ==========================================================
# IMPORT
# ==========================================================

from backend.question.response_planner import (
    planejar_resposta
)


# ==========================================================
# TESTES
# ==========================================================

TESTES = [

    {

        "descricao": "Pergunta direta sobre nome do usuário",

        "pergunta": "Qual é meu nome?",

        "dados_pergunta": {

            "intent": "consultar_nome",

            "question_type": "unknown"

        },

        "esperado": "DIRETA"

    },


    {

        "descricao": "Pergunta direta sobre criador",

        "pergunta": "Quem criou você?",

        "dados_pergunta": {

            "intent": "identidade_criador",

            "question_type": "person"

        },

        "esperado": "DIRETA"

    },


    {

        "descricao": "Pergunta direta sobre localização (question_type)",

        "pergunta": "Em que cidade eu moro?",

        "dados_pergunta": {

            "intent": "conversa",

            "question_type": "location"

        },

        "esperado": "DIRETA"

    },


    {

        "descricao": "Pergunta de definição sem pedido de detalhe",

        "pergunta": "O que é inteligência artificial?",

        "dados_pergunta": {

            "intent": "conversa",

            "question_type": "definition"

        },

        "esperado": "EXPLICATIVA"

    },


    {

        "descricao": "Pedido explícito de aprofundamento",

        "pergunta": "Explique detalhadamente como funciona o RAG.",

        "dados_pergunta": {

            "intent": "conversa",

            "question_type": "definition"

        },

        "esperado": "APROFUNDADA"

    },


    {

        "descricao": "Pedido explícito usando 'passo a passo'",

        "pergunta": "Me explique passo a passo como o Draco processa uma pergunta.",

        "dados_pergunta": {

            "intent": "conversa",

            "question_type": "definition"

        },

        "esperado": "APROFUNDADA"

    },


    {

        "descricao": "Intenção explicativa sobre arquitetura",

        "pergunta": "Qual sua arquitetura?",

        "dados_pergunta": {

            "intent": "identidade_arquitetura",

            "question_type": "unknown"

        },

        "esperado": "EXPLICATIVA"

    },


    {

        "descricao": "Fallback - pergunta sem classificação clara",

        "pergunta": "Olá Draco",

        "dados_pergunta": {

            "intent": "conversa",

            "question_type": "unknown"

        },

        "esperado": "DIRETA"

    }

]


# ==========================================================
# EXECUÇÃO
# ==========================================================


print()

print("=" * 70)

print("TESTE RESPONSE PLANNER - DRACO AI")

print("=" * 70)


total = len(TESTES)

passou = 0


for numero, teste in enumerate(
    TESTES,
    start=1
):


    resultado = planejar_resposta(

        teste["pergunta"],

        teste["dados_pergunta"]

    )


    estilo = resultado["estilo"]


    print()

    print(f"Teste {numero}/{total} - {teste['descricao']}")

    print("-" * 70)


    print("Pergunta:")

    print(teste["pergunta"])


    print()

    print("Resultado:")

    print(resultado)


    print()


    if estilo == teste["esperado"]:


        print("STATUS: PASSOU")

        passou += 1


    else:


        print(

            f"STATUS: FALHOU "
            f"(esperado: {teste['esperado']}, obtido: {estilo})"

        )


print()

print("=" * 70)

print("RESULTADO FINAL")

print("=" * 70)


print(
    f"{passou}/{total} testes passaram"
)


print("=" * 70)
