from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.brain import pensar
from backend.voice.voice_manager import VoiceManager



# =====================================
# Pasta de upload de áudio
# =====================================

VOICE_UPLOAD = Path(
    "backend/voice/audio"
)


VOICE_UPLOAD.mkdir(
    parents=True,
    exist_ok=True
)



# =====================================
# Arquivo saída Piper
# =====================================

PIPER_OUTPUT = Path(
    "piper/output/output.wav"
)



# =====================================
# Voice Manager
# =====================================

voice_manager = VoiceManager()



# =====================================
# Inicialização Draco API
# =====================================

app = FastAPI(

    title="Draco AI",

    description="Interface de comunicação do Draco AI",

    version="1.2"

)



# =====================================
# Configuração CORS
# Comunicação Frontend → Backend
# =====================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:5500",

        "http://127.0.0.1:5500"

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)



# =====================================
# Rota principal
# =====================================

@app.get("/")

def inicio():

    return {

        "status": "Draco AI online",

        "version": "1.2"

    }



# =====================================
# Comunicação Texto
# =====================================

@app.post("/chat")

def conversar(dados: dict):

    mensagem = dados.get(

        "mensagem",

        ""

    )


    resposta = pensar(

        mensagem

    )


    return {

        "resposta": resposta

    }



# =====================================
# Comunicação por Voz
# =====================================

@app.post("/voice")

async def receber_audio(

    audio: UploadFile = File(...)

):


    destino = VOICE_UPLOAD / "input.webm"


    with open(destino, "wb") as arquivo:

        arquivo.write(

            await audio.read()

        )



    print("\n================================")
    print("ÁUDIO RECEBIDO")
    print("================================")
    print(destino)
    print("================================\n")



    resultado = voice_manager.process(

        destino

    )



    print("\n================================")
    print("RESPOSTA DRACO")
    print("================================")
    print(resultado)
    print("================================\n")



    return resultado





# =====================================
# Retornar último áudio do Draco
# =====================================

@app.get("/audio")

def obter_audio():


    if not PIPER_OUTPUT.exists():


        return {

            "success": False,

            "message": "Áudio não encontrado."

        }



    return FileResponse(

        path=PIPER_OUTPUT,

        media_type="audio/wav",

        filename="output.wav"

    )