import json
import datetime

class Message(object):
	def __init__(self, msg = ""):
		if msg != "":
			self.msg = json.loads(msg)
		else:
			self.msg = {}

	def get_type(self):
		return self.msg["type"]
	def get_sender(self):
		return self.msg["sender"]
	def get_reciever(self):
		return self.msg["reciever"]
	def get_sender_name(self):
		return self.msg["sender name"]
	def get_body(self):
		return self.msg["body"]
	def get_date(self):
		return self.msg["date"]

	def set_type(self, Type):
		self.msg["type"] = Type
	def set_sender(self, sender):
		self.msg["sender"] = sender
	def set_reciever(self, reciever):
		self.msg["reciever"] = reciever
	def set_sender_name(self, sender_name):
		self.msg["sender name"] = sender_name
	def set_body(self, body):
		self.msg["body"] = body
	def set_date(self):
		dt = datetime.datetime.now()
		self.msg["date"] = "%s-%s-%s %s:%s" % (dt.day, dt.month, dt.year, dt.hour, dt.minute)


	def form_message(self, Type, sender, sender_name, reciever, body):
		self.set_type(Type)
		self.set_sender(sender)
		self.set_reciever(reciever)
		self.set_sender_name(sender_name)
		self.set_body(body)
		self.set_date()
		return json.dumps(self.msg)

	

