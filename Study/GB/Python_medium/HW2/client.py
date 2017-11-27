import socket

import sys

from log import Log

import config

from datetime import datetime

import json

___CONFIGPATH___ = 'config.json'

___MSGSIZE___ = 1024

class Client(object):
    
    @Log()
    def __init__(self, config_path = ___CONFIGPATH___):

        conf = config.Config(config_path)
        self._host = conf.get_IP()
        self._port = conf.get_port()
        self._name = None

    def set_name(self,name):
        self._name = name

    def get_name(self):
        return self._name

    @Log()
    def run(self):
        _arg = sys.argv[1]
        if _arg == 'w':
            self._name = input('Enter your name: ')

        with socket.socket() as sock:

            self.socket = sock

            self.socket.connect((self._host, self._port))

            while True:
                if _arg == 'w':
                    msg = input('Eenter message: ')
                    if msg == 'exit':
                        break
                    date_time = datetime.now()
                    dt = '%s-%s-%s %s:%s' % (date_time.day,
                                              date_time.month,
                                              date_time.year,
                                              date_time.hour,
                                              date_time.minute)
                    final_msg = json.dumps({"Name" : self._name,
                                            "Date and time" : dt,
                                            "Message" : msg})

                    sock.send(final_msg.encode('utf-8'))

                if _arg == 'r':
                    
                    data = self.socket.recv(int(___MSGSIZE___)).decode('utf-8')
                    data = json.loads(data)
                    print('%s\n%s\n%s' % (data["Name"], data["Date and time"],
                                          data["Message"]))


if __name__ == '__main__':

    client = Client()

    client.run()

