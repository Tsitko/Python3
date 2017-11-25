***Class generator***

**Version 1.0**

**Generating code frome text description**

1. Strings with "\*\*\*" and "\*\*" are passing
2. First non-passing string should start from your class name
3. Use word "have" to describe attributes
4. Use word "can" to describe methods
5. Use "is Initialyzing by setting" to describe initialization of your class

For example from this text:

Message:

have titile

have body

have sender, reciever and technical description

can form json

can form csv

can save json

can save csv

is initializing by setting title as Title, body as body text, sender = Test sender, reciever = Test reciever

You will get this code:

```python
class Message(object):
	def __init__(self):
		self._title = "Title"
		self._body = "body text"
		self._sender = "Test sender"
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
 
 ```
 
 For more information go to Documentation path
