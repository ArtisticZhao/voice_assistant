# coding:utf-8
from socket import socket, AF_INET, SOCK_DGRAM
import serial

GO_LIST = ["chair", "box", "door"]
ROS_PORT = 20000
SERIAL_LISTEN = '/dev/ttyUSB0'


class socket_sender(object):
    def __init__(self, addr, port):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.addr = addr
        self.port = port

    def send_data(self, data):
        self.sock.sendto(data, (self.addr, self.port))


class serial_listener(object):
    def __init__(self):
        self.ss = socket_sender('localhost', ROS_PORT)
        self.ser = serial.Serial(SERIAL_LISTEN, 9600, timeout=0.5)

    def read(self):
        while True:
            data = self.ser.readall()
            if data != '':
                if data.find('@IR#1') != 1:
                    print GO_LIST[int(data[-2])]
                    self.ss.send_data("go:" + GO_LIST[int(data[-2])])


if __name__ == '__main__':
    sl = serial_listener()
    sl.read()
