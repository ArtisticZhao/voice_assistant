# coding:utf-8
from SocketServer import BaseRequestHandler, ThreadingUDPServer
import time
import threading
from conversation import Conversation

c = Conversation()


class Handler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        # Get message and client socket
        msg, _ = self.request
        print(msg)  # write control function down here!
        if msg.find('cmd:') != -1:  # cmd mode
            if msg == 'cmd:getname':
                # get name for facenet
                print("recv cmd:getname!")
                c.is_getname_mode = True
        else:
            # speak mode
            c.tts_play(msg)


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
    up_ser = upper_socket_server()
    up_ser.go()

    while (True):
        pass
        while (not c.iat_recoder.recode_wav() and c.is_getname_mode):
            pass
        if c.is_getname_mode:
            print("getname mode")
            c.get_name()
        elif c.isconversation:
            c.get_a_conversation()
            continue
        else:
            print "pre conversation"
            c.pre_conversation()
        time.sleep(1)
