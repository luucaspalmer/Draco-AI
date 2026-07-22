"""
Draco AI - Ollama Client

Responsável pela comunicação
entre Draco AI e o modelo Qwen local.
"""

import requests
import json

from .config import OLLAMA_MODEL



OLLAMA_URL = "http://localhost:11434/api/generate"



def perguntar_ao_qwen(prompt):


    print("Draco esta pensando...")


    dados = {


        "model": OLLAMA_MODEL,


        "prompt": prompt,


        "stream": True,


        "keep_alive": "30m"

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