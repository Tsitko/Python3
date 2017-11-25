class Client(object):
	def __init__(self):
		self._name = None
		self._last_name = None

	def change_name(self, name):
		pass

	def change_last_name(self, last_name):
		pass

	def set_name(self, name):
		self._name = name

	def get_name(self):
		return self._name

	def set_last_name(self, last_name):
		self._last_name = last_name

	def get_last_name(self):
		return self._last_name

