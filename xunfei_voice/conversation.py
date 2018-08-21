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
from settings import SAVE_FILE, V_MODE, A_MODE
from record.record import recoder
from handler import Voice_Ctrl_Handler
from socketer import socket_sender
import logging


class Conversation(object):
    def __init__(self):
        self.islocked = False
        self.iat_recoder = recoder()
        self.isconversation = False
        self.handler = Voice_Ctrl_Handler()
        self.is_getname_mode = False
        self.sender = socket_sender('localhost', 20001)  # to facenet
        self.sender_to_navi = socket_sender('192.168.20.136', 20000)  # to navi
        self.vmode = V_MODE
        self.aiuimode = A_MODE

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
        while (self.is_getname_mode):
            logging.info("in get name")
            # get name until ok
            is_yes_or_no_mode = False
            if not is_yes_or_no_mode:
                self.tts_play("请说出您的名字")
                name_str = self.aiui_iat()
                while (type(name_str) != unicode):
                    self.tts_play("没听清楚请您再说一遍")
                    name_str = self.aiui_iat()
                name_str = name_str.encode('UTF-8')
                logging.info("get name:" + name_str)
                # name_str = unichr(name_str)
                self.tts_play("您叫" + name_str + "么？请回答正确或错误")

            is_yes_or_no_mode = True
            while (is_yes_or_no_mode):
                yes_or_no = self.aiui_iat()
                while (type(yes_or_no) != unicode):
                    self.tts_play("正确或错误?")
                    yes_or_no = self.aiui_iat()
                yes_or_no = str(yes_or_no.encode('UTF-8'))
                if '正确' in yes_or_no:
                    self.is_getname_mode = False
                    self.sender.send_data(name_str)
                    logging.info("done get name")
                    break
                elif '错误' in yes_or_no:
                    is_yes_or_no_mode = False

    def pre_conversation(self):
        x_ans = aiui()
        x_ans = json.loads(x_ans, encoding="UTF-8")

        if x_ans['data'] != 0:
            # 无错误
            # f_ans = json.dumps(
            #     x_ans,
            #     sort_keys=True,
            #     indent=4,
            #     separators=(',', ': '),
            #     ensure_ascii=False)
            # print f_ans
            data = x_ans['data'][-1]['intent']
            if data.get('data') is not None:
                try:
                    if_hello = data['data']['result'][0]['data'][0]['method']
                    if if_hello == 'hello':
                        self.isconversation = True
                        self.tts_play('你好')
                except Exception as e:
                    logging.error(e)
            else:
                logging.info('waitting')
        else:
            f_ans = json.dumps(
                data,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
                ensure_ascii=False)
            print f_ans

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

            # 检测是否切换回等待模式
            logging.info("in conversation:" + intent_res["text"])
            keywords = u'再见'
            if intent_res["text"].find(keywords) != -1:
                self.tts_play('再见！')
                self.isconversation = False
            elif self.handler.switch(intent_res["text"]):
                return
            # 检测是否为室内导航命令
            if intent_res.get('data') is not None:
                try:
                    if_go_where = intent_res['data']['result'][0]['data'][0][
                        'method']
                    if if_go_where == 'go_indoor_loc':
                        where = intent_res['data']['result'][0]['data'][1][
                            'location']
                        logging.info('indoor navi mode in')
                        logging.info(where)
                        self.sender_to_navi.send_data('Goal:' + where)

                except Exception as e:
                    logging.error("navi mode error")
                    logging.error(e)
            # 回答
            if intent_res.get('answer') is not None:
                text_ans = intent_res['answer']['text']
                logging.info("reply: " + text_ans)
                self.reply(text_ans)
            else:
                logging.error('dont understand')
        else:
            print "---->>>>>>>>error code !!!!!"
            try:
                j_ans = json.loads(x_ans)
                print j_ans
            except Exception as e:
                logging.error(e)
                print x_ans
                print e
            print "error code !!!!!<<<<<<<<----"

    def tts_play(self, string):
        if not self.islocked:
            self.islocked = True  # 加锁
            audio_name = tts(string, self.vmode)
            if audio_name is not None:
                play_sound(SAVE_FILE)
            self.islocked = False  # 解锁
        else:
            print('waiting')

    def reply(self, string):
        if self.aiuimode == 'online':
            self.tts_play(string)


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
    # c.is_getname_mode = True
    # c.get_name()

    c.pre_conversation()
