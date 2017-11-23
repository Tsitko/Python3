import unittest

import os

import datetime

import server

import client

import config

import json

___TESTIP___ = "10.10.10.10"

___TESTPORT___ = "8001"

___TESTCONFIG___ = "test_cofig.json"


class ClientServerInitTest(unittest.TestCase):
    def test_config_init(self):
        conf = config.Config(___TESTCONFIG___)
        self.assertEqual(conf._IP,___TESTIP___)
        self.assertEqual(conf._port,___TESTPORT___)
    
    def test_config_get_IP(self):
        conf = config.Config(___TESTCONFIG___)
        self.assertEqual(conf.get_IP(),conf._IP)

    def test_config_get_port(self):
        conf = config.Config(___TESTCONFIG___)
        self.assertEqual(conf.get_port(),conf._port)

    def test_client_init(self):
        conf = config.Config(___TESTCONFIG___)
        test_client = client.Client(config_path=___TESTCONFIG___)
        self.assertEqual(test_client._IP, conf.get_IP())
        self.assertEqual(test_client._port, conf.get_port())
        self.assertEqual(test_client._name, None)



    def test_client_set_name(self):
        _test_Name = "Test"
        test_client=client.Client()
        test_client.set_name(_test_Name)
        self.assertEqual(test_client._name, _test_Name)

    def test_client_form_msg(self):
        _test_name = "Name"
        _test_msg="Msg"
        _test_msgToServer= json.dumps({"Name" : _test_name, "Msg" : _test_msg}).encode("utf-8")
        test_client = client.Client()
        test_client.set_name(_test_name)
        self.assertEqual(test_client.form_msg(_test_msg), _test_msgToServer)

    def test_client_send_msg(self):
        _test_name = "Name"
        _test_msg="Msg"
        test_client = client.Client()
        test_client.set_name(_test_name)
        test_client.send_msg(test_client.form_msg(_test_msg))
        msg=test_client.recv_msg()
        test_client.close_connection()
        self.assertRaises(ConnectionError)

    def test_client_recv_msg(self):
        _test_name = "Name"
        _test_msg="Msg"
        dt=datetime.datetime.now()
        dt_str=dt.strftime('%d-%B-%Y')
        _test_recieved_msg = json.dumps({"Intro" : "\nHi, " + _test_name + "!",
                                         "Date" : "Today is " + dt_str,
                                         "Conclusion" : "It's not the best day to " + _test_msg})
        test_client = client.Client()
        test_client.set_name(_test_name)
        test_client.send_msg(test_client.form_msg(_test_msg))
        _msg=test_client.recv_msg()
        self.assertEqual(_msg, _test_recieved_msg)

    def test_server_init(self):
        conf = config.Config(___TESTCONFIG___)
        serv = server.Server(config_path = ___TESTCONFIG___)
        self.assertEqual(serv._IP, conf.get_IP())
        self.assertEqual(serv._port, conf.get_port())

    def test_server_form_msg(self):
        _test_client_name = "John"
        _test_msg = "go to hell"
        _test_client_msg = json.dumps({"Name" : _test_client_name, "Msg" : _test_msg})
        test_server = server.Server()
        dt=datetime.datetime.now()
        dt_str=dt.strftime('%d-%B-%Y')
        _test_msg=json.dumps({"Intro" : "\nHi, " + _test_client_name + "!",
                              "Date" : "Today is " + dt_str,
                              "Conclusion" : "It's not the best day to " + _test_msg})
        self.assertEqual(_test_msg.encode('utf-8'), test_server.form_msg(_test_client_msg))
        
        

if __name__ == '__main__':
    with open(___TESTCONFIG___,"w") as f:
        conf = json.dumps({"IP" : ___TESTIP___, "port" : ___TESTPORT___})
        f.write(conf)
        f.close()

    unittest.main()
    os.remove(___TESTCONFIG___)