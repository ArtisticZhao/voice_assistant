import json
import time
import hashlib
import base64
import logging
import requests
import parse

logging.basicConfig(level=logging.INFO)
appid ="5ae9b166"

apikey = {
    "iat":"0e3131d763b61111106e3131b164d844",
    "tts":"TTS_KEY",
    "ise":"ISE_KEY",
    "general":"GENERAL_KEY",
    "handwriting":"HANDWRITING_KEY"
}

url ={
    "iat":"http://api.xfyun.cn/v1/service/v1/iat",
    "tts":"http://api.xfyun.cn/v1/service/v1/tts",
    "ise":"http://api.xfyun.cn/v1/service/v1/ise",
    "general":"http://webapi.xfyun.cn/v1/service/v1/ocr/general",
    "handwriting":" http://webapi.xfyun.cn/v1/service/v1/ocr/handwriting"
}

IAT_AUDIO_APTH='output.mp3'
TTS_TEXT =''
ISE_AUDIO_PATH = ''
ISE_TEXT=''
IMAGE_PATH=''

def getToken(X_apikey,X_time,X_param):
    token = X_apikey + X_time+X_param
    m = hashlib.md5()
    m.update(token.encode(encoding=("utf-8")))
    X_checksum = m.hexdigest()
    return X_checksum

def getHeader(param,xapikey):
    X_header={
        "X-Appid" : appid,
        "X-CurTime":str(int(time.time()))
    }
    # logging.info(X_header)
    param = json.dumps(param)
    X_header['X-Param'] = base64.b64encode(param.encode(encoding="utf-8")).decode().strip('\n')
    X_header["X-CheckSum"] = getToken(xapikey,X_header["X-CurTime"],X_header['X-Param'])
    # logging.info(X_header)
    return X_header

def getAudioBody(filename):
    with open(filename,'rb') as f:
        file_content = f.read()
        base64_audio = base64.b64encode(file_content)
        f.close()
    body = {'audio':base64_audio}
    # body = parse.urlencode({'audio':base64_audio})  # //之前使用urllib，需要用urlencode
    return body

def getImgBody(filename):
    with open(filename,'rb') as f:
        file_content = f.read()
        base64_image = base64.b64encode(file_content)
        f.close()
    body = {'image':base64_image}
    return body

def getTextBody(text):
    body = {'text':text}
    return body

def getIseBody(filename,text):
    with open(filename,'rb') as f:
        file_content = f.read()
        base64_audio = base64.b64encode(file_content)
    body = {'audio':base64_audio,'text': text}
    return body

def iatweb():
    param = {
        # "speex_size":"60",           #否，speex音频帧率，speex音频必传
        # "scene": "main",             #否，情景模式
        # "vad_eos": "2000",           #否，后端点检测（单位：ms），默认1800
        "engine_type": "sms16k",       #是，引擎类型，可选值：sms16k（16k采样率普通话音频）、sms8k（8k采样率普通话音频）等，其他参见引擎类型说明
        "aue": "raw"                   #是，频编码，可选值：raw（未压缩的pcm或wav格式）、speex（speex格式）、speex-wb（宽频speex格式）
    }
    xapikey = apikey["iat"]
    header = getHeader(param,xapikey)
    body = getAudioBody(IAT_AUDIO_APTH)
    print(body)
    req = requests.post(url["iat"], headers=header, data=body)
    print(req.content.decode('utf-8'))
    jbody = json.loads(req.content.decode('utf-8'))
    print(jbody['data'])



def ttsweb():
    param = {
        "auf": "audio/L16;rate=16000",      #是，音频采样率，可选值：audio/L16;rate=8000，audio/L16;rate=16000
        "aue": "raw",                       #是，音频编码，可选值：raw（未压缩的pcm或wav格式），lame（mp3格式）
        "voice_name":"xiaoyan",             #是，发音人，可选值：详见发音人列表
        # "speed": "40",                      #否，语速，可选值：[0-100]，默认为50
        # "volume": "50",                     #否，音量，可选值：[0-100]，默认为50
        # "pitch": "50",                      #否，音高，可选值：[0-100]，默认为50
        # "engine_type": "x",                 #否，引擎类型，可选值：aisound（普通效果），intp65（中文），intp65_en（英文），mtts（小语种，需配合小语种发音人使用），x（优化效果），默认为inpt65
        # "ent":"x",                        #否，如果使用新的发音人，须将参数改为"ent":"x"
        "text_type": "text"                 #否，文本类型，可选值：text（普通格式文本），默认为text
    }
    xapikey = apikey["tts"]
    header = getHeader(param, xapikey)
    text = TTS_TEXT
    body = getTextBody(text)
    req = requests.post(url["tts"],data=body, headers=header)
    logging.info(req.headers)
    logging.info(req.status_code)
    if req.headers['Content-Type'] == "audio/mpeg":
        sid = req.headers['sid']
        if param["aue"] == "raw":
            with open( sid + ".wav", "wb") as f:
                f.write(req.content)
            f.close()
            print("wav文件合成完毕")
        else:
            with open(sid + ".mp3", "wb") as f:
                f.write(req.content)
            f.close()
            print("MP3文件合成完毕")
    else:
        print (req.text)

def iseweb():
    param = {
        "aue": "raw",                     #是，音频编码
        # "speex_size":"70" ,             #否，标准解码帧大小
        "result_level": "plain",          #否，评测结果等级，可选值： complete、 plain，默认为 complete
        "language": "cn",                 #是，评测语种，可选值： en（英语）、 cn（汉语）
        "extra_ability": "chapter",       #否，拓展能力，可选值：multi_dimension(全维度)、chapter（段落评测）
        "category": "read_sentence"       #是，评测题型，可选值： read_syllable（单字朗读，汉语专有）、 read_word（词语朗读）、 read_sentence（句子朗读）、read_chapter(段落朗读，需开通权限)
    }
    xapikey = apikey["ise"]
    header = getHeader(param,xapikey)
    audio = ISE_AUDIO_PATH
    text = ISE_TEXT
    body = getIseBody(audio,text)
    req = requests.post(url["ise"], data=body, headers=header)
    rbody = req.content.decode('utf-8')
    jbody = json.loads(rbody)
    print(jbody)

def ocrweb():
    xapikey = apikey["general"]
    param = {
        "language":"cn|en",         #是，语言，可选值：en（英文），cn|en（中英混合）
        "location":"false"          #否，是否返回文本位置信息，可选值：false（否），true（是），默认为false
    }
    header = getHeader(param, xapikey)
    body = getImgBody(IMAGE_PATH)
    req = requests.post(url["general"], data=body, headers=header)
    rbody = req.content.decode('utf-8')
    print(type(rbody),rbody)

def handweb():
    xapikey = apikey["handwriting"]
    param = {
        "language": "cn|en",  # 是，语言，可选值：en（英文），cn|en（中英混合）
        "location": "false"  # 否，是否返回文本位置信息，可选值：false（否），true（是），默认为false
    }
    header = getHeader(param, xapikey)
    print(header)
    body = getImgBody(IMAGE_PATH)
    req = requests.post(url["handwriting"], data=body, headers=header)
    rbody = req.content.decode('utf-8')
    print(rbody)

if __name__== '__main__':
    iatweb()
    # ttsweb()
    # iatweb()
    # ocrweb()
    # handweb()