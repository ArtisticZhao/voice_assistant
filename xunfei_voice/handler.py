# coding:utf-8
import serial
from settings import SERI_TO_YY, SERI_TO_SK
'''
Start kit 接收的是语音模块的串口2指令，
使用语音模块的串口转发功能进行转发
'''


class Voice_Ctrl_Handler(object):
    def __init__(self):
        try:
            # use usb serial port
            self.ser = serial.Serial(SERI_TO_SK, 9600, timeout=0.5)
        except Exception as e:
            print e
            self.ser = None

    def switch(self, text):
        if self.ser is not None:
            if text.find(u'向左看') != -1:
                print 'left'
                self.ser.write('@IR#001&$')
                return True
            elif text.find(u'向右看') != -1:
                print 'right'
                self.ser.write('@IR#002&$')
                return True
            elif text.find(u'向前看') != -1:
                print 'forward'
                self.ser.write('@IR#003&$')
                return True
        return False
