from ServerConfig import ServerConfig
from Message import Message
import json
import hashlib
from socketserver import BaseRequestHandler
from socketserver import TCPServer
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Numeric, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import func
import time

Base = declarative_base()


class ServerMessage(Base, Message):
	__tablename__ = 'Messages'
	id = Column(Integer, primary_key=True)
	sender = Column(String(50))
	reciever = Column(String(50))
	sender_name = Column(String(50))
	date = Column(String(50))
	body = Column(String(500))
	sent = Column(Integer)
	def __init__(self, msg, sent = 0):
		self.msg = json.loads(msg)
		self.sender = self.get_sender()
		self.reciever = self.get_reciever()
		self.sender_name = self.get_sender_name()
		self.body = self.get_body()
		self.date = self.get_date()
		self.sent = sent

	def form_message_from_table(self):
		return json.dumps({"type" : "message",
			"sender" : self.sender,
			"sender name" : self.sender_name,
			"reciever" : self.reciever,
			"date" : self.date,
			"body" : self.body
			})

class ContactList(Base):
	__tablename__ = "Contacts"
	id = Column(Integer, primary_key = True)
	client1_login = Column(String(50))
	client2_login = Column(String(50))
	def __init__(self, client1_login, client2_login):
		self.client1_login = client1_login
		self.client2_login = client2_login

class ServerClient(Base):
	__tablename__ = "Clients"
	id = Column(Integer, primary_key = True)
	name = Column(String(50))
	login = Column(String(50))
	password = Column(String(500))
	isActive = Column(Integer)
	isAuthorised = Column(Integer)
	def __init__(self, msg, isActive = 1, isAuthorised = 1):
		self.name = msg.get_sender_name()
		self.login = msg.get_sender()
		self.password = hashlib.md5(msg.get_body().encode('utf-8')).hexdigest()
		self.isActive = isActive
		self.isAuthorised = isAuthorised

	def get_login(self):
		return self.login



class BaseSocketHandler(BaseRequestHandler):
	def parse_message(self, data):
		return ServerMessage(data)

	def add_contact(self, client, msg):
		q = session.query(ContactList).filter_by(client1_login = client.get_login(), client2_login = msg.get_body())
		cnt = 0
		for cl in q:
			cnt+=1
		if cnt == 0:
			q = session.add(ContactList(client.get_login(), msg.get_body()))
			session.commit()

	def check_contacts(self, client1_login, client2_login):
		q = session.query(ContactList).filter_by(client1_login = client1_login, client2_login = client2_login)
		cnt = 0
		for cl in q:
			cnt+=1
		if cnt == 0:
			return False
		else:
			return True

	def check_registration(self, client):
		q = "id FROM messanger.clients where login = '%s'" % client.get_login()
		cnt = 0
		for cl in session.query(q):
			cnt+=1
		if cnt > 0:
			return True
		else:
			return False

	def check_authorization(self, client):
		q = "id FROM messanger.clients where login = '%s' and isAuthorised = 1" % client.get_login()
		cnt = 0
		for au in session.query(q):
			cnt+=1
		if cnt == 1:
			return True
		else:
			return False

	def authorise(self, client):
		cl = session.query(ServerClient).filter_by(login = client.get_login())
		password_ok = 0
		for c in cl:
			if c.password == client.password:
				password_ok = 1
		if password_ok == 1:
			cl.update({"isAuthorised" : 1})
			session.commit()
			return "authorised"
		else:
			return "wrong password"

	def register(self, client):
		if not self.check_registration(client):
			session.add(client)
			session.commit()

	def send_messages(self, client, msg):
		for ms in session.query(ServerMessage).filter_by(reciever = client.get_login(), sent = 0):
			if (self.check_contacts(ms.reciever, ms.sender)):
				self.request.send(ms.form_message_from_table().encode('utf-8'))
				time.sleep(0.02)
				session.query(ServerMessage).filter_by(id = ms.id).update({"sent" : 1})
		session.commit()
		self.request.send(self.form_error_message(msg, "no more messages").encode('utf-8')) 


	def form_error_message(self, message, text):
		return message.form_message("error message", "Server", "Server", message.get_sender(), text)

	def handle(self):
		data = self.request.recv(1024).decode('utf-8')
		msg = self.parse_message(data)
		client = ServerClient(msg)
		if msg.get_type() == "registration message":
			self.register(client)
			self.request.send(self.form_error_message(msg, "registration ok").encode('utf-8'))
		if msg.get_type() == "authorization message":
			if self.check_registration(client):
				text = self.authorise(client)
				self.request.send(self.form_error_message(msg, text).encode('utf-8'))
			else:
				self.request.send(self.form_error_message(msg, "client is not registered").encode('utf-8')) 
		if msg.get_type() == "message":
			if self.check_registration(client):
				if self.check_authorization(client):
					session.add(msg)
					session.commit()
					self.request.send(self.form_error_message(msg, "message accepted").encode('utf-8'))
				else:
					self.request.send(self.form_error_message(msg, "client is not authorised").encode('utf-8'))
			else:
				self.request.send(self.form_error_message(msg, "client is not registered").encode('utf-8'))
		if msg.get_type() == "ask message":
			if self.check_registration(client):
				if self.check_authorization(client):
					self.send_messages(client, msg)
				else:
					self.request.send(self.form_error_message(msg, "client is not authorised").encode('utf-8'))
			else:
				self.request.send(self.form_error_message(msg, "client is not registered").encode('utf-8'))
		if msg.get_type() == "add contact message":
			if self.check_registration(client):
				if self.check_authorization(client):
					self.add_contact(client, msg)
					self.request.send(self.form_error_message(msg, "friend added").encode('utf-8'))
				else:
					self.request.send(self.form_error_message(msg, "client is not authorised").encode('utf-8'))
			else:
				self.request.send(self.form_error_message(msg, "client is not registered").encode('utf-8'))
			

		

if __name__ == '__main__':
	conf = ServerConfig("ServerConfig.json")
	engine = create_engine('mysql://%s:%s@%s/%s' % (conf.get_DB_user(), conf.get_DB_user_password(), conf.get_DB_server(), conf.get_DB_name()))
	Session = sessionmaker(bind=engine)
	session = Session()
	Base.metadata.create_all(engine)
	server = TCPServer((conf.get_host(), conf.get_port()), BaseSocketHandler)
	try:

		print('server run on host %s and %s port' % (conf.get_host(), conf.get_port()))

		server.serve_forever()

	except KeyboardInterrupt as e:
		session.query(ServerClient).update({"isAuthorised" : 0})
		session.commit()

		print('server shutdown')

		server.shutdown()