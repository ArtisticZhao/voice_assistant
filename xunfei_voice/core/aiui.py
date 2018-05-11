#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib2
import time
import json
import hashlib
import base64


def aiui(query):

    url = 'https://api.xfyun.cn/v1/aiui/v1/text_semantic'
    api_key = 'e397d6acc6004afea833fc407fed2ed2'
    param = {"scene": "main", "userid": "dgr"}

    x_appid = '5ae9b166'
    x_param = base64.b64encode(json.dumps(param).replace(' ', ''))
    # query = '哈尔滨天气'
    base_query = base64.b64encode(query)
    # body = urllib.urlencode({'text': base_query})
    body = 'text=' + base_query
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(
        api_key + str(x_time) + x_param + body).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    print(body)
    req = urllib2.Request(url, body, x_header)
    result = urllib2.urlopen(req)
    result = result.read()
    print(result)
    return result


if __name__ == '__main__':
    aiui('时间')
