############################################################################
# Basic Server that supports treads
############################################################################
import socket
import threading
import sqlite3

game = True

class Player(object):

    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name
        self.money_counter = 0
        self.jail_card = False

    def setting(self):
        self.ip = '127.0.0.1'
        self.port = 1730
        self.name = 'hello'
        self.color = 'white'
        self.money_counter = 50

class Server(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.count = 0
        self.connection_lst = []
        self.current_turn = self.count
    def start(self):
        try:
           print('server starts up on ip %s port %s' % (self.ip, self.port))
           # Create a TCP/IP socket
           sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           sock.bind((self.ip, self.port))
           sock.listen(3)


           while True:
                print('waiting for a new client')
                clientSocket, client_address = sock.accept() # block
                self.connection_lst.append(clientSocket)
                print('new client entered')
                self.count += 1
                msg = clientSocket.recv(1024).decode()
                print(msg)
                print("clients count: ",self.count)
                # implement here your main logic
                self.handleClient(clientSocket, self.count)


        except socket.error as e:
            print(e)


    def sendallclients(self, msg):
        for client in self.connection_lst:
            msg = msg + ","
            client.send(str(msg).encode())


    def handleClient(self, clientSock, current):
        client_handler = threading.Thread(target=self.handle_client_connection, args=(clientSock, current,))
        # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
        client_handler.start()

    def turn(self, msg):
        if self.current_turn == self.count:
            self.current_turn = 0
        client = self.connection_lst[self.current_turn]
        output = msg + "| its your turn"
        client.send(output.encode())
        self.current_turn += 1

    #def get_players_info(self, msg):


    def sign_players(self, msg):
        count = 0
        name = ''
        password = ''
        while msg[count] != 'N':
            name = name + msg[count]
            count += 1
        count = len(msg) - 1
        while msg[count] != 'P':
            password = password + msg[count]
            count -= 1
        u = Users()
        u.insert_user(name, password)
        u.select_user_by_id(1)

    def handle_client_connection(self, client_socket, current):
        print("start\n")
        numbers = '0123456789'
        while True:
            msg = client_socket.recv(1024).decode()
            print(msg)
            if msg == "im leaving":
                print("a client is leaving")
                self.connection_lst.remove(client_socket)
                self.count -= 1
                client_socket.close()
                break
            #gets name and password
            if "NP" in msg:
                self.sign_players(msg)
            if msg == "start":
                output = "player count: " + str(self.count)
                self.sendallclients(output)
            if "|" in msg:
                self.sendallclients(msg)
                #self.turn(msg)
            #try:
            #    number = int("s")
            #except:
            #    print("hello")
            #        self.sendallclients(msg)
            else:
                output = 'Unknown Command, Please Type Again'
            #client_socket.sendall(output.encode())

class Users:
    """Creates database with users table includes:
       create query
       insert query
       select query
    """

    def __init__(self, tablename="users", userId="userId", password="password", username="username"):
        self.__tablename = tablename
        self.__userId = userId
        self.__password = password
        self.__username = username
        conn = sqlite3.connect('test.db')
        print("Opened database successfully")
        query_str = "CREATE TABLE IF NOT EXISTS " + tablename + "(" + self.__userId + " " + \
                    " INTEGER PRIMARY KEY AUTOINCREMENT ,"
        query_str += " " + self.__password + " TEXT    NOT NULL ,"
        query_str += " " + self.__username + " TEXT    NOT NULL );"

        # conn.execute("drop table users")
        conn.execute(query_str)
        print("Table created successfully")
        conn.commit()
        conn.close()

    def __str__(self):
        return "table  name is ", self.__tablename

    def get_table_name(self):
        return self.__tablename

    def insert_user(self, username, password):
        conn = sqlite3.connect('test.db')
        insert_query = "INSERT INTO " + self.__tablename + " (" + self.__username + "," + self.__password + ") VALUES " \
                                                                                                            "(" + "'" + username + "'" + "," + "'" + password + "'" + ");"
        print(insert_query)
        conn.execute(insert_query)
        conn.commit()
        conn.close()
        print("Record created successfully")

    def select_user_by_id(self, userId):
        conn = sqlite3.connect('test.db')
        print("Opened database successfully")
        str1 = "select * from users;"

        """strsql = "SELECT userId, username, password  from " +  self.__tablename + " where " + self.__userId + "=" \
            + str(userId)
        """
        print(str1)
        cursor = conn.execute(str1)
        for row in cursor:
            print("userId = ", row[0])
            print("username = ", row[1])
            print("password = ", row[2])

        print("Operation done successfully")
        conn.close()


if __name__ == '__main__':
   ip = '127.0.0.1'
   port = 1730
   s = Server(ip, port)
   s.start()
