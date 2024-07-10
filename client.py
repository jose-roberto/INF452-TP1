from socket import *
import threading
import select

class Client:
    def __init__(self):
        self.server_ip = "200.235.131.66"
        self.server_port = 10001

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.p2p_socket = socket(AF_INET, SOCK_STREAM)
    
        self.username = ''

    def create_port(self, username):
        self.username = username
        try:
            _, port = self.client_socket.getsockname()
            self.client_socket.bind(self.client_socket.getsockname())
            self.client_socket.listen(1)
        except OSError:
            pass

        return port

    def connect_to_central_server(self):
        self.client_socket.connect((self.server_ip, self.server_port))

    def connect_to_p2p(self, ip, port):
        self.p2p_socket.connect((ip, port))
        self.send_message(f"USER {self.username}:{port}\r\n") 
        self.recv_from_server()
    
    def check_requests(self):
        ready_to_read, _, _ = select.select([self.client_socket], [], [], 0.1)
        if ready_to_read:
            connectionSocket, addr = self.client_socket.accept()

    def send_user_port(self, username, port):
        user_port = f"USER {username}:{port}\r\n"
        self.client_socket.send(user_port.encode())

    def keep(self):
        self.client_socket.send("KEEP\r\n".encode())
        threading.Timer(5.0, self.keep).start()

    def get_list(self):
        self.client_socket.send("LIST\r\n".encode())
        self.recv_from_server()

    def get_address(self, recipient):
        self.client_socket.send(f"ADDR {recipient}\r\n".encode())
        addr_message = self.recv_from_server()

        _, result = (addr_message.decode()).split(' ')
        ip, port = result.split(':')

        self.connect_to_p2p(ip, int(port))       

    def send_message(self, message):
        self.p2p_socket.send(message.encode())

    def recv_from_server(self):
        self.client_socket.settimeout(5)
        try:
            received = self.client_socket.recv(1024)
            print("Server:", received.decode())
        except TimeoutError:
            print("TimeoutError")
            pass

        return received
        
