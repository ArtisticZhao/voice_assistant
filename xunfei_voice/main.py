# coding:utf-8
from SocketServer import BaseRequestHandler, ThreadingUDPServer
import time
import threading
import logging
from conversation import Conversation

logging.basicConfig(
    level=logging.INFO,
    format=
    '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    filename='info.log',
    filemode='w')

c = Conversation()


class Handler(BaseRequestHandler):
    '''
    @ 指令列表：
    cmd:getname     :启动获取名字功能
    mod:tts         :在线语音合成
    mod:ser         :离线语音合成
    aiui:ol         :在线语音识别
    aiui:off        :离线语音识别
    '''

    def handle(self):
        print('Got connection from', self.client_address)
        # Get message and client socket
        msg, _ = self.request
        print(msg)  # write control function down here!
        if msg.find('cmd:') != -1:  # cmd mode
            if msg == 'cmd:getname':
                # get name for facenet
                logging.info("start get name mode")
                c.is_getname_mode = True


class upper_socket_server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server = ThreadingUDPServer(('', 20000), Handler)

    def run(self):
        self.server.serve_forever()

    def go(self):
        self.setDaemon(True)
        self.start()


if __name__ == '__main__':
    c.tts_play('我是H-I-T狗')
    logging.info("start system")
    up_ser = upper_socket_server()
    up_ser.go()

    while (True):
        try:
            while (not c.iat_recoder.recode_wav() and not c.is_getname_mode):
                pass
            if c.is_getname_mode:
                logging.info('getname mode')
                c.get_name()
            elif c.isconversation:
                c.get_a_conversation()
                continue
            else:
                logging.info("pre conversation")
                c.pre_conversation()
            time.sleep(0.2)
        except Exception as e:
            logging.error(e)
