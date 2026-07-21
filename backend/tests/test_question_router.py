"""
test_question_router.py

Teste do sistema de roteamento cognitivo do Draco AI.

Executar:

python backend/tests/test_question_router.py
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

from backend.question.question_router import (
    route_question
)



# ==========================================================
# TESTES
# ==========================================================

TESTES = [

    {

        "entrada": {

            "is_question": True,

            "question_type": "person",

            "entity": "draco"

        },

        "esperado": "identity"

    },


    {

        "entrada": {

            "is_question": True,

            "question_type": "definition",

            "entity": "inteligência artificial"

        },

        "esperado": "knowledge"

    },


    {

        "entrada": {

            "is_question": True,

            "question_type": "event",

            "entity": "eclipse sombrio"

        },

        "esperado": "rag"

    },


    {

        "entrada": {

            "is_question": False,

            "question_type": "unknown",

            "entity": ""

        },

        "esperado": "conversation"

    },


    {

        "entrada": {

            "is_question": True,

            "question_type": "relationship",

            "entity": "draco e aldorion"

        },

        "esperado": "graph"

    }

]



# ==========================================================
# EXECUÇÃO
# ==========================================================


print()

print("=" * 70)

print("TESTE QUESTION ROUTER - DRACO AI")

print("=" * 70)



total = len(TESTES)

passou = 0



for numero, teste in enumerate(
    TESTES,
    start=1
):


    resultado = route_question(
        teste["entrada"]
    )


    rota = resultado["route"]



    print()

    print(f"Teste {numero}/{total}")

    print("-" * 70)


    print("Entrada:")

    print(
        teste["entrada"]
    )


    print()

    print("Resultado:")

    print(
        resultado
    )


    print()



    if rota == teste["esperado"]:


        print("STATUS: PASSOU")

        passou += 1



    else:


        print("STATUS: FALHOU")



print()

print("=" * 70)

print("RESULTADO FINAL")

print("=" * 70)


print(
    f"{passou}/{total} testes passaram"
)


print("=" * 70)