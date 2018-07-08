# coding:utf-8
import serial


class Voice_Ctrl_Handler(object):
    def __init__(self):
        try:
            self.ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5) #use usb serial port
        except Exception as e:
            print e
            self.ser = None

    def switch(self, text):
        print "in"
        if self.ser is not None:
            if text.find(u'向左看') != -1:
                print 'left'
                self.ser.write('l')
                return True
            elif text.find(u'向右看') != -1:
                print 'right'
                self.ser.write('r')
                return True
            elif text.find(u'向前看') != -1:
                print 'forward'
                self.ser.write('f')   
                return True 
        return False
