import Config
import json
import unittest

_TESTCONFPATH_ = "test_Config.json"

def Make_test_config():
	test_Config = open(_TESTCONFPATH_, "w")
	test_data = json.dumps({"NAs" : ["NA1", "NA2"],
							"NaNs" : ["NaN1", "NaN2"],
							"DateFormats" : ["Format1", "Format2"],
							"CsvSeparators" : ["Sep1", "Sep2"],
							"NumberSeparators" : ["NumSep1","NumSep2"]})
	test_Config.write(test_data)
	test_Config.close()

class test_Config(unittest.TestCase):

	def test_Config_NAs(self):
		Make_test_config()
		Conf = Config.Config(path = _TESTCONFPATH_)
		self.assertEqual(Conf.get_NAs()[0], "NA1")
		self.assertEqual(Conf.get_NAs()[1], "NA2")

	def test_Config_NaNs(self):
		Make_test_config()
		Conf = Config.Config(path = _TESTCONFPATH_)
		self.assertEqual(Conf.get_NaNs()[0], "NaN1")
		self.assertEqual(Conf.get_NaNs()[1], "NaN2")

	def test_Config_DateFormats(self):
		Make_test_config()
		Conf = Config.Config(path = _TESTCONFPATH_)
		self.assertEqual(Conf.get_DateFormats()[0], "Format1")
		self.assertEqual(Conf.get_DateFormats()[1], "Format2")

	def test_Config_CsvSeparators(self):
		Make_test_config()
		Conf = Config.Config(path = _TESTCONFPATH_)
		self.assertEqual(Conf.get_CsvSeparators()[0], "Sep1")
		self.assertEqual(Conf.get_CsvSeparators()[1], "Sep2")

	def test_Config_NumberSeparators(self):
		Make_test_config()
		Conf = Config.Config(path = _TESTCONFPATH_)
		self.assertEqual(Conf.get_NumberSeparators()[0], "NumSep1")
		self.assertEqual(Conf.get_NumberSeparators()[1], "NumSep2")

	


if __name__ == '__main__':
	unittest.main()
