"""
Draco AI - Ollama Client

Responsável pela comunicação
entre Draco AI e o modelo Qwen local.
"""

import requests

from .config import OLLAMA_MODEL



# =====================================
# Configuração
# =====================================

OLLAMA_URL = "http://localhost:11434/api/generate"



# =====================================
# Perguntar ao Qwen
# =====================================

def perguntar_ao_qwen(prompt):


    print("Draco esta pensando...")


    dados = {

        "model": OLLAMA_MODEL,

        "prompt": prompt,

        "stream": False

    }


    try:


        resposta = requests.post(

            OLLAMA_URL,

            json=dados,

            timeout=120

        )


        resposta.raise_for_status()



        resultado = resposta.json()



        if "response" in resultado:


            return resultado["response"]



        print(
            "Resposta inesperada do Ollama:",
            resultado
        )


        return "Não consegui interpretar a resposta do meu núcleo."



    except requests.exceptions.ConnectionError:


        print(
            "Erro: Ollama não está conectado."
        )


        return "Meu núcleo local está offline."



    except requests.exceptions.Timeout:


        print(
            "Erro: tempo limite excedido."
        )


        return "Meu núcleo demorou muito para responder."



    except Exception as e:


        print(
            "ERRO OLLAMA:",
            e
        )


        return "Meu núcleo apresentou uma falha."
