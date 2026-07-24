import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


from backend.intelligence.intelligence_orchestrator import (
    IntelligenceOrchestrator
)


TESTS = [

    {
        "descricao": "Pergunta clara sobre identidade",

        "pergunta": "Qual seu propósito?",

        "dados_pergunta": {
            "question_type": "definition",
            "entity": "propósito",
            "is_question": True
        },

        "rota_pergunta": {"route": "identity"},

        "intencao": "identidade_proposito",

        "espera_esclarecimento": False
    },

    {
        "descricao": "Pergunta ambígua (pronome sem referência)",

        "pergunta": "Como faço isso?",

        "dados_pergunta": {
            "question_type": "unknown",
            "entity": "",
            "is_question": True
        },

        "rota_pergunta": {"route": "general"},

        "intencao": "conversa",

        "espera_esclarecimento": True
    },

    {
        "descricao": "Pedido vago de melhoria",

        "pergunta": "Pode melhorar?",

        "dados_pergunta": {
            "question_type": "unknown",
            "entity": "",
            "is_question": True
        },

        "rota_pergunta": {"route": "general"},

        "intencao": "conversa",

        "espera_esclarecimento": True
    },

    {
        "descricao": "Pergunta complexa de comparação",

        "pergunta": "Compare Python e JavaScript para inteligência artificial",

        "dados_pergunta": {
            "question_type": "list",
            "entity": "python e javascript",
            "is_question": True
        },

        "rota_pergunta": {"route": "knowledge"},

        "intencao": "conversa",

        "espera_esclarecimento": False
    }

]


def run_tests():

    print()
    print("=" * 70)
    print("TESTE INTELLIGENCE ORCHESTRATOR - DRACO AI")
    print("=" * 70)

    orquestrador = IntelligenceOrchestrator()

    passed = 0

    for i, teste in enumerate(TESTS, start=1):

        print()
        print(f"Teste {i}/{len(TESTS)} - {teste['descricao']}")
        print("-" * 70)

        print("Pergunta:")
        print(teste["pergunta"])

        resultado = orquestrador.analisar(

            teste["pergunta"],

            teste["dados_pergunta"],

            teste["rota_pergunta"],

            teste["intencao"]

        )

        print()
        print("Resultado:")
        print(resultado)

        ok = (

            resultado["precisa_esclarecimento"]

            == teste["espera_esclarecimento"]

        )

        if not teste["espera_esclarecimento"]:

            ok = (

                ok

                and resultado["plano_contexto"] is not None

                and resultado["analise_intencao"] is not None

            )

        status = "PASSOU" if ok else "FALHOU"

        if ok:

            passed += 1

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
