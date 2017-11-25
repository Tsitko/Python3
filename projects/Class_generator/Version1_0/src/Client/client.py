___VERSION___ = 1.0

import json

import config

import socket

import os

from log import Log


___MSGSIZE___ = 1048576

___CONFIG___ = "config.json"

___GENERATEDCLASSESPATH___ = "GenClasses/"

___DESCRIPTIONCONFIGPATH___ = "description_config.json"

___DESCRIPTIONTEXTPATH___ = "DescText/"

class Client(object):
	def __init__(self, config_path = ___CONFIG___):
		conf = config.Config(config_path)
		self._IP = conf.get_IP()
		self._port = conf.get_port()

	@Log()
	def get_IP(self):
		return self._IP

	@Log()
	def get_port(self):
		return self._port

	@Log()
	def form_message(self, text_path, description_config_path):
		with open(text_path,"r") as f:
			text = f.read()
			f.close()
		with open(description_config_path,"r") as f:
			description_config = f.read()
			f.close()
		description_config = json.loads(description_config)
		msg = json.dumps({"Description text" : text, "Description config" : description_config})
		return msg.encode("utf-8")
		
	@Log()
	def form_class(self, server_message):
		server_message = json.loads(server_message.decode("utf-8"))
		data = server_message["Class"] + server_message["Init"]
		for msg in server_message["Methods"]:
			data = data + msg["Method"]
		return str(data)

	def run(self, description_text_path = ___DESCRIPTIONTEXTPATH___, 
		description_config_path = ___DESCRIPTIONCONFIGPATH___, 
		generated_classes_path = ___GENERATEDCLASSESPATH___):
		files = os.listdir(description_text_path)
		for file in files:
			sock = socket.socket()
			sock.connect((client.get_IP(), client.get_port()))
			sock.send(client.form_message(description_text_path + file, description_config_path))
			#time.sleep(2) 
			msg = sock.recv(___MSGSIZE___)
			if msg.decode('utf-8')[0:6] == "ERROR:":
				print("%s %s" % (file, msg.decode('utf-8')))
			else:
				if msg.decode('utf-8') == "":
					print("%s %s" % (file, "ERROR: wrong client config or class description format"))
				else:
					recv_class = client.form_class(msg)
					with open(generated_classes_path + file.split(".",1)[0] + ".py", "w") as f:
						f.write(recv_class)
						f.close()
						print("%s OK" % file)

			sock.close()


if __name__ == "__main__":
	client = Client()
	client.run()

	

