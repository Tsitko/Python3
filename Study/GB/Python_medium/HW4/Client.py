import json
import socket
from Message import Message
from ClientConfig import ClientConfig

___OKMESSAGES___ = ["no more messages", "authorised", "registered", "message accepted", "registration ok"]

class Client(object):
	def __init__(self, config_path):
		self.conf = ClientConfig(config_path)
		self.host = self.conf.get_host()
		self.port = self.conf.get_port()
		self.name = self.conf.get_name()
		self.login = self.conf.get_login()
		self.password = self.conf.get_password()

	def set_name(self, name):
		self.name = name
		self.conf.set_name(name)

	def set_login(self, login):
		self.login = login
		self.cong.set_login(login)

	def set_password(self, password):
		self.password = password
		self.conf.set_password(password)

	def form_message(self, reciever, text):
		msg = Message()
		result = msg.form_message("message",self.login,self.name, reciever, text)
		return result

	def form_ask_message(self, text = ""):
		msg = Message()
		result = msg.form_message("ask message",self.login,self.name, "Server", text)
		return result

	def form_registration_message(self):
		msg = Message()
		result = msg.form_message("registration message",self.login,self.name, "Server", self.password)
		return result

	def form_authorization_message(self):
		msg = Message()
		result = msg.form_message("authorization message",self.login,self.name, "Server", self.password)
		return result

	def form_add_contact_message(self, text):
		msg = Message()
		result = msg.form_message("add contact message",self.login,self.name, "Server", text)
		return result

	def check_message(self, message):
		return message.get_type()

	def parse_message(self, data):
		return Message(data)

	def handle_errors(self, msg):
		if msg.get_body() in ___OKMESSAGES___:
			pass
		else:
			print(msg.get_body())

	def print_message(self, msg):
		print(msg.get_sender_name())
		print(msg.get_date())
		print(msg.get_body())

	def ask_for_messages(self):
		self.socket = socket.socket()
		self.socket.connect((self.host, self.port))
		self.socket.send(self.form_ask_message().encode('utf-8'))
		while True:
			ans = self.socket.recv(2048).decode('utf-8')
			print(ans)
			ans = self.parse_message(ans)
			if self.check_message(ans) == "error message":
				self.handle_errors(ans)
				break
			else:
				self.print_message(ans)
		self.socket.close()


	def send_message(self, reciever, text):
		self.socket = socket.socket()
		self.socket.connect((self.host, self.port))
		self.socket.send(self.form_message(reciever, text).encode('utf-8'))
		ans = self.socket.recv(2048).decode('utf-8')
		ans = self.parse_message(ans)
		if self.check_message(ans) == "error message":
			self.handle_errors(ans)
		self.socket.close()

	def authorise(self):
		self.socket = socket.socket()
		self.socket.connect((self.host, self.port))
		self.socket.send(self.form_authorization_message().encode('utf-8'))
		ans = self.socket.recv(2048).decode('utf-8')
		ans = self.parse_message(ans)
		if self.check_message(ans) == "error message":
			self.handle_errors(ans)
		self.socket.close()

	def register(self):
		self.socket = socket.socket()
		self.socket.connect((self.host, self.port))
		self.socket.send(self.form_registration_message().encode('utf-8'))
		ans = self.socket.recv(2048).decode('utf-8')
		ans = self.parse_message(ans)
		if self.check_message(ans) == "error message":
			self.handle_errors(ans)
		self.socket.close()

	def add_contact(self, friend_login):
		self.socket = socket.socket()
		self.socket.connect((self.host, self.port))
		self.socket.send(self.form_add_contact_message(text = friend_login).encode('utf-8'))
		ans = self.socket.recv(2048).decode('utf-8')
		ans = self.parse_message(ans)
		if self.check_message(ans) == "error message":
			self.handle_errors(ans)
		self.socket.close()




c = Client("ClientConfig.json")
c.register()
c.authorise()
c.ask_for_messages()
c.add_contact("Login")
c.ask_for_messages()