from pathlib import Path
import threading

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.brain import pensar
from backend.voice.voice_manager import VoiceManager
from backend.voice.wake_assistant import WakeWordAssistant



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
#
# Instância única, compartilhada entre o fluxo do botão
# (/voice) e o Wake Assistant. Evita carregar Whisper e
# Piper duas vezes na memória.
# =====================================

voice_manager = VoiceManager()



# =====================================
# Wake Word Assistant
#
# Reaproveita o voice_manager acima. Roda em thread separada
# porque seu loop principal (start()) é síncrono e bloqueante
# (leitura contínua de microfone).
# =====================================

wake_assistant = WakeWordAssistant(
    voice_manager=voice_manager,
    wake_word_model_path="backend/voice/models/draco.onnx",
)

_wake_thread = None



def _iniciar_wake_assistant_em_background():

    global _wake_thread

    _wake_thread = threading.Thread(

        target=wake_assistant.start,

        name="WakeWordAssistantThread",

        daemon=True

    )

    _wake_thread.start()

    print(
        "\n[Main] Wake Word Assistant iniciado em background.\n"
    )



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
# Ciclo de vida da aplicação
# =====================================

@app.on_event("startup")

def iniciar_servicos_em_background():

    _iniciar_wake_assistant_em_background()



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
# Comunicação por Voz (botão)
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


    # -------------------------------------------------
    # O frontend vai reproduzir o áudio da resposta agora.
    # Pausamos o detector de wake word ANTES de devolver a
    # resposta, para que ele não escute a própria voz do
    # Draco saindo das caixas de som do navegador.
    #
    # O detector só será reativado quando o frontend avisar
    # que o playback terminou (POST /voice/playback-finished),
    # disparado pelo evento onended do <audio>.
    # -------------------------------------------------

    wake_assistant.notificar_inicio_playback(

        origem="frontend_botao"

    )


    return resultado



# =====================================
# Fim de reprodução de áudio (frontend)
#
# Chamado pelo frontend quando o <audio> termina de tocar
# (evento onended). Aguarda o intervalo de acomodação, limpa
# o buffer de microfone e reativa o detector de wake word.
#
# Serve para QUALQUER reprodução de áudio feita pelo
# frontend, não apenas a do botão — basta chamar este mesmo
# endpoint sempre que um áudio do Draco terminar de tocar.
# =====================================

@app.post("/voice/playback-finished")

def playback_finished():

    wake_assistant.notificar_fim_playback(

        origem="frontend_botao"

    )

    return {

        "success": True,

        "estado": wake_assistant.obter_estado()

    }



# =====================================
# Status do Wake Word Assistant
#
# Permite ao frontend exibir o estado atual da escuta por
# voz (ex.: "aguardando", "ouvindo", "processando").
# =====================================

@app.get("/voice/wake-status")

def status_wake_assistant():

    return {

        "estado": wake_assistant.obter_estado(),

        "ativo": wake_assistant.wake_detector.ativo

    }



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