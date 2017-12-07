***Functional requirments for messanger application***

**Client**

* Client have name, login, password, host and port
* Client can set and get name, login, password, host and port
* Client can form message (takes message text and Clients attributes, returns object of class Message with type message)
* Client can form registration message (takes Clients attributes, returns object of class Message with type registration message)
* Client can form authorization message (takes Clients attributes, returns object of class Message with type authorization message)
* Client can form request message (takes Clients attributes, returns object of class Message with type request message)
* Client can send message (takes objeck of type message and Clients attributes, returns result of sending (object of type Message))
* Client can check message (takes object of type message, returns message type)
* Client can parse message (takes string, returns object of type Message)
* Client can handle errors (takes object of type Message with type error message, returns error text)
* Client can register on server (takes Clients attributes, forms registration message, sends it to server, returns registration result)
* Client can authorise on server (takes Clients attributes, forms authorization message, sends it to server, returns authorization result)
* Client is initialyzing by crating object of class config and getting name, login, password, host and port from it


**Message**

* Message have sender, sender name, reciever, body, date, isSent and type
* Message can set and get sender, sender name, reciever, body, date, isSent and type 
* Message is initialysing from json object. It sets sender, sender name, reciever, body, date and type from that object 

**Config**

* Config have host and port
* Config can get and set host and port
* Config is initializing from json file. It sets host and port from that file

**Client config (child of Config)**

* Client config have host, port, name, login and password
* Client config can get and set host, port, name, login and password
* Config is initializing from json file. It sets host, port, name, login and password from that file

**Server client**

* Server client have name, login, password, isActive
* Server client can set and get name, login, password, isActive
* Server client is initializing by setting name, login, password, isActive

**Server(TCPServer, BaseRequestHandler)**

* Server can set and get host and port
* Server can handle request (get user info from message, send answer or error or a set of messages to client)
* Server can check message (taking object of type Message, returns 1 if message is ok, 0 if not ok)
* Server can get client  (taking object of type Message with type message, returns object of type Server Client)
* Server can check active (taking object of type Server client, returns 1 or 0 for active/ not active)
* Server can activate client (taking object of type Server client, setting clients isActive as 1 and updating it in DB)
* Server can deactivate client (taking object of type Server client, setting clients isActive as 0 and updating it in DB)
* Server can check registration (taking object of type Server client, trying to find it in DB and returns 1 if found, 0 if not)
* Server can ask registration (taking object of type Server client, returns object of type Message with type error message and text "Client is not registered")
* Server can form message (taking object of type Server client, message type and text, returns object of type Message with given type and given text, sender =  Server, reciever = Server clients login, date = current date)
* Server can form error message (taking object of type Server client and error text, returns object of type Message with type error message and given text, sender =  Server, reciever = Server clients login, date = current date)
* Server can send messages (taking object of type Server client, finding not sended messages for that client, sending all those messages to client and setting its isSent to 1 or sending message with type no messages and empty text to client)

