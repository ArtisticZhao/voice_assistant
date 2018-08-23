# -*- coding: utf-8 -*-
import time
import serial

SERI_TO_YY = '/dev/ttyUSB1'

# gen serial link to tts
try:
    ser_to_tts = serial.Serial(SERI_TO_YY, 9600, timeout=0.5)
except Exception as e:
    print e
    ser_to_tts = None

TTS_HEADER = "@TextToSpeech#"  # add '$' to tail


def tts_ser(string):
    if isinstance(string, unicode):
        send_data = TTS_HEADER + string.encode('GB2312') + '$'
    else:
        send_data = TTS_HEADER + string.decode('UTF-8').encode('GB2312') + '$'
    ser_to_tts.write(send_data)
    time.sleep(0.3 * len(string))


if __name__ == '__main__':
    tts_ser('哈哈')
