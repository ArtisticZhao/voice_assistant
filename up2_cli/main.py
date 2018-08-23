# coding:utf-8
from SocketServer import BaseRequestHandler, ThreadingUDPServer
import threading
import logging
from tts_offline import tts_ser, ser_to_tts
from serial_server import serial_listener
'''
这个是运行在up2board上的，进行离线tts，以及处理舵机指令用
'''
logging.basicConfig(
    level=logging.INFO,
    format=
    '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    filename='info.log',
    filemode='w')

sl = serial_listener(ser_to_tts)


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
        logging.info("msg:" + msg)
        if msg.find('aiui:') != -1:  # change aiui mod
            if msg == 'aiui:ol':
                logging.info("aiui mode change : ONLINE")
                ser_to_tts.write('@AsrMode#2$')
            else:
                logging.info("aiui mode change : OFFLINE")
                ser_to_tts.write('@AsrMode#1$')
        if msg.find("motor:") != -1:
            smsg = msg.split(':')
            sl.ser_to_sk.go_direct(smsg[1])
        else:
            # speak mode
            tts_ser(msg)


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
    tts_ser('我是导盲精灵')
    logging.info("start system")
    up_ser = upper_socket_server()
    up_ser.go()

    sl.read_forever()
