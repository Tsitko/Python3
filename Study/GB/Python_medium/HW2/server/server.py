import sys
import socket
import select
from log import Log


class Server(object):

    @Log()
    def __init__(self, host, port):
        self._host = host
        self._port = port

        self._sock = socket.socket()

        self._sock.bind((str(self._host), self._port))

        self._clients = list()
        
    @Log()
    @property
    def tcp_socket(self):
        return self._sock
    
    @Log()
    def _read(self, read_clients):

        responces = dict()

        for client in read_clients:

            try:

                data = client.recv(1024).decode('utf-8')
                responces[client] = data

            except Exception as err:

                print(err)

                print('client %s %s disconnected.' % (client.fileno(), client.getpeername()))

                self._clients.remove(client)

        return responces

    @Log()
    def _write(self, responces, write_clients, read_clients):

        for client in read_clients:

            if client in responces:

                try:

                    responce = responces[client].encode('utf-8')

                    for cl in write_clients:

                        cl.send(responce)

                except:

                    print('client %s %s disconnected.' % (client.fileno(), client.getpeername()))

                    self._clients.remove(client)

                    client.close()

                    self._clients.remove(client)

    @Log()
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

                self._write(responces, write_clients, read_clients)

if __name__ == '__main__':
    server = Server('localhost', 8001)
    server.run()
