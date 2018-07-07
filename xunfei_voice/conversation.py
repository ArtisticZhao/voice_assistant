# coding:utf-8
'''
语音模块的入口：
tts_play()：
args： string 想要说的话， 自动调用
'''
import json
import time
from core.iat import iat
from core.WebaiuiDemo import aiui
from core.ttsv2 import tts
from core.play_music import play_sound
from settings import SAVE_FILE
from record.record import recoder
from handler import Voice_Ctrl_Handler


class Conversation(object):
    def __init__(self):
        self.islocked = False
        self.iat_recoder = recoder()
        self.isconversation = False
        self.handler = Voice_Ctrl_Handler()

    def pre_conversation(self):
        res = iat()
        res = json.loads(res, encoding="UTF-8")
        if int(res['code']) == 0:
            data = res['data']
            keywords = u'狗'
            if data.find(keywords) != -1:
                print 'start conversation'
                self.isconversation = True
                self.tts_play("你好！")
            else:
                print 'waiting'

    def get_a_conversation(self):
        x_ans = aiui()
        x_ans = json.loads(x_ans, encoding="UTF-8")
        if int(x_ans['code']) == 0 and x_ans['data'][-1]['intent']:
            # print chardet.detect(x_ans)
            # f_ans = json.dumps(x_ans, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
            # print f_ans
            intent_res = x_ans['data'][-1]['intent']
            print "---->>>>>>>>debug0"
            print json.dumps(
                intent_res,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
                ensure_ascii=False)
            print "debug0<<<<<<<<----"
            print intent_res["text"]
            keywords = u'再见'
            if intent_res["text"].find(keywords) != -1:
                self.tts_play('再见！')
                self.isconversation = False
            elif self.handler.switch(intent_res["text"]):
                return
            if intent_res.get('answer') is not None:
                text_ans = intent_res['answer']['text']
                print text_ans
                self.tts_play(text_ans)
            else:
                print 'dont understand'
        else:
            print "---->>>>>>>>error code !!!!!"
            print json.dumps(
                x_ans,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
                ensure_ascii=False)
            print "error code !!!!!<<<<<<<<----"

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
    c = Conversation()
    c.tts_play('我是H-I-T狗')
    while (True):
        while (not c.iat_recoder.recode_wav()):
            pass
        if c.isconversation:
            c.get_a_conversation()
            continue
        else:
            print "pre conversation"
            c.pre_conversation()
        time.sleep(1)
