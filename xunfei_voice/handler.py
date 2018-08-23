# coding:utf-8
from settings import UP2_IP, MAIN_PORT, FACE_TRIGGER_PORT
from socketer import socket_sender
'''
Start kit 接收的是语音模块的串口2指令，
使用语音模块的串口转发功能进行转发
'''


class Voice_Ctrl_Handler(object):
    def __init__(self):
        self.sender_to_main = socket_sender(UP2_IP, MAIN_PORT)
        self.sender_to_trigger = socket_sender(UP2_IP, FACE_TRIGGER_PORT)

    def switch(self, text):
        if text.find(u'向左看') != -1:
            print 'left'
            self.sender_to_main.send_data('motor:2')
            return True
        elif text.find(u'向右看') != -1:
            print 'right'
            self.sender_to_main.send_data('motor:1')
            return True
        elif text.find(u'向前看') != -1:
            print 'forward'
            self.sender_to_main.send_data('motor:3')
            return True
        elif text.find(u'录入人脸') != -1:
            print 'rec face'
            self.sender_to_trigger.send_data('start:getface')
            return True
