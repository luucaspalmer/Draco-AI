import sounddevice as sd
import numpy as np


def callback(indata, frames, time, status):

    if status:
        print("STATUS:", status)

    volume = np.abs(
        np.frombuffer(indata, dtype=np.int16)
    ).mean()

    print("Volume:", volume)


stream = sd.RawInputStream(
    samplerate=16000,
    channels=1,
    dtype="int16",
    callback=callback
)

print("Testando microfone... fale alguma coisa")

with stream:
    while True:
        pass