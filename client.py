from socket import *

class Client:
    def __init__(self, username, port):
        self.serverName = username
        serverPort = port
        clientSocket = socket(AF_INET, SOCK_STREAM)