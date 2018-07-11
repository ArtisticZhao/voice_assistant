# -*- coding: utf-8 -*-
import requests
import re
import time
import hashlib
import base64

from settings import SAVE_PATH, SAVE_FILE
from core import security

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


def tts(string):
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
