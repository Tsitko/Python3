import json

___CONFIG___ = "config.json"

class Config(object):
	def __init__(self, config_path = ___CONFIG___):
		conf = self.get_config_json(config_path)
		self.set_IP(conf["IP"])
		self.set_port(conf["port"])

	def get_config_json(self, config_path):
		with open(config_path,"r") as f:
			data = f.read()
			f.close
			configData = json.loads(data)
		return configData

	def get_IP(self):
		return self._IP

	def get_port(self):
		return self._port

	def set_IP(self, IP):
		self._IP = IP

	def set_port(self, port):
		self._port = int(port)





