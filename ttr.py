#! /usr/bin/env python  
# -*- coding: utf-8 -*-  
# python version >3.5  
  
__author__ = 'onestab'  
  
import sys, os, time  
from datetime import datetime  
from ctypes import *  
  
dll = windll.LoadLibrary("msc.dll")  
login_params = b"appid = 12345678, work_dir = ."  
session_begin_params = b"engine_type = local, voice_name = xiaoyan, text_encoding = UTF8, tts_res_path = fo|res\\tts\\xiaoyan.jet;fo|res\\tts\\common.jet, sample_rate = 16000, speed = 80, volume = 70, pitch = 50, rdn = 0"  
  
wav_header = b'RIFF6n\x06\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00}\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00'  
MSP_SUCCESS = 0  
MSP_TTS_FLAG_STILL_HAVE_DATA = 1  
MSP_TTS_FLAG_DATA_END = 2  
MSP_TTS_FLAG_CMD_CANCELED = 4  
  
filename = "tts_sample.wav"  
  
class Msp:  
    def __init__(self):  
        pass  
  
    def login(self):  
        ret = dll.MSPLogin(None, None, login_params)  
        print(('MSPLogin =>'), ret)  
  
    def tts(self, text, filename, session_begin_params):  
        ret, audio_len, synth_status, getret, wav_datasize = c_int(), c_int(), c_int(), c_int(), c_int()   
        sessionID = dll.QTTSSessionBegin(session_begin_params, byref(ret))  
        ret = dll.QTTSTextPut(sessionID, text, len(text), None)  
  
        wavFile = open(filename, 'wb')  
        wavFile.write(wav_header)  
        while True:  
            data = dll.QTTSAudioGet(sessionID, byref(audio_len), byref(synth_status), byref(getret))  
            if audio_len.value>0:  
                print('datasize:            %d\r' % wav_datasize.value, end='\r')  
            if getret.value != MSP_SUCCESS:  
                break  
            if data:  
                wavFile.write(string_at(data, audio_len))  
                wav_datasize.value += audio_len.value  
            if synth_status.value == MSP_TTS_FLAG_DATA_END:  
                break  
            #time.sleep(0.01)  
        # fix wav header  
        WAVE_HEADER_SIZE = 44  
        if wav_datasize.value>0:  
            wav_size8 = c_int()  
            wav_size8.value = WAVE_HEADER_SIZE + wav_datasize.value - 8  
            wavFile.seek(4)  
            wavFile.write(wav_size8)  
            wavFile.seek(40)  
            wavFile.write(wav_datasize)  
        wavFile.close()  
        dll.QTTSSessionEnd(sessionID, "Normal")  
  
if __name__ == "__main__":  
    text = "欢迎来到方工的CSDN博客。CSDN创立于1999年，是中国专业的IT技术社区和开发者服务平台。拥有5000万注册用户以及60万注册企业及合作伙伴。"  
    print(text)  
    msp = Msp()  
    msp.login()  
    msp.tts(text.encode('U8'), filename, session_begin_params)  