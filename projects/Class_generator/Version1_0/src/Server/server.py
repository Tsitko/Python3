___VERSION___ = 1.0

import sys

import select

import json

import socket

import config

from log import Log

from description_config import DescriptionConfig

from data_processor import DataProcessor

___DESCRIPTIONCONFIGPATH___ = "description_config.json"

___CONFIG___ = "config.json"

___MSGSIZE___ = 1048576

___CONNECTIONS___ = 5

class Server(object):
	def __init__(self, config_path = ___CONFIG___):
		conf = config.Config(___CONFIG___)
		self._IP = conf.get_IP()
		self._port = conf.get_port()
		self._sock = socket.socket()
		self._sock.bind((self._IP, self._port))
		self._clients = list()

	@Log()
	def _read(self, read_clients):
		responces = dict()
		for client in read_clients:
			try:
				data = client.recv(___MSGSIZE___).decode('utf-8')
				responces[client] = data
			except Exception as err:
				print(err)
				print('client %s %s disconnected.' % (client.fileno(), client.getpeername()))
				self._clients.remove(client)
		return responces

	def _write(self, responces, write_clients):

		for client in write_clients:
			if client in responces:
				try:
					responce = responces[client]
					if responce != '':
						data_processor = DataProcessor()

						p_data = data_processor.make_parsed_data(responce)
						msg = ''
						msg = data_processor.form_message(p_data)
						if msg != '':
							client.send(msg)
						else:
							err = "ERROR: wrong client config or class description format"
					else:
						client.close()
						self._clients.remove(client)
				except:
					print('client %s %s disconnected.' % (client.fileno(), client.getpeername()))
					client.close()
					self._clients.remove(client)


	def run(self):
		self._sock.listen(5)
		self._sock.settimeout(0.2)

		while True:
			try:
				client, addr = self._sock.accept()
			except KeyboardInterrupt:
				print('='*50, '\nServer disabled\n', '='*50)
				self._sock.close()
				sys.exit()
			except OSError as err:
				pass
			else:
				print('connected with %s' % str(addr))
				self._clients.append(client)
			finally:
				read_clients = list()
				write_clients = list()
				try:
					read_clients, write_clients, except_clients = select.select(self._clients, self._clients, [], 0)
				except:
					pass
				responces = self._read(read_clients)
				self._write(responces, write_clients)

if __name__ == "__main__":
	server = Server()
	server.run()