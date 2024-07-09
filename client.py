from socket import *
from random import randint
import threading
class Client:
    def __init__(self):
        self.server_ip = "200.235.131.66"
        self.server_port = 10001
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.communication_socket = socket(AF_INET, SOCK_STREAM)
        self.username = ''

    def connect(self):
        self.client_socket.connect((self.server_ip, self.server_port))
        # self.recv_from_server()

    def create_port(self, user):
        self.username = user
        try:
            ip, port = self.client_socket.getsockname()
            self.client_socket.bind(self.client_socket.getsockname())
        except OSError:
            pass

        return port

    def keep(self):
        self.client_socket.send("KEEP\r\n".encode())
        threading.Timer(5.0, self.keep).start()

    def send_user_port(self, user_port):
        self.client_socket.send(user_port.encode())
        # self.recv_from_server()

    def list(self):
        self.client_socket.send("LIST\r\n".encode())
        self.recv_from_server()

    def address(self, recipient):
        self.client_socket.send(f"ADDR {recipient}\r\n".encode())
        addr_message = self.recv_from_server()
        ip, port = addr_message.split(':')
        self.communication_socket.connect((ip, port))
        self.send_message(f"USER {self.username}:{port}\r\n")        

    def send_message(self, message):
        self.communication_socket.send(message.encode())
        # self.recv_from_server()

    def recv_from_server(self):
        self.client_socket.settimeout(5)
        try:
            received = self.client_socket.recv(1024)
            print("Server:", received.decode())
        except TimeoutError:
            print("TimeoutError")
            pass

        return received
        
