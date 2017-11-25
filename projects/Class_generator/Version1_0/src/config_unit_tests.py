import unittest

import os

import json

import config

___TESTCONFIG___ = "test_config.json"

___TESTIP___ = "10.10.10.10"

___TESTPORT___ = 8001

class ConfigTest(unittest.TestCase):
	def test_config_init(self):
		conf = config.Config(___TESTCONFIG___)
		self.assertEqual(conf._IP, ___TESTIP___)
		self.assertEqual(conf._port, ___TESTPORT___)

	def test_config_set_IP(self):
		_test_IP = "11.11.11.11"
		conf = config.Config(___TESTCONFIG___)
		self.assertNotEqual(conf._IP, _test_IP)
		conf.set_IP(_test_IP)
		self.assertEqual(conf._IP, _test_IP)

	def test_config_set_port(self):
		_test_port = 8010
		conf = config.Config(___TESTCONFIG___)
		self.assertNotEqual(conf._port,_test_port)
		conf.set_port(_test_port)
		self.assertEqual(conf._port, _test_port)

	def test_config_get_IP(self):
		conf = config.Config(___TESTCONFIG___)
		self.assertEqual(conf._IP, ___TESTIP___)

	def test_config_get_port(self):
		conf = config.Config(___TESTCONFIG___)
		self.assertEqual(conf._port, ___TESTPORT___)

	def test_config_save_config(self):
		conf_path="conf.json"
		with open(___TESTCONFIG___,"w") as f:
			conf = json.dumps({"IP" : ___TESTIP___, "port" : ___TESTPORT___})
			f.write(conf)
			f.close()
		conf = config.Config(___TESTCONFIG___)
		conf.save_config(conf_path)
		with open(conf_path,"r") as f:
			data = f.read()
			f.close
			configData = json.loads(data)
		self.assertEqual(int(configData["port"]), ___TESTPORT___)
		self.assertEqual(configData["IP"], ___TESTIP___)
		os.remove(conf_path)





if __name__ == '__main__':
    with open(___TESTCONFIG___,"w") as f:
        conf = json.dumps({"IP" : ___TESTIP___, "port" : ___TESTPORT___})
        f.write(conf)
        f.close()
    unittest.main()
    os.remove(___TESTCONFIG___)