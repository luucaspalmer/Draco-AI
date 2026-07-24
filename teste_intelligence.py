from backend.intelligence.regression_predictor import predictor


memorias = {

    "draco": {
        "valor":"Lucas está desenvolvendo o Draco AI",
        "importancia":10,
        "confianca":1.0,
        "criado_em":"2026-07-20 10:00:00",
        "atualizado_em":"2026-07-22 10:00:00",
        "origem":"usuario"
    },


    "teste": {
        "valor":"Lucas perguntou sobre FIFA",
        "importancia":2,
        "confianca":0.5,
        "criado_em":"2025-01-01 10:00:00",
        "atualizado_em":"2025-01-01 10:00:00",
        "origem":"sistema"
    }

}


resultado = predictor.ranquear_memorias(memorias)


for item in resultado:
    print(item[0], round(item[2],3))