import json

class ServerConfig(object):
	def __init__(self,config_path):
		with open(config_path, "r") as f:
			conf = json.loads(f.read())
			f.close()
			self.host = conf["host"]
			self.port = conf["port"]
			self.DB_server = conf["connection string"]["DB server"]
			self.DB_user = conf["connection string"]["DB user"]
			self.DB_user_password = conf["connection string"]["DB user password"]
			self.DB_name = conf["connection string"]["DB name"]
	

	def get_host(self):
		return self.host
	def get_port(self):
		return self.port
	def get_DB_server(self):
		return self.DB_server
	def get_DB_user(self):
		return self.DB_user
	def get_DB_user_password(self):
		return self.DB_user_password
	def get_DB_name(self):
		return self.DB_name