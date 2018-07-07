# coding:utf-8
'''
存放一些公共配置信息
'''
import os

# path to save
abs_file = os.path.realpath(__file__)
abs_dir = abs_file[:abs_file.rfind("/")]
SAVE_PATH = os.path.join(abs_dir, 'audio_temp')
SAVE_FILE = os.path.join(SAVE_PATH, 'tts.wav')
SAVE_REC = os.path.join(SAVE_PATH, 'rec.wav')

# recoder
REC_LEVEL = 500
