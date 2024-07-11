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

        self.p2p_listening_socket = socket(AF_INET, SOCK_STREAM)
        self.p2p_listening_port = None

        self.p2p_listening()

        self.p2p_to_connect = socket(AF_INET, SOCK_STREAM)

    # Conecta-se ao servidor central
    def connect_to_central_server(self):
        self.central_server_socket.connect(
            (self.central_server_ip, self.central_server_port))
        print("\nConectado ao servidor central!")
        
    # Mantém a conexão com o servidor central
    def keepalive(self):
        self.central_server_socket.send("KEEP\r\n".encode())

    # Define p2p_listening_socket como o responsável por ouvir novas conexões
    def p2p_listening(self):
        try:
            self.p2p_listening_socket.bind(('', 0))
            self.p2p_listening_socket.listen(1)
            
            _, self.p2p_listening_port = self.p2p_listening_socket.getsockname() # Define a porta de escuta
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
        ready_to_read, _, _ = select.select([self.p2p_listening_socket], [], [], 0.1) # Garante que a função não bloqueie o programa

        if ready_to_read:
            connectionSocket, addr = self.p2p_listening_socket.accept() # Aceita uma conexão

            # Exibe informações sobre a conexão
            with connectionSocket:
                print("Connectado a: ", addr)
                message = connectionSocket.recv(1024)
                print("Messagem recebida:", message.decode())
                connectionSocket.send("Mensagem recebida!\r\n".encode())
                
    # Lista os usuários conectados
    def get_list(self):
        self.central_server_socket.send("LIST\r\n".encode())
        
        list = self.received_messages()
        list = list.replace("\r\n", "")
        _, users = (list.split(' '))
        
        users_list = users.split(':')
        
        print("\nUsuários conectados:")
        for i, user in enumerate(users_list, 1):
            print(f"{i}. {user}")
        
    # Obtém o endereço de um usuário
    def get_address(self, recipient):
        self.central_server_socket.send((f"ADDR {recipient}\r\n").encode())
        address = self.received_messages()

        _, address = address.split(' ')
        ip, port = address.split(':')

        return ip, int(port)
    
    # Conecta-se a um usuário
    def connect_to_peer(self, recipient):
        try:
            ip, port = self.get_address(recipient)
            
            self.p2p_to_connect.connect((ip, port))
            
            self.send_message_to_peer(port)
            
            received_from_peer = self.received_messages()
            print("Received from peer:", received_from_peer)
        except TimeoutError:
            print(f"Não foi possível conectar-se a {recipient} devido a um timeout.")
        except Exception as e:
            print(f"Erro ao conectar-se a {recipient}: {e}")
        
    # Envia mensagem à um usuário
    def send_message_to_peer(self, port):
        message = f"USER {self.username}:{port}\r\n"
        self.p2p_to_connect.send(message.encode())
                 
    # Recebe mensagens do servidor central
    def received_messages(self):
        self.central_server_socket.settimeout(5) # Define um timeout de 5 segundos

        try:
            received_message = self.central_server_socket.recv(1024)
            # print("\nServer:", received_message.decode())
        except TimeoutError:
            print("TimeoutError")
            pass
        
        return received_message.decode()