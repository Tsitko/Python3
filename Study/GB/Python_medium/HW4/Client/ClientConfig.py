import json

class ClientConfig(object):
	def __init__(self,config_path):
		with open(config_path, "r") as f:
			conf = json.loads(f.read())
			f.close()
			self.host = conf["host"]
			self.port = conf["port"]
			self.name = conf["name"]
			self.login = conf["login"]
			self.password = conf["password"]
		self.config_path = config_path
	

	def get_host(self):
		return self.host
	def get_port(self):
		return self.port
	def get_name(self):
		return self.name
	def get_login(self):
		return self.login
	def get_password(self):
		return self.password

	def set_host(self,host):
		with open(self.config_path, "r") as f:
			conf = json.loads(f.read())
			f.close()
			conf["host"] = host
			self.host = host
			with open(self.config_path, "w") as f:
				f.write(json.dumps(conf))
				f.close()

	def set_port(self,port):
		with open(self.config_path, "r") as f:
			conf = json.loads(f.read())
			f.close()
			conf["port"] = port
			self.port = port
			with open(self.config_path, "w") as f:
				f.write(json.dumps(conf))
				f.close()

	def set_name(self,name):
		with open(self.config_path, "r") as f:
			conf = json.loads(f.read())
			f.close()
			conf["name"] = name
			self.name = name
			with open(self.config_path, "w") as f:
				f.write(json.dumps(conf))
				f.close()

	def set_login(self,login):
		with open(self.config_path, "r") as f:
			conf = json.loads(f.read())
			f.close()
			conf["login"] = login
			self.login = login
			with open(self.config_path, "w") as f:
				f.write(json.dumps(conf))
				f.close()

	def set_password(self,password):
		with open(self.config_path, "r") as f:
			conf = json.loads(f.read())
			f.close()
			conf["password"] = password
			self.password = password
			with open(self.config_path, "w") as f:
				f.write(json.dumps(conf))
				f.close()