"""
test_question_analyzer.py

Teste completo do módulo question_analyzer.

Executar na raiz do projeto:

python backend/tests/test_question_analyzer.py
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

sys.path.insert(0, BASE_DIR)


# ==========================================================
# IMPORT DO QUESTION ANALYZER
# ==========================================================

try:
    from backend.question.question_analyzer import analyze_question

except Exception as error:

    print("ERRO AO IMPORTAR QUESTION ANALYZER")
    print(error)

    sys.exit(1)


# ==========================================================
# CASOS DE TESTE
# ==========================================================

TEST_CASES = [

    {
        "text": "Quem é Draco?",
        "type": "person",
        "entity": "draco"
    },

    {
        "text": "Quem foi Albert Einstein?",
        "type": "person",
        "entity": "albert einstein"
    },

    {
        "text": "Quem são os pais de Draco?",
        "type": "person",
        "entity": "os pais de draco"
    },

    {
        "text": "O que é Inteligência Artificial?",
        "type": "definition",
        "entity": "inteligência artificial"
    },

    {
        "text": "O que significa API?",
        "type": "definition",
        "entity": "api"
    },

    {
        "text": "Quando nasceu Isaac Newton?",
        "type": "time",
        "entity": "isaac newton"
    },

    {
        "text": "Onde fica a Biblioteca Celestial?",
        "type": "location",
        "entity": "a biblioteca celestial"
    },

    {
        "text": "Quais são os núcleos do Draco?",
        "type": "list",
        "entity": "os núcleos do draco"
    },

    {
        "text": "Por que Draco recebeu esse título?",
        "type": "reason",
        "entity": "draco recebeu esse título"
    },

    {
        "text": "O que aconteceu no Eclipse Sombrio?",
        "type": "event",
        "entity": "no eclipse sombrio"
    },

    {
        "text": "Qual a relação entre Draco e Aldorion?",
        "type": "relationship",
        "entity": "entre draco e aldorion"
    },

    {
        "text": "Quantos módulos existem?",
        "type": "quantity",
        "entity": "módulos existem"
    },

    {
        "text": "De quem é este livro?",
        "type": "owner",
        "entity": "este livro"
    },


    # Não perguntas

    {
        "text": "Bom dia Draco",
        "type": "unknown",
        "entity": ""
    },

    {
        "text": "Obrigado",
        "type": "unknown",
        "entity": ""
    }

]


# ==========================================================
# EXECUÇÃO DOS TESTES
# ==========================================================

def run_tests():

    print()
    print("=" * 70)
    print("TESTE QUESTION ANALYZER - DRACO AI")
    print("=" * 70)
    print()


    total = len(TEST_CASES)

    passed = 0


    for index, test in enumerate(TEST_CASES, start=1):

        result = analyze_question(test["text"])


        type_ok = (
            result["question_type"]
            ==
            test["type"]
        )


        entity_ok = (
            result["entity"]
            ==
            test["entity"]
        )


        if type_ok and entity_ok:
            status = "PASSOU"
            passed += 1

        else:
            status = "FALHOU"


        print(f"Teste {index}/{total}")
        print("-" * 70)

        print("Entrada:")
        print(test["text"])

        print()

        print("Esperado:")
        print(
            f"Tipo: {test['type']} | "
            f"Entidade: {test['entity']}"
        )

        print()

        print("Recebido:")
        print(
            f"Tipo: {result['question_type']} | "
            f"Entidade: {result['entity']}"
        )

        print()

        print("Status:", status)
        print("=" * 70)



    print()
    print("RESULTADO FINAL")
    print("=" * 70)

    print(
        f"{passed}/{total} testes passaram"
    )

    print("=" * 70)



# ==========================================================
# START
# ==========================================================

if __name__ == "__main__":

    print("Iniciando testes...")

    run_tests()