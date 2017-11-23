from subprocess import Popen, CREATE_NEW_CONSOLE, PIPE

from unittest import mock, TestCase, main

import os

import config

from log import Log

import json

import appLogConfig

import client

import server

from time import sleep


___TESTIP___ = "10.10.10.10"

___TESTPORT___ = "8001"

___TESTCONFIG___ = "test_cofig.json"

___CONFIGPATH___ = "config.json"

___LIFETIME___ = 2

@Log()
def test_func(a, b):
    return a + b

class ConfigTestCases(TestCase):
    def test_config_init(self):
        conf = config.Config(___TESTCONFIG___)
        self.assertEqual(conf._IP,str(___TESTIP___))
        self.assertEqual(conf._port,int(___TESTPORT___))
    
    def test_config_get_IP(self):
        conf = config.Config(___TESTCONFIG___)
        self.assertEqual(conf.get_IP(),conf._IP)

    def test_config_get_port(self):
        conf = config.Config(___TESTCONFIG___)
        self.assertEqual(conf.get_port(),conf._port)

class LogTestCases(TestCase):
    def test_log_init(self):
        log = Log()
        self.assertEqual(log._log, appLogConfig.app_log)

    def test_log_logging(self):
        size1 = os.stat(appLogConfig.fname).st_size
        test_func(1, 2)
        size2 = os.stat(appLogConfig.fname).st_size
        self.assertNotEqual(size1, size2)

class ClientTestCases(TestCase):
    def test_client_init(self):
        conf = config.Config(___TESTCONFIG___)
        test_client = client.Client(config_path=___TESTCONFIG___)
        self.assertEqual(test_client._host, conf.get_IP())
        self.assertEqual(test_client._port, conf.get_port())
        

    def test_client_run_w(self):
        p_list = []
        p_list.append(Popen('python server.py',
                            creationflags=CREATE_NEW_CONSOLE))
        p_list.append(Popen('python client.py w',
                            creationflags=CREATE_NEW_CONSOLE))

        sleep(___LIFETIME___)
        poll = p_list[1].poll()
        
        for p in p_list:
            p.kill()
        p_list.clear()
        self.assertEqual(poll, None)
        
        
    def test_client_run_r(self):
        p_list = []
        p_list.append(Popen('python server.py',
                            creationflags=CREATE_NEW_CONSOLE))
        p_list.append(Popen('python client.py r',
                            creationflags=CREATE_NEW_CONSOLE))

        sleep(___LIFETIME___)
        poll = p_list[1].poll()
        
        for p in p_list:
            p.kill()
        p_list.clear()
        self.assertEqual(poll, None)

class ServerTestCases(TestCase):
    def test_server_init(self):
        conf = config.Config(___CONFIGPATH___)
        test_server = server.Server(___CONFIGPATH___)
        self.assertEqual(test_server._host, conf.get_IP())
        self.assertEqual(test_server._port, conf.get_port())

    def test_server_run(self):
        p = Popen('python server.py',
                            creationflags=CREATE_NEW_CONSOLE)
        sleep(___LIFETIME___)
        poll = p.poll()
        p.kill()
        self.assertEqual(poll, None)

    
 

if __name__ == '__main__':
    with open(___TESTCONFIG___,"w") as f:
        conf = json.dumps({"IP" : ___TESTIP___, "port" : ___TESTPORT___})
        f.write(conf)
        f.close()
    

    main()
    os.remove(___TESTCONFIG___)
