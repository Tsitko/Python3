import socket

import sys

from log import Log

import config

___CONFIGPATH___ = 'config.json'

___MSGSIZE___ = 1024

class Client(object):
    
    @Log()
    def __init__(self, config_path = ___CONFIGPATH___):

        conf = config.Config(config_path)
        self._host = conf.get_IP()
        self._port = conf.get_port()

            

    @Log()
    def run(self):
        _arg = sys.argv[1]

        with socket.socket() as sock:

            self.socket = sock

            self.socket.connect((self._host, self._port))

            while True:
                if _arg == 'w':
                    msg = input('Eenter message: ')
                    if msg == 'exit':
                        break

                    sock.send(msg.encode('utf-8'))

                if _arg == 'r':
                    
                    data = self.socket.recv(int(___MSGSIZE___)).decode('utf-8')
                    print('Ansver is: ', data)


if __name__ == '__main__':

    client = Client()

    client.run()

