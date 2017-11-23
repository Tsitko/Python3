import socket

import sys

from log import Log

class Client(object):
    
    @Log()
    def __init__(self, host, port):

        self._host = str(host)

        self._port = int(port)

    @Log()
    def recv(self, size):
        data = sock.recv(int(size)).decode('utf-8')
        return data

    @Log()
    def form_msg(self):
        msg = input('Eenter message: ')

        return msg

               

    @Log()
    def run(self):
        _arg = sys.argv[1]

        with socket.socket() as sock:

            self.socket = sock

            self.socket.connect((self._host, self._port))

            while True:
                if _arg == 'w':
                    msg = self.form_msg()
                    if msg == 'exit':
                        break

                    sock.send(msg.encode('utf-8'))

                if _arg == 'r':

                    print('Ansver is: ', self.recv(1024))


if __name__ == '__main__':

    client = Client('localhost', 8001)

    client.run()
    # sock = socket.socket()

    # sock.connect(('localhost', 8005))


    # massage = sock.recv(1024)

    # sock.close()

    # print(massage)
