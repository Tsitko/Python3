class Message(object):
	def __init__(self):
		self._title = "Title"
		self._body = "body text"
		self._reciever = "Test reciever"


	def form_json(self):
		pass

	def form_csv(self):
		pass

	def save_json(self):
		pass

	def save_csv(self):
		pass

	def set_titile(self, titile):
		self._titile = titile

	def get_titile(self):
		return self._titile

	def set_body(self, body):
		self._body = body

	def get_body(self):
		return self._body

	def set_sender(self, sender):
		self._sender = sender

	def get_sender(self):
		return self._sender

	def set_reciever(self, reciever):
		self._reciever = reciever

	def get_reciever(self):
		return self._reciever

	def set_technical_description(self, technical_description):
		self._technical_description = technical_description

	def get_technical_description(self):
		return self._technical_description

