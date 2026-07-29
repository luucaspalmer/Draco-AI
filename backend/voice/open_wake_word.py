"""
Draco AI
Voice - Open Wake Word Detector

Detector de Wake Word dedicado, baseado em openWakeWord.

Histórico de mudanças relevantes:

1) Download dos modelos ocorre apenas na primeira execução.
   Um arquivo marcador local (.oww_download_complete) indica
   que o cache já existe, evitando qualquer verificação de
   rede nas execuções seguintes.

2) O detector pode ser explicitamente pausado/retomado
   (ativo=False/True), permitindo que o restante do sistema
   (wake_assistant.py) desligue completamente a detecção
   durante os estados WAKE_WORD_DETECTED, LISTENING,
   PROCESSING e SPEAKING, evitando que o Draco detecte a
   própria voz.

3) retomar() reseta o estado interno do modelo (buffers de
   áudio e histórico de predição). Sem isso, a primeira
   chamada de detectar() após um resume podia devolver um
   score OBSOLETO (calculado antes da pausa), causando
   disparos falsos "fantasma" logo após o Draco terminar de
   responder.

4) Modo debug: quando debug=True, imprime o score de TODO
   frame avaliado (mesmo abaixo do threshold), permitindo
   diagnosticar problemas de sensibilidade/calibração do
   modelo customizado (ex.: draco.onnx) sem precisar adivinhar
   se o modelo está "quase" detectando ou não reagindo em
   absolutamente nada.
"""

import os
import time
from pathlib import Path

import numpy as np
import openwakeword
from openwakeword.model import Model


# =====================================
# Controle de download único
# =====================================

_MODELS_STATE_DIR = Path(__file__).parent / "models"

_DOWNLOAD_MARKER = _MODELS_STATE_DIR / ".oww_download_complete"


class OpenWakeWordDetector:

    def __init__(
        self,
        model_path=None,
        model_name="hey_jarvis",
        threshold=0.5,
        inference_framework="onnx",
        vad_threshold=None,
        cooldown_frames=10,
        debug=False,
        debug_min_score=0.02,
    ):
        """
        model_path:
            Caminho para um modelo .onnx customizado
            (ex.: "backend/voice/models/draco.onnx").
            Quando fornecido, tem prioridade sobre model_name.

        model_name:
            Nome de um modelo pré-treinado da biblioteca,
            usado apenas como fallback/teste.

        threshold:
            Score mínimo (0 a 1) para considerar a wake word
            detectada.

        inference_framework:
            "onnx" (recomendado, mais leve) ou "tflite".

        vad_threshold:
            Quando definido (0 a 1), ativa o VAD interno
            (Silero) do openWakeWord como filtro extra contra
            falsos positivos em ruído de fundo.

        cooldown_frames:
            Quantidade de frames ignorados logo após uma
            detecção, evitando múltiplos disparos seguidos
            para o mesmo evento de fala.

        debug:
            Quando True, imprime o score de TODO frame
            avaliado (acima de debug_min_score), mesmo que
            não ultrapasse o threshold. Útil para calibrar um
            modelo customizado recém-treinado. Deixe False em
            uso normal (gera muito log).

        debug_min_score:
            Score mínimo para o log de debug aparecer (evita
            poluir o console com ruído de fundo em 0.001).
        """

        self._garantir_modelos_baixados()

        modelo_alvo = model_path if model_path else model_name

        kwargs = {
            "wakeword_models": [modelo_alvo],
            "inference_framework": inference_framework,
        }

        if vad_threshold is not None:

            kwargs["vad_threshold"] = vad_threshold

        print(f"[OpenWakeWord] Carregando modelo: {modelo_alvo}")

        self.model = Model(**kwargs)

        self.wakeword_key = os.path.splitext(
            os.path.basename(modelo_alvo)
        )[0]

        self.threshold = threshold
        self.cooldown_frames = cooldown_frames
        self._cooldown_restante = 0

        # -------------------------------------------------
        # Gate de ativação. Enquanto ativo=False, detectar()
        # retorna False imediatamente, sem rodar inferência.
        # -------------------------------------------------
        self.ativo = True

        self.debug = debug
        self.debug_min_score = debug_min_score

        self.last_score = 0.0
        self.last_detection_time_ms = 0.0

        print(
            f"[OpenWakeWord] Pronto. Chave de detecção: "
            f"'{self.wakeword_key}' | threshold={threshold} | "
            f"debug={self.debug}"
        )

    # =====================================
    # Download único dos modelos
    # =====================================

    def _garantir_modelos_baixados(self):
        """
        Garante que os modelos do openWakeWord existam
        localmente, mas realiza essa verificação apenas UMA
        vez por instalação.

        Depois da primeira execução bem-sucedida, um arquivo
        marcador é criado e todas as execuções seguintes pulam
        completamente esta etapa (nenhuma checagem, nenhuma
        chamada de rede) — inicialização instantânea.

        Para forçar um novo download (ex.: modelos corrompidos
        ou atualização), basta apagar o arquivo:
        backend/voice/models/.oww_download_complete
        """

        if _DOWNLOAD_MARKER.exists():

            # Cache já confirmado em execução anterior.
            # Não faz nenhuma verificação adicional.
            return

        _MODELS_STATE_DIR.mkdir(parents=True, exist_ok=True)

        print(
            "[OpenWakeWord] Primeira execução detectada — "
            "baixando modelos (ocorre apenas uma vez)..."
        )

        openwakeword.utils.download_models()

        _DOWNLOAD_MARKER.touch()

        print("[OpenWakeWord] Modelos baixados e cacheados.")

    # =====================================
    # Controle de ativação
    # =====================================

    def pausar(self):
        """
        Desativa completamente o detector. Enquanto pausado,
        detectar() não executa nenhuma inferência.
        """

        if self.ativo:

            print("[OpenWakeWord] Detector PAUSADO.")

        self.ativo = False

    def retomar(self):
        """
        Reativa o detector, limpa o cooldown residual e
        reseta o estado interno do modelo (buffers de áudio
        e histórico de predição).

        Sem esse reset, o openWakeWord pode devolver, na
        primeira chamada após o resume, um score obsoleto
        (calculado antes da pausa), pois ele só recalcula a
        predição quando acumula amostras novas suficientes.
        Sem novas amostras ainda acumuladas, ele repete o
        último valor conhecido — o que causava disparos
        falsos "fantasma" logo após retomar a escuta.
        """

        if not self.ativo:

            print("[OpenWakeWord] Detector RETOMADO.")

        # Limpa buffers internos de áudio e a última predição
        # armazenada, garantindo que a próxima inferência seja
        # calculada do zero, sem herdar estado da fala anterior.
        try:

            self.model.reset()

        except AttributeError:

            # Fallback defensivo: caso a versão instalada da
            # biblioteca não exponha reset(), recriamos os
            # buffers de predição manualmente.
            try:

                for chave in list(self.model.prediction_buffer.keys()):

                    self.model.prediction_buffer[chave].clear()

            except Exception as erro:

                print(
                    f"[OpenWakeWord] Aviso: não foi possível "
                    f"resetar o estado interno do modelo "
                    f"({erro}). Score residual pode persistir "
                    f"na próxima detecção."
                )

        self.ativo = True
        self._cooldown_restante = 0
        self.last_score = 0.0
        self.last_detection_time_ms = 0.0

    # =====================================
    # Inferência
    # =====================================

    def _extrair_score(self, prediction: dict) -> float:

        if self.wakeword_key in prediction:

            return float(prediction[self.wakeword_key])

        if prediction:

            return float(list(prediction.values())[0])

        return 0.0

    def detectar(self, audio_bytes: bytes) -> bool:
        """
        Recebe um frame de áudio (bytes int16 mono, 16kHz) e
        retorna True se a wake word foi detectada.

        Se o detector estiver pausado (self.ativo=False), o
        frame é descartado imediatamente, sem nenhuma
        inferência.
        """

        if not self.ativo:

            return False

        if self._cooldown_restante > 0:

            self._cooldown_restante -= 1

            return False

        audio_np = np.frombuffer(audio_bytes, dtype=np.int16)

        if audio_np.size == 0:

            return False

        inicio = time.perf_counter()

        prediction = self.model.predict(audio_np)

        tempo_ms = (time.perf_counter() - inicio) * 1000

        score = self._extrair_score(prediction)

        self.last_score = score
        self.last_detection_time_ms = tempo_ms

        # -------------------------------------------------
        # DEBUG: mostra todo score relevante avaliado, mesmo
        # que não tenha cruzado o threshold. Serve para
        # calibrar modelos customizados recém-treinados.
        # -------------------------------------------------
        if self.debug and score > self.debug_min_score:

            print(
                f"[DEBUG score] {score:.3f} "
                f"(threshold={self.threshold}) | "
                f"inferencia={tempo_ms:.2f}ms"
            )

        detectado = score >= self.threshold

        if detectado:

            print(
                f"[OpenWakeWord] WAKE WORD DETECTADA | "
                f"score={score:.3f} | tempo_inferencia={tempo_ms:.2f}ms"
            )

            self._cooldown_restante = self.cooldown_frames

        return detectado