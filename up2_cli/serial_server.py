# coding:utf-8
from socket import socket, AF_INET, SOCK_DGRAM
import logging
import serial

GO_LIST = ["chair", "box", "door"]
ROS_PORT = 20000
SERIAL_LISTEN = '/dev/ttyUSB0'
SERIAL_TO_SK = '/dev/ttyACM0'
SERIAL_TO_SK1 = '/dev/ttyACM1'


class socket_sender(object):
    def __init__(self, addr, port):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.addr = addr
        self.port = port

    def send_data(self, data):
        self.sock.sendto(data, (self.addr, self.port))


class serial_listener(object):
    def __init__(self, serial_link):
        self.ss = socket_sender('localhost', ROS_PORT)
        self.ser = serial_link
        self.ser_to_sk = motor_ctrl_seri()

    def read_forever(self):
        while True:
            data = self.ser.readall()
            if len(data) == 1:
                data = ord(data)
                if data == 1 or data == 2 or data == 3:
                    logging.info("serial from voicemodel:motor ctrl:" +
                                 str(data))
                    self.ser_to_sk.go_direct(str(data))


class motor_ctrl_seri(object):
    def __init__(self):
        try:
            self.ser = serial.Serial(SERIAL_TO_SK, 9600, timeout=0.5)
        except Exception as e:
            print e
            self.ser = serial.Serial(SERIAL_TO_SK1, 9600, timeout=0.5)
        self.ser.flushInput()
        self.ser.flushOutput()

    def go_direct(self, direct):
        print direct
        if direct == '1' or direct == '2' or direct == '3':
            print('->send:' + 'qwer00' + direct + 'q')
            self.ser.write('qwer00' + direct + 'q')


if __name__ == '__main__':
    # sl = serial_listener()
    # sl.read()
    pass
