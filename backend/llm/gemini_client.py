"""
Draco AI - LLM / Gemini Client (Provedor Online)
"""

import os
import requests

DEFAULT_MODEL = "gemini-flash-latest"

GEMINI_URL_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent"
)

from backend import config
from backend.llm.base_llm import BaseLLM


class GeminiLLM(BaseLLM):
    """
    Provedor Online do Draco AI, utilizando a API Gemini.
    """

    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        self.model = config.GEMINI_MODEL

    def available(self) -> bool:
        return bool(self.api_key)

    def generate(self, prompt: str, num_predict: int = 300) -> str:
        if not self.available():
            print("[GeminiLLM] GEMINI_API_KEY não configurada.")
            return "Meu núcleo online não está configurado no momento."

        url = GEMINI_URL_TEMPLATE.format(model=self.model)

        # Garantimos 1000 tokens para que NUNCA haja corte mecânico pelo Gemini.
        # As instruções do prompt é que vão ditar a extensão do texto.
        max_tokens = max(num_predict, 1000)

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "maxOutputTokens": max_tokens
            }
        }

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }

        try:
            resposta = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=60
            )
            resposta.raise_for_status()
            dados = resposta.json()

            texto_gerado = self._extrair_texto(dados)

            # LOG DE DEBUG: Verifique no terminal se a resposta aqui sai completa!
            print(f"\n====== [DEBUG GEMINI RAW OUTPUT] ======\n{texto_gerado}\n=======================================\n")

            return texto_gerado

        except requests.exceptions.ConnectionError:
            print("[GeminiLLM] Erro: sem conexão com a API Gemini.")
            return "Meu núcleo online está offline."

        except requests.exceptions.Timeout:
            print("[GeminiLLM] Erro: tempo limite excedido.")
            return "Meu núcleo online demorou muito para responder."

        except Exception as erro:
            print(f"[GeminiLLM] Erro: {erro}")
            return "Meu núcleo online apresentou uma falha."

    @staticmethod
    def _extrair_texto(dados: dict) -> str:
        try:
            candidatos = dados.get("candidates", [])

            if not candidatos:
                return "Não recebi uma resposta válida do núcleo online."

            partes = (
                candidatos[0]
                .get("content", {})
                .get("parts", [])
            )

            texto = "".join(
                parte.get("text", "")
                for parte in partes
            )

            return texto.strip()

        except Exception as erro:
            print(f"[GeminiLLM] Erro ao interpretar resposta: {erro}")
            return "Não consegui interpretar a resposta do núcleo online."