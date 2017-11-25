import unittest

import json

import description_config

___ATTRIBUTEKEYWORDS___ = ["have", "has"]

___METHODKEYWORDS___ = ["can", "have opportunity to"]

___INITIALIZATIONKEYWORDS___ = [{"Attribute keywords": ["initialyzing by setting", "by default sets"],
								"Attribute values keywords": ["as", "="]}]

___TESTDESCRIPTIONCONFIG___ = "test_description_config.json"

class DescriptionConfigTest(unittest.TestCase):
	def test_description_config_init(self):
		with open(___TESTDESCRIPTIONCONFIG___,"r") as f:
			data = f.read()
			f.close
			data = json.loads(data)
		desc_conf = description_config.DescriptionConfig(data)
		self.assertEqual(desc_conf._attribute_keywords, ___ATTRIBUTEKEYWORDS___)
		self.assertEqual(desc_conf._method_keywords, ___METHODKEYWORDS___)
		self.assertEqual(desc_conf._initialization_keywords, ___INITIALIZATIONKEYWORDS___)

	def test_description_config_set_attribute_keywords(self):
		with open(___TESTDESCRIPTIONCONFIG___,"r") as f:
			data = f.read()
			f.close
			data = json.loads(data)
		desc_conf = description_config.DescriptionConfig(data)
		self.assertEqual(desc_conf._attribute_keywords, ___ATTRIBUTEKEYWORDS___)
		desc_conf.set_attribute_keywords(["smth"])
		self.assertNotEqual(desc_conf._attribute_keywords, ___ATTRIBUTEKEYWORDS___)

	def test_description_config_set_method_keywords(self):
		with open(___TESTDESCRIPTIONCONFIG___,"r") as f:
			data = f.read()
			f.close
			data = json.loads(data)
		desc_conf = description_config.DescriptionConfig(data)
		self.assertEqual(desc_conf._method_keywords, ___METHODKEYWORDS___)
		desc_conf.set_method_keywords(["smth"])
		self.assertNotEqual(desc_conf._method_keywords, ___METHODKEYWORDS___)

	def test_description_config_set_initialization_keywords(self):
		with open(___TESTDESCRIPTIONCONFIG___,"r") as f:
			data = f.read()
			f.close
			data = json.loads(data)
		desc_conf = description_config.DescriptionConfig(data)
		self.assertEqual(desc_conf._initialization_keywords, ___INITIALIZATIONKEYWORDS___)
		desc_conf.set_initialization_keywords(["smth"])
		self.assertNotEqual(desc_conf._initialization_keywords, ___INITIALIZATIONKEYWORDS___)

	def test_description_config_get_attribute_keywords(self):
		with open(___TESTDESCRIPTIONCONFIG___,"r") as f:
			data = f.read()
			f.close
			data = json.loads(data)
		desc_conf = description_config.DescriptionConfig(data)
		self.assertEqual(desc_conf.get_attribute_keywords(), ___ATTRIBUTEKEYWORDS___)

	def test_description_config_get_method_keywords(self):
		with open(___TESTDESCRIPTIONCONFIG___,"r") as f:
			data = f.read()
			f.close
			data = json.loads(data)
		desc_conf = description_config.DescriptionConfig(data)
		self.assertEqual(desc_conf.get_method_keywords(), ___METHODKEYWORDS___)

	def test_description_config_get_initialization_keywords(self):
		with open(___TESTDESCRIPTIONCONFIG___,"r") as f:
			data = f.read()
			f.close
			data = json.loads(data)
		desc_conf = description_config.DescriptionConfig(data)
		self.assertEqual(desc_conf.get_initialization_keywords(), ___INITIALIZATIONKEYWORDS___)

if __name__ == '__main__':
	with open(___TESTDESCRIPTIONCONFIG___,"w") as f:
		conf = json.dumps({"Attribute keywords" : ___ATTRIBUTEKEYWORDS___, "Method keywords" : ___METHODKEYWORDS___, 
    						"Initialization keywords": ___INITIALIZATIONKEYWORDS___})
		f.write(conf)
		f.close()
	unittest.main()