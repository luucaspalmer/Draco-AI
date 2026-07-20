"""
Draco AI
Sistema de Voz
Motor Whisper
"""


import whisper
import os


# ==============================
# Modelo Whisper
# ==============================

MODEL_NAME = "base"


print("Carregando Whisper...")

model = whisper.load_model(
    MODEL_NAME
)

print("Whisper carregado!")


# ==============================
# Transcrição
# ==============================


def transcrever_audio(caminho_audio):

    if not os.path.exists(caminho_audio):
        return None


    resultado = model.transcribe(
        caminho_audio,
        language="pt"
    )


    texto = resultado["text"]


    return texto.strip()