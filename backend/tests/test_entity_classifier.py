import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(
    0,
    str(ROOT)
)


from backend.question.entity_classifier import classify_entity



TESTS = [

    {
        "input": {
            "entity": "draco",
            "exists": True,
            "source": "internal"
        },

        "expected_route": "identity"

    },


    {
        "input": {
            "entity": "lucas",
            "exists": True,
            "source": "memory"
        },

        "expected_route": "memory"

    },


    {
        "input": {
            "entity": "aldorion",
            "exists": True,
            "source": "memory"
        },

        "expected_route": "rag"

    },


    {
        "input": {
            "entity": "python",
            "exists": True,
            "source": "internal"
        },

        "expected_route": "knowledge"

    }

]



def run_tests():

    print()
    print("=" * 70)
    print("TESTE ENTITY CLASSIFIER - DRACO AI")
    print("=" * 70)


    passed = 0


    for i, test in enumerate(TESTS, start=1):

        print()
        print(f"Teste {i}/{len(TESTS)}")
        print("-" * 70)


        print("Entrada:")
        print(test["input"])


        result = classify_entity(
            test["input"]
        )


        print()
        print("Resultado:")
        print(result)



        if result["route"] == test["expected_route"]:

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

    print(
        f"{passed}/{len(TESTS)} testes passaram"
    )

    print("=" * 70)



if __name__ == "__main__":

    run_tests()