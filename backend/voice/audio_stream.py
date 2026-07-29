"""
Draco AI
Voice - Audio Stream

Responsável por capturar áudio contínuo do microfone
em blocos pequenos, utilizado pelo modo Wake Word.

Diferente de Microphone (voice/microphone.py), que grava
uma duração fixa para o fluxo do botão, este módulo mantém
um stream contínuo aberto, necessário para detecção de
wake word e de fim de fala (VAD).
"""

import queue
import sounddevice as sd


class MicrophoneStream:
    """Stream contínuo de áudio do microfone em blocos (frames)."""

    def __init__(self, sample_rate=16000, frame_ms=30, channels=1):

        self.sample_rate = sample_rate
        self.frame_ms = frame_ms
        self.channels = channels
        self.frame_size = int(sample_rate * frame_ms / 1000)

        self._queue = queue.Queue()
        self._stream = None

    def _callback(self, indata, frames, time_info, status):

        if status:
            print(f"[MicrophoneStream] Status: {status}")

        self._queue.put(bytes(indata))

    def start(self):

        self._stream = sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=self.frame_size,
            channels=self.channels,
            dtype="int16",
            callback=self._callback,
        )

        self._stream.start()

    def stop(self):

        if self._stream is not None:

            self._stream.stop()
            self._stream.close()
            self._stream = None

    def read_frame(self, timeout=1.0):
        """Retorna o próximo frame de áudio (bytes int16 mono)."""

        try:

            return self._queue.get(timeout=timeout)

        except queue.Empty:

            return None

    def flush(self):
        """
        Descarta todos os frames pendentes na fila, sem
        processá-los.

        Usado para eliminar áudio acumulado durante períodos
        em que ninguém deveria estar "ouvindo" (ex.: enquanto
        o Draco está falando), evitando que esse backlog seja
        processado quando a escuta for retomada.
        """

        descartados = 0

        while True:

            try:

                self._queue.get_nowait()

                descartados += 1

            except queue.Empty:

                break

        if descartados:

            print(
                f"[MicrophoneStream] Flush: {descartados} "
                f"frames descartados."
            )

    def __enter__(self):

        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.stop()