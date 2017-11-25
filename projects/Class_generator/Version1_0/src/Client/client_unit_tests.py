import unittest

import json

import client

import config

from subprocess import Popen, CREATE_NEW_CONSOLE, PIPE

import time

import os

___CONFIG___ = "config.json"

___GENERATEDCLASSESPATH___ = "GenClasses/"

___DESCRIPTIONCONFIGPATH___ = "description_config.json"

___DESCRIPTIONTEXTPATH___ = "DescText/"


class ClientTest(unittest.TestCase):
	def test_client_init(self):
		conf = config.Config(___CONFIG___)
		test_client = client.Client(___CONFIG___)
		self.assertEqual(test_client._IP, conf.get_IP())
		self.assertEqual(test_client._port, conf.get_port())

	def test_client_get_IP(self):
		conf = config.Config(___CONFIG___)
		test_client = client.Client(___CONFIG___)
		self.assertEqual(test_client.get_IP(), conf.get_IP())

	def test_client_get_IP(self):
		conf = config.Config(___CONFIG___)
		test_client = client.Client(___CONFIG___)
		self.assertEqual(test_client.get_port(), conf.get_port())

	def test_client_form_message(self):
		test_client = client.Client(___CONFIG___)
		with open(___DESCRIPTIONTEXTPATH___ + "User.md","r") as f:
			text = f.read()
			f.close
		with open(___DESCRIPTIONCONFIGPATH___,"r") as f:
			desc_conf = f.read()
			f.close
		desc_conf = json.loads(desc_conf)
		test_message = json.dumps({"Description text" : text, "Description config" : desc_conf})
		self.assertEqual(test_client.form_message(___DESCRIPTIONTEXTPATH___ + "User.md", ___DESCRIPTIONCONFIGPATH___), test_message.encode('utf-8'))


	def test_client_form_class(self):
		test_client = client.Client(___CONFIG___)
		test_server_message = json.dumps({"Class" : "class User(object):\n",
											"Init" : "    def __init__(self):\n        self._apples = 5\n        self._oranges = 7\n\n",
											"Methods" : [{"Method" : "    def give_apples(self, apples):\n        pass\n\n"},
														{"Method" : "    def get_apples(self, apples):\n        pass\n\n"},
														{"Method" : "    def give_oranges(self, oranges):\n        pass\n\n"},
														{"Method" : "    def get_oranges(self, oranges):\n        pass\n\n"}]})
		test_class_code = str("class User(object):\n    def __init__(self):\n        self._apples = 5\n        self._oranges = 7\n\n" +
		    					"    def give_apples(self, apples):\n        pass\n\n    def get_apples(self, apples):\n        pass\n\n"+
    							"    def give_oranges(self, oranges):\n        pass\n\n    def get_oranges(self, oranges):\n        pass\n\n")
		self.assertEqual(test_client.form_class(test_server_message.encode("utf-8")), test_class_code)

	def test_client_run(self):
		text = "monkey:\n have bananas\n can give bananas"
		if "Monkey.md" in os.listdir(___DESCRIPTIONTEXTPATH___):
			os.remove(___DESCRIPTIONTEXTPATH___ + "Monkey.md")
		if "Monkey.py" in os.listdir(___GENERATEDCLASSESPATH___):
			os.remove(___GENERATEDCLASSESPATH___ + "Monkey.py")
		with open(___DESCRIPTIONTEXTPATH___ + "Monkey.md", "w") as f:
			f.write(text)
			f.close()
		check1 = "Monkey.py" in os.listdir(___GENERATEDCLASSESPATH___)
		cl = Popen('python client.py', creationflags=CREATE_NEW_CONSOLE)
		time.sleep(2)
		cl.kill()
		check2 = "Monkey.py" in os.listdir(___GENERATEDCLASSESPATH___)
		if "Monkey.md" in os.listdir(___DESCRIPTIONTEXTPATH___):
			os.remove(___DESCRIPTIONTEXTPATH___ + "Monkey.md")
		if "Monkey.py" in os.listdir(___GENERATEDCLASSESPATH___):
			os.remove(___GENERATEDCLASSESPATH___ + "Monkey.py")
		self.assertNotEqual(check1, check2)

if __name__ == '__main__':
	unittest.main()