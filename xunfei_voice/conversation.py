# coding:utf-8
'''
语音模块的入口：
tts_play()：
args： string 想要说的话， 自动调用
'''
import json
import chardet
from core.WebaiuiDemo import aiui
from core.ttsv2 import tts
from core.play_music import play_sound
from settings import SAVE_FILE
from record.record import recoder


class Conversation(object):
    def __init__(self):
        self.islocked = False
        self.iat_recoder = recoder()

    def get_a_conversation(self):
        self.iat_recoder.recode_wav()
        x_ans = aiui()
        x_ans = json.loads(x_ans, encoding="UTF-8")
        # print chardet.detect(x_ans)
        # f_ans = json.dumps(x_ans, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        text_ans = x_ans['data'][-1]['intent']['answer']['text']
        # print json.dumps(temp, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        print text_ans
        self.tts_play(text_ans)

    def tts_play(self, string):
        if not self.islocked:
            self.islocked = True  # 加锁
            audio_name = tts(string)
            if audio_name is not None:
                play_sound(SAVE_FILE)
            self.islocked = False  # 解锁
            print('unlock')
        else:
            print('waiting')

if __name__ == '__main__':
    # get_a_conversation()
    c = Conversation()
    # c.tts_play('我是H-I-T狗')
    while(True):
        c.get_a_conversation()
