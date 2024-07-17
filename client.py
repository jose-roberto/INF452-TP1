# Bibliotecas necessárias
import select
from socket import *
import threading
import sys


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

        self.peers_list = {}

    # Conecta-se ao servidor central
    def connect_to_central_server(self):
        self.central_server_socket.connect((self.central_server_ip, self.central_server_port))
        # print("\nConectado ao servidor central!")

    # Mantém a conexão com o servidor central
    def keepalive(self):
        self.central_server_socket.send("KEEP\r\n".encode())

    # Define p2p_listening_socket como o responsável por ouvir novas conexões
    def p2p_listening(self):
        try:
            self.p2p_listening_socket.bind(('', 0))
            self.p2p_listening_socket.listen(1)

            # Define a porta de escuta
            _, self.p2p_listening_port = self.p2p_listening_socket.getsockname()
        except OSError:
            pass
  
        self.send_initial_message(self.central_server_socket, self.p2p_listening_port)

    # Envia mensagem inicial ao servidor central
    def send_initial_message(self, socket, port):
        initial_message = None

        if port == -1:
            initial_message = f"USER {self.username}\r\n"
        else:
            initial_message = f"USER {self.username}:{port}\r\n"

        socket.send(initial_message.encode())
    
    def start_chat(self, chat_socket):
        received = self.received_messages(chat_socket)
        user = (received.split(' ')[1]).replace("\r\n", "")

        self.peers_list[user] = chat_socket

        print(f"\nConectado a: {user}\n")

        while True:
            print(f"{user}: {self.received_messages(chat_socket)}")
            self.send_message_to_peer(user)

    # Verifica se há novas requisições de conexão
    def check_requests(self):
        ready_to_read,_,_=select.select([self.p2p_listening_socket,self.central_server_socket,sys.stdin],[],[])
        for sock in ready_to_read:
            if sock == self.p2p_listening_socket:
                chat_socket, _ = self.p2p_listening_socket.accept()  # Aceita uma conexão
                self.start_chat(chat_socket)

    # Lista os usuários conectados
    def get_list(self):
        self.central_server_socket.send("LIST\r\n".encode())

        list = self.received_messages(self.central_server_socket)
        
        list = list.replace("\r\n", "")
        _, users = (list.split(' '))

        users_list = users.split(':')

        print("\nUsuários conectados:")
        for i, user in enumerate(users_list, 1):
            print(f"{i}. {user}")

    # Obtém o endereço de um usuário
    def get_address(self, recipient):
        self.central_server_socket.send((f"ADDR {recipient}\r\n").encode())
        
        address= self.received_messages(self.central_server_socket)
        
        _, address = address.split(' ')
        ip, port = address.split(':')

        return ip, int(port)

    # Conecta-se a um usuário
    def connect_to_peer(self, recipient):
        try:
            ip, port = self.get_address(recipient)

            self.peers_list[recipient] = socket(AF_INET, SOCK_STREAM)

            self.peers_list[recipient].connect((ip, port))

            self.send_initial_message(self.peers_list[recipient], -1)

        except TimeoutError:
            print(
                f"Não foi possível conectar-se a {recipient} devido a um timeout.")
        except Exception as e:
            print(f"Erro ao conectar-se a {recipient}: {e}")

    # Envia mensagem à um usuário
    def send_message_to_peer(self, recipient):
        socket = self.peers_list[recipient]
        
        while True:
            message = input("Digite uma mensagem: ")

            if message == "/disconnect":
                socket.send("DISC\r\n".encode())
                socket.close()
                break
            elif message == "/exit":
                break 

            socket.send(message.encode())
            print(self.received_messages(socket))

    # Recebe mensagens do servidor central
    def received_messages(self, socket):
        received_message = None
        
        try:
            received_message = socket.recv(1024)
        except TimeoutError:
            print("TimeoutError")
            return

        return received_message.decode()
