class User(object):
	def __init__(self):
		self._login = "test user"
		self._password = 123


	def login_to_system(self, login):
		pass

	def send_message(self):
		pass

	def receive_message(self):
		pass

	def set_login(self, login):
		self._login = login

	def get_login(self):
		return self._login

	def set_password(self, password):
		self._password = password

	def get_password(self):
		return self._password

