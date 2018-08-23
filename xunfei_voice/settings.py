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
REC_LEVEL = 3000

# voice mode
V_MODE = "remote"  # "xf" or "serial" or "remote"
A_MODE = "online"
# serial
SERI_TO_YY = "/dev/ttyUSB0"
SERI_TO_SK = "/dev/ttyACM0"

# recorder mode
REC_MODE = 'RELEASE'  # 'DEBUG' to show rec_level

# net config
UP2_IP = '192.168.20.136'
FACE_TRIGGER_PORT = 20003
NAVI_PORT = 20002
FACE_PORT = 20001
MAIN_PORT = 20000
