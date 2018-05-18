#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import urllib.request
import json
import hashlib
import base64


def iat():
    f = open("output.wav", 'rb')
    file_content = f.read()
    base64_audio = base64.b64encode(file_content)
    body = urllib.parse.urlencode({'audio': base64_audio})

    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    api_key = '0e3131d763b61111106e3131b164d844'
    param = {"engine_type": "sms16k", "aue": "raw"}

    x_appid = '5ae9b166'
    x_param = base64.b64encode(json.dumps(param).replace(' ', ''))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(api_key + str(x_time) + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    print(body)
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    print(result)
    return result


if __name__ == '__main__':
    iat()