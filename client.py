from socket import *
from random import randint
import threading
class Client:
    def __init__(self):
        self.serverIP = "200.235.131.66"
        self.serverPort = 10001
        self.clientSocket = socket(AF_INET, SOCK_STREAM)

    def connect(self):
        self.clientSocket.connect((self.serverIP, self.serverPort))
        # self.recv_from_server()

    def create_port(self):
        while True:
            try:
                ip = self.clientSocket.getsockname()
                port = randint(1025, 63535)
                self.clientSocket.bind((ip, port))
                break
            except OSError:
                pass

        return port

    def keep(self):
        self.clientSocket.send("KEEP\r\n".encode())
        threading.Timer(5.0, self.keep).start()

    def send_user_port(self, user_port):
        self.clientSocket.send(user_port.encode())
        # self.recv_from_server()

    def list(self):
        self.clientSocket.send("LIST\r\n".encode())
        self.recv_from_server()

    def address(self, recipient):
        self.clientSocket.send(f"ADDR {recipient}\r\n".encode())
        self.recv_from_server()

    def send_message(self, message):
        self.clientSocket.send(message.encode())
        # self.recv_from_server()

    def recv_from_server(self):
        self.clientSocket.settimeout(5)
        try:
            modifiedSentence = self.clientSocket.recv(1024)
            print("Server:", modifiedSentence.decode())
        except TimeoutError:
            print("TimeoutError")
            pass
        
