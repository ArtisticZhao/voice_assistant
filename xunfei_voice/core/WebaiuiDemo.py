# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64
from settings import SAVE_REC
from core import security

URL = "http://openapi.xfyun.cn/v2/aiui"
APPID = security.AIUI_ID
API_KEY = security.AIUI_KEY
AUE = "raw"
AUTH_ID = security.AIUI_AUTH_ID
DATA_TYPE = "audio"
SAMPLE_RATE = "16000"
SCENE = "main"
RESULT_LEVEL = "complete"
LAT = "39.938838"
LNG = "116.368624"
FILE_PATH = SAVE_REC


def buildHeader():
    curTime = str(int(time.time()))
    param = "{\"result_level\":\"" + RESULT_LEVEL + "\",\"auth_id\":\"" + AUTH_ID + "\",\"data_type\":\"" + DATA_TYPE + "\",\"sample_rate\":\"" + SAMPLE_RATE + "\",\"scene\":\"" + SCENE + "\",\"lat\":\"" + LAT + "\",\"lng\":\"" + LNG + "\"}"
    paramBase64 = base64.b64encode(param)

    m2 = hashlib.md5()
    m2.update(API_KEY + curTime + paramBase64)
    checkSum = m2.hexdigest()

    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
    }
    return header


def readFile(filePath):
    binfile = open(filePath, 'rb')
    data = binfile.read()
    return data


def aiui():
    r = requests.post(URL, headers=buildHeader(), data=readFile(FILE_PATH))
    return r.content


if __name__ == "__main__":
    r = requests.post(URL, headers=buildHeader(), data=readFile(FILE_PATH))
    print(r.content)