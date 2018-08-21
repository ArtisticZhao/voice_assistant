# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64
import serial

from settings import SAVE_PATH, SAVE_FILE, V_MODE, SERI_TO_YY
from core import security

# gen serial link to tts
try:
    ser_to_tts = serial.Serial(SERI_TO_YY, 9600, timeout=0.5)
except Exception as e:
    print e
    ser_to_tts = None

TTS_HEADER = "@TextToSpeech#"  # add '$' to tail

URL = "http://api.xfyun.cn/v1/service/v1/tts"
AUE = "raw"

APPID = security.TTS_ID
API_KEY = security.TTS_KEY


def getHeader():
    curTime = str(int(time.time()))
    param = "{\"aue\":\"" + AUE + "\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"xiaoyan\",\"engine_type\":\"intp65\"}"
    paramBase64 = base64.b64encode(param)
    m2 = hashlib.md5()
    m2.update(API_KEY + curTime + paramBase64)
    checkSum = m2.hexdigest()
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'X-Real-Ip': '127.0.0.1',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header


def getBody(text):
    data = {'text': text}
    return data


def writeFile(file, content):
    with open(file, 'wb') as f:
        f.write(content)
    f.close()


def tts(string, mode):
    if mode == "xf":
        tts_xf(string)
    else:
        tts_ser(string)


def tts_ser(string):
    if isinstance(string, unicode):
        send_data = TTS_HEADER + string.encode('GB2312') + '$'
    else:
        send_data = TTS_HEADER + string.decode('UTF-8').encode('GB2312') + '$'
    ser_to_tts.write(send_data)
    time.sleep(0.3 * len(string))


def tts_xf(string):
    r = requests.post(URL, headers=getHeader(), data=getBody(string))
    print r.headers
    contentType = r.headers['Content-Type']
    if contentType == "audio/mpeg":
        sid = r.headers['sid']
        if AUE == "raw":
            writeFile(SAVE_FILE, r.content)
        else:
            writeFile(SAVE_PATH + 'tts' + ".mp3", r.content)
        print("success, sid = " + sid)
        return sid
    else:
        print r.text


if __name__ == '__main__':
    tts('哈哈')
