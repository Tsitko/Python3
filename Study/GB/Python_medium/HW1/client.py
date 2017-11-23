import json

import socket

import config

___CONFIG___ = "Config.json"

___MSGSIZE___ = 1024

class Client(object):

    def __init__(self, config_path = ___CONFIG___):
        conf = config.Config(config_path)
        self._IP = conf.get_IP()
        self._port = conf.get_port()
        self._name = None

    def set_name(self,Name):
        self._name = Name

    def recv_msg(self):
        msg = self.sock.recv(___MSGSIZE___)
        return msg.decode("utf-8")

    def form_msg(self, myMsg):
        msg = json.dumps({"Name" : str(self._name), "Msg" : str(myMsg)})
        return msg.encode("utf-8")

    def send_msg(self, myMsg):
        self.sock=socket.socket()
        self.sock.connect((self._IP,self._port))
        self.sock.send(myMsg)

    def close_connection(self):
        self.sock.close()


if __name__=='__main__':

    client = Client()

    print("What is your name?")    

    client.set_name(input())
    
    print("What do you want from me?")    
    
    myMsg = (input())

    client.send_msg(client.form_msg(myMsg))

    msg=client.recv_msg()

    client.close_connection()

    msg=json.loads(msg)

    print(msg["Intro"])
    print(msg["Date"])
    print(msg["Conclusion"])

