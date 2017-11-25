import unittest

import json

import server

import config

from data_processor import DataProcessor

from description_config import DescriptionConfig

___CONFIG___ = "config.json"

class ServerTestCases(unittest.TestCase):
	def test_server_init(self):
		conf = config.Config(___CONFIG___)
		test_server = server.Server(___CONFIG___)
		self.assertEqual(test_server._IP, conf.get_IP())
		self.assertEqual(test_server._port, conf.get_port())
		self.assertEqual(test_server._clients, list())

class DataProcessorTestCases(unittest.TestCase):
	def test_form_message(self):
		test_data_processor = DataProcessor()
		test_parsed_data = {"Class" : {"Name" : "User", "Initialization" : [{}], "Methods" : [{"Method" : "get_apples", "Attributes" : ["apples"]},
								{"Method" : "give_apples", "Attributes" : ["apples"]}], "Attributes" : ["apples"]}}
		test_message = {"Class" : "class User(object):\n",
						"Init" : "	def __init__(self):\n		self._apples = None\n\n",
						"Methods" : [{"Method" : "	def get_apples(self, apples):\n		pass\n\n"},
						 {"Method" : "	def give_apples(self, apples):\n		pass\n\n"},
						 {"Method" : "	def set_apples(self, apples):\n		self._apples = apples\n\n"},
						 {"Method" : "	def get_apples(self):\n		return self._apples\n\n"}]}
		test_message = json.dumps(test_message)
		self.assertEqual(test_data_processor.form_message(test_parsed_data), test_message.encode('utf-8'))

	def test_clean_strings(self):
		test_data_processor = DataProcessor()
		test_input_string = "***Smth***\n\n**Smth more**\n     \n1. How are you? Are you here?!\n\n2. Hi, I'm Alex. And you?"
		test_output_string = "How are you Are you here\nHi, Im Alex And you\n"
		data_processor_output = test_data_processor.clean_strings(test_input_string)
		self.assertEqual(data_processor_output, test_output_string)

	def test_parse_methods(self):
		data = {"Attribute keywords": ["have ", "must have ", "has "], "Method keywords": ["can ", "should "],
				"Initialization keywords": {"Attribute keywords": ["is initializing by setting ", "by default get "],
				"Attribute values keywords": [" as ", " equal to ", " = "]}}
		description_config = DescriptionConfig(data)
		test_data_processor = DataProcessor()
		test_attributes = ["apples", "oranges"]
		test_line1 = "Client can swim"
		test_line2 = "can give apples, take apples and eat oranges"
		test_output1 = [{"Method" : "swim", "Attributes" : []}]
		test_output2 = [{"Method" : "give apples", "Attributes" : ["apples"]}, {"Method" : "take apples", "Attributes" : ["apples"]},
						{"Method" : "eat oranges", "Attributes" : ["oranges"]}]
		self.assertEqual(test_data_processor.parse_methods(test_line1, test_attributes, description_config), test_output1)
		self.assertEqual(test_data_processor.parse_methods(test_line2, test_attributes, description_config), test_output2)

	def test_parse_initialization(self):
		data = {"Attribute keywords": ["have ", "must have ", "has "], "Method keywords": ["can ", "should "],
				"Initialization keywords": {"Attribute keywords": ["is initializing by setting ", "by default get "],
				"Attribute values keywords": [" as ", " equal to ", " = "]}}
		description_config = DescriptionConfig(data)
		test_data_processor = DataProcessor()
		test_attributes = ["apples", "oranges"]
		test_line1 = "Client is initializing by setting apples as 1, oranges as ten"
		test_line2 = "is initializing by setting apples = 1 and oranges = 5"
		test_output1 = ["apples", "oranges"], [1, "ten"]
		test_output2 = ["apples", "oranges"], [1, 5]
		self.assertEqual(test_data_processor.parse_initialization(test_line1, test_attributes, description_config), test_output1)
		self.assertEqual(test_data_processor.parse_initialization(test_line2, test_attributes, description_config), test_output2)

	def test_parse_attributes(self):
		data = {"Attribute keywords": ["have ", "must have ", "has "], "Method keywords": ["can ", "should "],
				"Initialization keywords": {"Attribute keywords": ["is initializing by setting ", "by default get "],
				"Attribute values keywords": [" as ", " equal to ", " = "]}}
		description_config = DescriptionConfig(data)
		test_data_processor = DataProcessor()
		test_line1 = "Client have apples"
		test_line2 = "have apples, oranges and bananas"
		test_output1 = ["apples"]
		test_output2 = ["apples", "oranges", "bananas"]
		self.assertEqual(test_data_processor.parse_attributes(test_line1, description_config), test_output1)
		self.assertEqual(test_data_processor.parse_attributes(test_line2, description_config), test_output2)

	def test_make_lines(self):
		test_data_processor = DataProcessor()
		input1 = "string1\nstring2\n"
		input2 = "string1\nstring2\nstring3\n"
		output1 = ["string1", "string2"]
		output2 = ["string1", "string2", "string3"]
		self.assertEqual(test_data_processor.make_lines(input1), output1)
		self.assertEqual(test_data_processor.make_lines(input2), output2)

	def test_check_attr(self):
		test_data_processor = DataProcessor()
		test_attributes = ["name", "last name"]
		test_line1 = "change name"
		test_line2 = "change last name"
		self.assertEqual(test_data_processor.check_attr("name", test_attributes, test_line1), 1)
		self.assertEqual(test_data_processor.check_attr("name", test_attributes, test_line2), 0)
		self.assertEqual(test_data_processor.check_attr("last name", test_attributes, test_line2), 1)  

	def test_make_val(self):
		test_data_processor = DataProcessor()
		val1 = "5"
		val2 = "5.2"
		val3 = "5.0"
		val4 = "char"
		self.assertEqual(test_data_processor.make_val(val1), 5)
		self.assertEqual(test_data_processor.make_val(val2), 5.2)
		self.assertEqual(test_data_processor.make_val(val3), 5)
		self.assertEqual(test_data_processor.make_val(val4), "char")

	def test_make_name(self):
		test_data_processor = DataProcessor()
		name1 = ""
		name2 = "name"
		name3 = "word1 word2"
		name4 = "word1 word2 word3"
		self.assertEqual(test_data_processor.make_name(name1), "")
		self.assertEqual(test_data_processor.make_name(name2), "name")
		self.assertEqual(test_data_processor.make_name(name3), "word1_word2")
		self.assertEqual(test_data_processor.make_name(name4), "word1_word2_word3")



if __name__ == '__main__':
	
	unittest.main()