from socket import *

class Client:
    def __init__(self, username, port):
        self.serverName = username
        self.serverPort = port
        self.clientSocket = socket(AF_INET, SOCK_STREAM)

    def connect(self):
        self.clientSocket.connect((self.serverName, self.serverPort))