# coding:utf-8
'''
语音模块的入口：
tts_play()：
args： string 想要说的话， 自动调用
'''
import json
from core.WebaiuiDemo import aiui
from core.ttsv2 import tts
from core.play_music import play_sound
from settings import SAVE_FILE
from record.record import recoder
from handler import Voice_Ctrl_Handler
from socketer import socket_sender


class Conversation(object):
    def __init__(self):
        self.islocked = False
        self.iat_recoder = recoder()
        self.isconversation = False
        self.handler = Voice_Ctrl_Handler()
        self.is_getname_mode = False
        self.sender = socket_sender('localhost', 20001)  # to facenet

    def aiui_iat(self):
        while (not self.iat_recoder.recode_wav()):
            # waiting input
            pass
        x_ans = aiui()
        x_ans = json.loads(x_ans, encoding="UTF-8")
        if int(x_ans['code']) == 0 and x_ans['data'][-1]['intent']:
            intent_res = x_ans['data'][-1]['intent']
            if intent_res:
                # not none
                return intent_res['text']
            else:
                return ''
        else:
            print x_ans
            return ''

    def get_name(self):
        print('lock')
        while (self.is_getname_mode):
            print "in get name"
            # get name until ok
            is_yes_or_no_mode = False
            if not is_yes_or_no_mode:
                self.tts_play("请说出您的名字")
                name_str = self.aiui_iat()
                while (type(name_str) != unicode):
                    self.tts_play("没听清楚请您再说一遍")
                    name_str = self.aiui_iat()
                name_str = name_str.encode('UTF-8')
                print name_str
                # name_str = unichr(name_str)
                self.tts_play("您叫" + name_str + "么？请回答对或错")

            is_yes_or_no_mode = True
            yes_or_no = self.aiui_iat()
            while (type(yes_or_no) != unicode):
                self.tts_play("没听清楚请您再说一遍")
                yes_or_no = self.aiui_iat()
            yes_or_no = str(yes_or_no.encode('UTF-8'))
            if '对' in yes_or_no:
                self.is_getname_mode = False
                self.sender.send_data(name_str)
            elif '错' in yes_or_no:
                is_yes_or_no_mode = False
        print('unlock')

    def pre_conversation(self):
        # res = iat()
        # res = json.loads(res, encoding="UTF-8")
        res = self.aiui_iat()
        print res
        # if int(res['code']) == 0:
        #    data = res['data']
        #    keywords = u'狗'
        #    if data.find(keywords) != -1:
        #        print 'start conversation'
        #        self.isconversation = True
        #        self.tts_play("你好！")
        #    else:
        #        print 'waiting'
        if res.find(u'狗') != -1:
            print 'start conversation'
            self.isconversation = True
            self.tts_play('你好！')
        else:
            print 'waiting'

    def get_a_conversation(self):
        x_ans = aiui()
        x_ans = json.loads(x_ans, encoding="UTF-8")
        if int(x_ans['code']) == 0 and x_ans['data'][-1]['intent']:
            # print chardet.detect(x_ans)
            # f_ans = json.dumps(
            # x_ans, sort_keys=True,
            # indent=4, separators=(',', ': '), ensure_ascii=False)
            # print f_ans
            intent_res = x_ans['data'][-1]['intent']
            # print "---->>>>>>>>debug0"
            # print json.dumps(
            #     intent_res,
            #     sort_keys=True,
            #     indent=4,
            #     separators=(',', ': '),
            #     ensure_ascii=False)
            # print "debug0<<<<<<<<----"
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
    # c.tts_play('我是H-I-T狗')
    # while (True):
    #     while (not c.iat_recoder.recode_wav()):
    #         pass
    #     if c.isconversation:
    #         c.get_a_conversation()
    #         continue
    #     else:
    #         print "pre conversation"
    #         c.pre_conversation()
    #     time.sleep(1)
    c.is_getname_mode = True
    c.get_name()
