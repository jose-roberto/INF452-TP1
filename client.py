# Bibliotecas necessárias
from socket import *
import select

class Client:
    # Construtor
    def __init__(self, username, central_server_ip, central_server_port):
        self.username = username

        self.central_server_ip = central_server_ip
        self.central_server_port = central_server_port

        self.central_server_socket = socket(AF_INET, SOCK_STREAM)
        self.connect_to_central_server()

        self.p2p_socket = socket(AF_INET, SOCK_STREAM)
        self.p2p_listening_port = None

        self.p2p_listening()

        # Inutilizado até o momento:
        # self.client_port = None
        # self.p2p_to_connect = socket(AF_INET, SOCK_STREAM)

    # Conecta-se ao servidor central
    def connect_to_central_server(self):
        self.central_server_socket.connect(
            (self.central_server_ip, self.central_server_port))
        print("\nConectado ao servidor central!")

    # Mantém a conexão com o servidor central
    def keepalive(self):
        self.central_server_socket.send("KEEP\r\n".encode())

    # Define p2p_socket como o responsável por ouvir novas conexões
    def p2p_listening(self):
        try:
            self.p2p_socket.bind(('', 0))
            self.p2p_socket.listen(1)
            
            _, self.p2p_listening_port = self.p2p_socket.getsockname() # Define a porta de escuta
        except OSError:
            pass

        print("p2p_listening_port: ", self.p2p_listening_port)
        
        self.send_initial_message()
    
    # Envia mensagem inicial ao servidor central
    def send_initial_message(self):
        initial_message = f"USER {self.username}:{self.p2p_listening_port}\r\n" # Envia a porta de escuta por onde outros clientes poderão se conectar
        self.central_server_socket.send(initial_message.encode())

    # Verifica se há novas requisições de conexão
    def check_requests(self):
        ready_to_read, _, _ = select.select([self.p2p_socket], [], [], 0.1) # Garante que a função não bloqueie o programa

        if ready_to_read:
            connectionSocket, addr = self.p2p_socket.accept() # Aceita uma conexão

            # Exibe informações sobre a conexão
            with connectionSocket:
                print("Connectado a: ", addr)
                message = connectionSocket.recv(1024)
                print("Messagem recebida:", message.decode())

    # Lista os usuários conectados
    def get_list(self):
        self.central_server_socket.send("LIST\r\n".encode())
        self.recv_from_server()
    
    # Recebe mensagens do servidor central
    def recv_from_server(self):
        self.central_server_socket.settimeout(5) # Define um timeout de 5 segundos

        try:
            received = self.central_server_socket.recv(1024)
            print("\nServer:", received.decode())
        except TimeoutError:
            print("TimeoutError")
            pass

    # Inutilizado até o momento:
    # def connect_to_p2p(self, ip, port):
    #     self.p2p_server.connect((ip, port))
    #     self.send_message(f"USER {self.username}:{port}\r\n")
    #     self.recv_from_server()

    # def get_address(self, recipient):
    #     self.client_socket.send(f"ADDR {recipient}\r\n".encode())
    #     addr_message = self.recv_from_server()

    #     _, result = (addr_message.decode()).split(' ')
    #     ip, port = result.split(':')

    #     self.connect_to_p2p(ip, int(port))

    # def send_message(self, message):
    #     self.p2p_server.send(message.encode())
    
    # def get_client_port(self):
    #     _, self.client_port = self.central_server_socket.getsockname()
    #     print("client_socket port:", self.client_port)

    #     return self.client_port
