import sys
import os


# Adiciona raiz do projeto ao PATH
ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

sys.path.append(ROOT_DIR)



from backend.question.entity_resolver import resolve_entity




def run_tests():


    testes = [

        {
            "entity": "draco",
            "expected": True
        },


        {
            "entity": "python",
            "expected": True
        },


        {
            "entity": "aldorion",
            "expected": True
        },


        {
            "entity": "",
            "expected": False
        }

    ]



    passou = 0



    print("\n")
    print("=" * 70)
    print("TESTE ENTITY RESOLVER - DRACO AI")
    print("=" * 70)



    for i, teste in enumerate(testes, 1):


        print(f"\nTeste {i}/{len(testes)}")
        print("-" * 70)


        resultado = resolve_entity(
            teste["entity"]
        )


        print("Entrada:")
        print(teste["entity"])


        print("\nResultado:")
        print(resultado)



        if resultado["exists"] == teste["expected"]:


            print("\nSTATUS: PASSOU")

            passou += 1


        else:


            print("\nSTATUS: FALHOU")



    print("\n")
    print("=" * 70)

    print(
        f"RESULTADO FINAL: {passou}/{len(testes)} testes passaram"
    )

    print("=" * 70)




if __name__ == "__main__":

    run_tests()