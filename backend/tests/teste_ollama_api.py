import requests
import time


url = "http://localhost:11434/api/generate"


dados = {

    "model": "qwen2.5:3b",

    "prompt": "O que é inteligência artificial?",

    "stream": False

}


inicio = time.time()


resposta = requests.post(
    url,
    json=dados,
    timeout=120
)


fim = time.time()


print(
    "Tempo:",
    fim - inicio,
    "segundos"
)


print(
    resposta.json()["response"]
)