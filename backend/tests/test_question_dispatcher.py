import sys
from pathlib import Path

# Permite importar o pacote backend
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.question.question_dispatcher import dispatch_question


TESTS = [

    {
        "input": {
            "route": "identity"
        },
        "expected_executor": "identity"
    },

    {
        "input": {
            "route": "knowledge"
        },
        "expected_executor": "knowledge"
    },

    {
        "input": {
            "route": "graph"
        },
        "expected_executor": "graph"
    },

    {
        "input": {
            "route": "memory"
        },
        "expected_executor": "memory"
    },

    {
        "input": {
            "route": "rag"
        },
        "expected_executor": "rag"
    },

    {
        "input": {
            "route": "conversation"
        },
        "expected_executor": "qwen"
    },

    {
        "input": {
            "route": "unknown"
        },
        "expected_executor": "qwen"
    }

]


def run_tests():

    print()

    print("=" * 70)
    print("TESTE QUESTION DISPATCHER - DRACO AI")
    print("=" * 70)

    passed = 0

    for i, test in enumerate(TESTS, start=1):

        print()

        print(f"Teste {i}/{len(TESTS)}")
        print("-" * 70)

        print("Entrada:")
        print(test["input"])

        result = dispatch_question(
            test["input"]
        )

        print()

        print("Resultado:")
        print(result)

        ok = (
            result["executor"]
            == test["expected_executor"]
        )

        if ok:

            passed += 1

            status = "PASSOU"

        else:

            status = "FALHOU"

        print()

        print(f"STATUS: {status}")

    print()

    print("=" * 70)
    print("RESULTADO FINAL")
    print("=" * 70)

    print(f"{passed}/{len(TESTS)} testes passaram")

    print("=" * 70)


if __name__ == "__main__":

    run_tests()