***Simple client-server application on python 3***

**Overwiev**

This application will let up to 5 users send messages to server and got ansvers from it.

**Files**

*Config.json* - config file with connection information (IP and port)

*config.py* - config class description

*client.py* - client class descripton and operations on that class

*server.py* - server class descripton and operations on that class

*unit_tests.py* - unit tests for all given classes and it's interaction (you should ran server before unit tests)

**How to demo**

1. Start server
2. Start unit_tests.py and see OK
3. Start 2 clients in differet terminals
4. First is John and he wants server to go to hell
5. Second is Ivan and ge wants server to make revolution
6. First will get answer "Hi, John! Today is [todays date]. It's not the best day to go to hell"
7. Second will get answer "Hi, Ivan! Today is [todays date]. It's not the best day to start revolution"
