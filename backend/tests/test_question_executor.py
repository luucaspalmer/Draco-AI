import sys
from pathlib import Path


# Permite importar o pacote backend
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


from backend.question.question_executor import execute_question



TESTS = [

    {
        "input": {
            "executor": "identity",
            "module": "identity",
            "route": "identity"
        },

        "expected_handled": False
    },


    {
        "input": {
            "executor": "memory",
            "module": "memory",
            "route": "memory"
        },

        "expected_handled": True
    },


    {
        "input": {
            "executor": "graph",
            "module": "memory_graph",
            "route": "graph"
        },

        "expected_handled": False
    },


    {
        "input": {
            "executor": "knowledge",
            "module": "knowledge",
            "route": "knowledge"
        },

        "expected_handled": False
    },


    {
        "input": {

            "executor": "rag",
            "module": "rag",
            "route": "rag"

        },

        "expected_handled": False
    },


    {
        "input": {

            "executor": "qwen",
            "module": "conversation",
            "route": "conversation"

        },

        "expected_handled": False
    }

]



def run_tests():

    print()
    print("=" * 70)
    print("TESTE QUESTION EXECUTOR - DRACO AI")
    print("=" * 70)


    passed = 0



    for i, test in enumerate(TESTS, start=1):

        print()
        print(f"Teste {i}/{len(TESTS)}")
        print("-" * 70)


        print("Entrada:")
        print(test["input"])



        result = execute_question(
            test["input"]
        )


        print()
        print("Resultado:")
        print(result)



        ok = (

            result["success"] is True

            and result["executor"] ==
            test["input"]["executor"]

            and result["module"] ==
            test["input"]["module"]

            and result["route"] ==
            test["input"]["route"]

            and result["handled"] ==
            test["expected_handled"]

        )



        # Caso seja memória, precisa retornar resposta
        if test["input"]["executor"] == "memory":

            ok = (

                ok

                and result["response"] is not None

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

    print(
        f"{passed}/{len(TESTS)} testes passaram"
    )

    print("=" * 70)



if __name__ == "__main__":

    run_tests()