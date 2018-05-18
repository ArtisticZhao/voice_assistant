# coding:utf-8
'''
语音模块的入口：
tts_play()：
args： string 想要说的话， 自动调用
'''
from core.WebaiuiDemo import aiui
from core.ttsv2 import tts
from core.play_music import play_sound

class Conversation(object):
    def __init__(self):
        self.islocked = False

    def get_a_conversation(self):
        x_ans = aiui()
        print(x_ans)
        # tts()

    def tts_play(self, string):
        if not self.islocked:
            self.islocked = True  # 加锁
            audio_name = tts(string)
            if audio_name is not None:
                play_sound('/home/bg2dgr/audio/' + audio_name + '.wav')
            self.islocked = False  # 解锁
            print('unlock')
        else:
            print('waiting')

if __name__ == '__main__':
    # get_a_conversation()
    c = Conversation()
    c.tts_play('我是H-I-T狗')
