import json

class Config(object):

    def __init__(self,file):

        with open(file,"r") as f:
            data = f.read()
            f.close
            configData = json.loads(data)
            self._IP = str(configData["IP"])
            self._port = int(configData["port"])




    def get_IP(self):
        return self._IP


    def get_port(self):
        return self._port
