"""
Draco AI
Voice - Wake Assistant

Fluxo (um ciclo por ativação, sem exceções):

WAITING_WAKE
    ↓ wake word detectada (detector é pausado IMEDIATAMENTE)
WAKE_WORD_DETECTED → "Estou ouvindo"
    ↓
LISTENING → grava exatamente UMA pergunta (VAD decide o fim)
    ↓
PROCESSING → Speech To Text -> Brain -> LLM
    ↓
SPEAKING → reproduz a resposta em áudio
    ↓
WAITING_WAKE (novo ciclo, detector reativado só depois de um
              intervalo de acomodação + flush)

Controle de pausa/retomada (unificado):

O pause/resume do detector de wake word não é mais exclusivo
do ciclo interno. Os métodos públicos notificar_inicio_playback()
e notificar_fim_playback() são o ÚNICO ponto de entrada para
pausar/retomar, usados tanto pelo ciclo interno (quando o
próprio Draco fala "Estou ouvindo" ou a resposta final) quanto
por QUALQUER reprodução de áudio externa (ex.: o frontend
tocando a resposta do botão de microfone).

Isso garante que a wake word nunca vai reconhecer a própria
voz do Draco, não importa de onde o áudio esteja sendo
reproduzido.

Modo debug:

wake_word_debug=True imprime o score de todo frame avaliado
pelo detector, mesmo abaixo do threshold. Útil apenas para
calibrar um modelo customizado (ex.: draco.onnx) recém
treinado. Deixe False em uso normal.

Integração com o servidor (main.py):

Este módulo pode reaproveitar um VoiceManager já existente
(passado via voice_manager=), evitando carregar Whisper e
Piper duas vezes na memória quando roda integrado ao FastAPI.
Se voice_manager=None (uso isolado, "python -m
backend.voice.wake_assistant"), ele cria sua própria
instância, como sempre fez.
"""

import time
from pathlib import Path

import numpy as np
import soundfile as sf

from backend.voice.audio_stream import MicrophoneStream
from backend.voice.vad import VoiceActivityDetector
from backend.voice.open_wake_word import OpenWakeWordDetector
from backend.voice.conversation_state import (
    ConversationState,
    ConversationStateMachine,
)
from backend.voice.voice_manager import VoiceManager
from backend.voice.audio_player import AudioPlayer


class WakeWordAssistant:

    SAMPLE_RATE = 16000
    FRAME_MS = 30

    MAX_QUESTION_SECONDS = 15
    SILENCE_SECONDS_TO_STOP = 1.0
    MIN_SPEECH_SECONDS = 0.3

    # Intervalo de acomodação após qualquer reprodução de
    # áudio (ack, resposta final do ciclo interno, OU
    # resposta tocada pelo frontend), antes de descartar a
    # fila e reativar o detector de wake word.
    POST_SPEAKING_SETTLE_SECONDS = 0.4

    def __init__(
        self,
        wake_word_model_path=None,
        wake_word_model_name="hey_jarvis",
        wake_word_threshold=0.5,
        wake_word_debug=False,
        voice_manager=None,
    ):
        """
        voice_manager:
            Instância já existente de VoiceManager, para
            reaproveitar Whisper e Piper já carregados (usado
            quando o Wake Assistant roda integrado ao servidor
            principal, em main.py). Se None, cria sua própria
            instância — comportamento original, usado ao rodar
            este módulo isoladamente
            (python -m backend.voice.wake_assistant).
        """

        print("\nInicializando Wake Word Assistant...\n")

        if voice_manager is not None:

            self.voice_manager = voice_manager

            print(
                "[WakeAssistant] Reaproveitando VoiceManager "
                "já existente (Whisper/Piper compartilhados)."
            )

        else:

            self.voice_manager = VoiceManager()

        self.wake_detector = OpenWakeWordDetector(
            model_path=wake_word_model_path,
            model_name=wake_word_model_name,
            threshold=wake_word_threshold,
            debug=wake_word_debug,
        )

        self.vad = VoiceActivityDetector(
            sample_rate=self.SAMPLE_RATE
        )

        self.audio_player = AudioPlayer()

        self.state_machine = ConversationStateMachine()

        self.audio_dir = Path(__file__).parent / "audio"
        self.audio_dir.mkdir(exist_ok=True)

        # Referência ao stream de microfone ativo, exposta
        # para permitir flush() solicitado por fora do loop
        # principal (ex.: quando o playback do frontend
        # termina). Só existe enquanto start() está rodando.
        self._stream = None

        print("Wake Word Assistant pronto.\n")

    # =====================================
    # Estado atual (para consulta externa, ex.: API/frontend)
    # =====================================

    def obter_estado(self):
        """
        Retorna o nome do estado atual da máquina de estados,
        como string (ex.: "WAITING_WAKE", "LISTENING").
        """

        return self.state_machine.state.name

    # =====================================
    # Controle unificado de pausa/retomada
    #
    # ÚNICO ponto de entrada para pausar ou retomar o detector
    # de wake word. Usado tanto pelo ciclo interno quanto por
    # qualquer reprodução de áudio externa (ex.: frontend).
    # =====================================

    def notificar_inicio_playback(self, origem="desconhecida"):
        """
        Deve ser chamado IMEDIATAMENTE ANTES de qualquer áudio
        do Draco começar a ser reproduzido, não importa onde
        (caixa de som local ou <audio> do navegador).

        Pausa o detector de wake word, para que ele não
        reconheça a própria voz do Draco como uma nova
        ativação.
        """

        print(
            f"[WakeAssistant] Pausando detector "
            f"(origem: {origem})."
        )

        self.wake_detector.pausar()

    def notificar_fim_playback(self, origem="desconhecida"):
        """
        Deve ser chamado quando um áudio do Draco TERMINA de
        tocar (evento onended do <audio>, ou fim do
        AudioPlayer local).

        Aguarda um intervalo de acomodação (para o eco/
        reverberação terminar de chegar ao microfone), limpa
        o buffer de áudio acumulado nesse intervalo e só então
        retoma o detector.

        Proteção contra corrida:
        Se o próprio Wake Assistant estiver, neste exato
        momento, no meio de um ciclo interno seu (estado
        diferente de WAITING_WAKE), esta chamada é ignorada —
        quem é dono da retomada nesse caso é o próprio ciclo
        interno (_entrar_waiting_wake), que vai cuidar disso
        na hora certa. Evita reativar o detector cedo demais
        durante uma conversa já em andamento.
        """

        if self.state_machine.state != ConversationState.WAITING_WAKE:

            print(
                f"[WakeAssistant] Retomada solicitada por "
                f"'{origem}' ignorada — ciclo de wake word "
                f"próprio em andamento "
                f"({self.state_machine.state.name})."
            )

            return

        time.sleep(self.POST_SPEAKING_SETTLE_SECONDS)

        if self._stream is not None:

            self._stream.flush()

        self.wake_detector.retomar()

        print(
            f"[WakeAssistant] Detector retomado "
            f"(origem: {origem})."
        )

    # =====================================
    # Loop principal
    #
    # Cada iteração do while True é UM ciclo completo:
    # WAITING_WAKE -> ... -> SPEAKING -> (volta ao topo)
    # =====================================

    def start(self):

        print('\nAguardando a palavra de ativação "Draco"...\n')

        with MicrophoneStream(
            sample_rate=self.SAMPLE_RATE,
            frame_ms=self.FRAME_MS,
        ) as stream:

            self._stream = stream

            try:

                while True:

                    try:

                        self._executar_ciclo(stream)

                    except KeyboardInterrupt:

                        print(
                            "\nEncerrando Wake Word Assistant.\n"
                        )

                        break

                    except Exception as erro:

                        print(
                            f"[WakeAssistant] Erro no ciclo: {erro}"
                        )

                        stream.flush()

                        self.wake_detector.pausar()

            finally:

                self._stream = None

    # =====================================
    # Um ciclo completo de conversa
    #
    # Chamada exatamente uma vez por ativação de wake word.
    # Não chama a si mesma, não repete _gravar_pergunta().
    # =====================================

    def _executar_ciclo(self, stream):

        # ---- WAITING_WAKE ----
        self._entrar_waiting_wake(stream)

        self._aguardar_wake_word(stream)
        # Detector já foi pausado dentro de _aguardar_wake_word
        # assim que a wake word foi detectada.

        # ---- WAKE_WORD_DETECTED ----
        self._responder_estou_ouvindo()

        stream.flush()

        # ---- LISTENING (uma única vez) ----
        audio_pergunta = self._gravar_pergunta(stream)

        if audio_pergunta is None:

            # Nenhuma fala capturada após a wake word.
            # Ciclo encerra aqui, sem processar nem falar.
            # O próximo laço do while True volta para
            # WAITING_WAKE normalmente.
            return

        # ---- PROCESSING + SPEAKING ----
        self._processar_pergunta(audio_pergunta)

        # Ciclo TERMINADO. Não há nenhum caminho de volta para
        # LISTENING a partir daqui. O próximo ciclo só começa
        # na próxima iteração do while True, passando de novo
        # por WAITING_WAKE.

    # =====================================
    # Entrada em WAITING_WAKE
    #
    # Reaproveita notificar_fim_playback() em vez de ter sua
    # própria cópia de sleep+flush+retomar.
    # =====================================

    def _entrar_waiting_wake(self, stream):

        self.state_machine.transition(ConversationState.WAITING_WAKE)

        self.notificar_fim_playback(origem="ciclo_interno")

    # =====================================
    # Etapa 1 - Aguardar wake word (openWakeWord)
    # =====================================

    def _aguardar_wake_word(self, stream):

        inicio_espera = time.perf_counter()

        while True:

            frame = stream.read_frame()

            if frame is None:

                continue

            if self.wake_detector.detectar(frame):

                tempo_total = (
                    time.perf_counter() - inicio_espera
                ) * 1000

                print(
                    f"[TEMPO] Wake Word detectada em "
                    f"{tempo_total:.1f}ms | "
                    f"score={self.wake_detector.last_score:.3f} | "
                    f"inferencia={self.wake_detector.last_detection_time_ms:.2f}ms"
                )

                self.state_machine.transition(
                    ConversationState.WAKE_WORD_DETECTED
                )

                self.notificar_inicio_playback(
                    origem="wake_word_detectada"
                )

                return

    # =====================================
    # Etapa 2 - "Estou ouvindo"
    # =====================================

    def _responder_estou_ouvindo(self):

        try:

            audio_file = self.voice_manager.text_to_speech.speak(
                "Estou ouvindo.",
                filename="wake_ack.wav",
            )

            self.audio_player.play(audio_file)

        except Exception as erro:

            print(f"[WakeAssistant] Erro ao responder: {erro}")

    # =====================================
    # Etapa 3 - Gravar A pergunta (uma única vez)
    # =====================================

    def _gravar_pergunta(self, stream):

        self.state_machine.transition(ConversationState.LISTENING)

        frames_gravados = []

        frames_silencio_consecutivos = 0
        frames_fala_consecutivos = 0
        fala_iniciada = False

        frames_para_parar = int(
            self.SILENCE_SECONDS_TO_STOP * 1000 / self.FRAME_MS
        )

        frames_minimo_fala = int(
            self.MIN_SPEECH_SECONDS * 1000 / self.FRAME_MS
        )

        inicio = time.time()

        while time.time() - inicio < self.MAX_QUESTION_SECONDS:

            frame = stream.read_frame()

            if frame is None:

                continue

            frames_gravados.append(frame)

            em_fala = self.vad.is_speech(frame)

            if em_fala:

                frames_fala_consecutivos += 1
                frames_silencio_consecutivos = 0

                if frames_fala_consecutivos >= frames_minimo_fala:

                    fala_iniciada = True

            else:

                frames_fala_consecutivos = 0

                if fala_iniciada:

                    frames_silencio_consecutivos += 1

            if (
                fala_iniciada
                and frames_silencio_consecutivos >= frames_para_parar
            ):

                break

        if not fala_iniciada:

            print(
                "[WakeAssistant] Nenhuma fala detectada após "
                "a wake word."
            )

            return None

        return self._salvar_audio(frames_gravados)

    def _salvar_audio(self, frames):

        audio_bytes = b"".join(frames)

        audio_np = np.frombuffer(audio_bytes, dtype=np.int16)

        caminho = self.audio_dir / "wake_question.wav"

        sf.write(
            caminho,
            audio_np,
            self.SAMPLE_RATE,
        )

        return caminho

    # =====================================
    # Etapa 4 e 5 - Processar e responder
    #
    # Última etapa do ciclo. Não retorna para LISTENING.
    # =====================================

    def _processar_pergunta(self, audio_path):

        self.state_machine.transition(ConversationState.PROCESSING)

        resultado = self.voice_manager.process(audio_path)

        print("\n====== PERGUNTA (WAKE WORD) ======")
        print(resultado.get("user_text"))
        print("Resposta:", resultado.get("response"))
        print("===================================\n")

        self.state_machine.transition(ConversationState.SPEAKING)

        audio_resposta = resultado.get("audio_file")

        if audio_resposta:

            self.audio_player.play(audio_resposta)

        # FIM DO CICLO. A transição para WAITING_WAKE acontece
        # apenas no início do próximo ciclo, em
        # _entrar_waiting_wake(), garantindo que o settle +
        # flush + reativação do detector aconteçam sempre
        # juntos e nesta ordem.


if __name__ == "__main__":

    assistente = WakeWordAssistant(
        wake_word_model_path="backend/voice/models/draco.onnx",
        wake_word_threshold=0.5,
        wake_word_debug=False,
    )

    assistente.start()