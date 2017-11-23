import sys

import json

import socket

import datetime

import config


___CONFIG___ = "Config.json"

___MSGSIZE___ = 1024

class Server(object):

    def __init__(self, config_path = ___CONFIG___):
        conf = config.Config(config_path)
        self._IP = conf.get_IP()
        self._port = conf.get_port()
        self.sock=socket.socket()

    def open_connection(self, connections):
        self.sock.bind((self._IP, self._port))
        self.sock.listen(connections)

    def close_connection(self):
            print('-'*50, '\nServer stopped.\n', '-'*50)
            self.sock.close()
            sys.exit()

    def get_client(self):
        client, addr = self.sock.accept()
        print('-'*50, '\nConnected with %s\n' % str(addr), '-'*50)
        return client, addr


    def form_msg(self,client_msg):
        dt=datetime.datetime.now()
        dt_str=dt.strftime('%d-%B-%Y')
        client_msg=json.loads(client_msg)
        msg=json.dumps({"Intro" : "\nHi, " + client_msg["Name"] + "!",
                        "Date" : "Today is " + dt_str,
                        "Conclusion" : "It's not the best day to " + client_msg["Msg"]})
        return msg.encode('utf-8')

if __name__=='__main__':

    server = Server()

    server.open_connection(5)


    while True:

        try:

            client, addr = server.get_client()
            
            msg = client.recv(___MSGSIZE___).decode("utf-8")

            client.send(server.form_msg(msg))
            client.close()

        except KeyboardInterrupt:
            
            server.close_connection()

        except Exception as err:

            print(err)
            server.close_connection()





