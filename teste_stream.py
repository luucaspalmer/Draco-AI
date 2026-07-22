import requests
import json
import time


url = "http://localhost:11434/api/generate"


dados = {

    "model": "qwen2.5:3b",

    "prompt": "O que é inteligência artificial?",

    "stream": True

}


inicio = time.time()


resposta = requests.post(
    url,
    json=dados,
    stream=True
)


primeiro_token = None


texto = ""


for linha in resposta.iter_lines():

    if linha:

        agora = time.time()


        if primeiro_token is None:

            primeiro_token = agora - inicio

            print(
                "Primeiro token:",
                primeiro_token,
                "segundos"
            )


        dados = json.loads(
            linha.decode("utf-8")
        )


        if "response" in dados:

            texto += dados["response"]


print("\nTempo total:")
print(time.time() - inicio)

print("\nResposta:")
print(texto)