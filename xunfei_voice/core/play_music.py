# coding: utf-8
"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
import time


CHUNK = 1024

def play_sound(path):
    # audio_path = '/home/bg2dgr/code/HIT_DOGS/voice_assistant/xunfei_voice/core/audio/hts0002487f@ch52f50e58f134477400.wav'
    audio_path = path
    wf = wave.open(audio_path, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)
    time.sleep(0.5)
    stream.stop_stream()
    stream.close()
    p.terminate()