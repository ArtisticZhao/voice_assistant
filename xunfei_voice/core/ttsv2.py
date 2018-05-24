# -*- coding: utf-8 -*-
import requests
import re
import time
import hashlib
import base64
import struct
import os
import sys


URL = "http://api.xfyun.cn/v1/service/v1/tts"
AUE = "raw"
APPID = "5ae9b166"
API_KEY = "0bc55dfd7956327353fbf2714f81c3cc"
abs_file = os.path.realpath(__file__)
abs_dir=abs_file[:abs_file.rfind("/")]
print("abs path is %s" % (abs_dir))
SAVE_PATH = os.path.join(abs_dir, '..', 'audio_temp')
print("save path is %s" % (SAVE_PATH))


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
            writeFile(SAVE_PATH + 'tts' + ".wav", r.content)
        else:
            writeFile(SAVE_PATH + 'tts' + ".mp3", r.content)
        print("success, sid = " + sid)
        return sid
    else:
        print r.text


if __name__ == '__main__':
    tts('哈哈')
