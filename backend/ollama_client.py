"""
Draco AI - Ollama Client

Responsável pela comunicação
entre Draco AI e o modelo Qwen local.
"""

import requests
import json

from .config import OLLAMA_MODEL



OLLAMA_URL = "http://localhost:11434/api/generate"



def perguntar_ao_qwen(prompt, num_predict=300):
    """
    num_predict controla o teto máximo de tokens gerados
    pelo Qwen para esta resposta.

    Esse valor normalmente vem do Response Planner
    (backend/question/response_planner.py), que decide
    o estilo da resposta (DIRETA, EXPLICATIVA, APROFUNDADA)
    antes da construção do prompt.

    Quando não informado, 300 é usado como valor neutro
    de segurança.
    """


    print("Draco esta pensando...")

    print(f"Limite de tokens (num_predict): {num_predict}")


    dados = {


        "model": OLLAMA_MODEL,


        "prompt": prompt,


        "stream": True,


        "keep_alive": "30m",


        "options": {

            "num_predict": num_predict

        }

    }



    try:


        resposta = requests.post(

            OLLAMA_URL,

            json=dados,

            stream=True,

            timeout=120

        )


        resposta.raise_for_status()



        texto_final = ""



        for linha in resposta.iter_lines():


            if not linha:

                continue



            dados_linha = json.loads(

                linha.decode("utf-8")

            )



            if "response" in dados_linha:


                texto_final += dados_linha["response"]



            if dados_linha.get(
                "done",
                False
            ):

                break



        return texto_final.strip()




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
