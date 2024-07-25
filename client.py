# Bibliotecas necessárias
import select
from socket import *
import threading
import sys


class Client:
    # Construtor
    def __init__(self, username, central_server_ip, central_server_port):
        self.username = username

        #Define credenciais do servidor e inicia conexao
        self.central_server_ip = central_server_ip
        self.central_server_port = central_server_port

        self.central_server_socket = socket(AF_INET, SOCK_STREAM)
        self.connect_to_central_server()

        #Define porta a ser usada para conexoes
        self.p2p_listening_socket = socket(AF_INET, SOCK_STREAM)
        self.p2p_listening_port = None
        self.p2p_listening()

        self.peers_list = {}
        self.thread_flags = {}

    # Conecta-se ao servidor central
    def connect_to_central_server(self):
        self.central_server_socket.connect((self.central_server_ip, self.central_server_port))

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

    # Verifica se há novas requisições de conexão
    def check_requests(self):
        chat_socket, _ = self.p2p_listening_socket.accept()  # Aceita uma conexão
        received = self.received_messages(chat_socket)
        user = (received.split(' ')[1]).replace("\r\n", "")

        self.peers_list[user] = chat_socket

        print(f"--------\n\nConectado a: {user}\n")

        sys.stdout.write("Escolha uma ação: ")
        sys.stdout.flush()

    # Lista os usuários conectados
    def print_list(self):
        self.central_server_socket.send("LIST\r\n".encode())

        list = self.received_messages(self.central_server_socket)

        list = list.replace("\r\n", "")
        _, users = (list.split(' '))

        users_list = users.split(':')

        print("\nUsuários disponíveis:")
        for i, user in enumerate(users_list, 1):
            print(f"{i}. {user}")

    # Obtém o endereço de um usuário
    def get_address(self, recipient):
        self.central_server_socket.send((f"ADDR {recipient}\r\n").encode())

        address = self.received_messages(self.central_server_socket)

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
            return False
        except Exception as e:
            print(f"Erro ao conectar-se a {recipient}: {e}")
            return False
        return True

    # Exibe a lista de peers ao qual tem-se conexão
    def print_peers_list(self):
        if self.peers_list == {}:
            print("\nVocê não está conectado com ninguém.\nInicie um bate-papo com /chat.")
            return False
        print("\nUsuários conectados:")
        for i, (user, _) in enumerate(self.peers_list.items(), 1):
            print(f"{i}. {user}")

        return True

    # Envia as mensagens entre os peers que estão no bate-papo
    def send_message_to_peer(self, recipient):
        try:
            socket = self.peers_list[recipient]
            self.thread_flags[recipient] = True
        except KeyError:
            print('Usuário inválido.')
            return
        
        print("Entrou no chat!\nPara disconectar digite /disc.")

        # Thread resposánvel pela exibição das mensagens recebidas
        comm_thread = threading.Thread(target=self.print_peer_messages, args=(socket, recipient))
        comm_thread.daemon = True
        comm_thread.start()

        while True:
            message = input()

            if not self.thread_flags[recipient]:
                break
            elif message == "/disc":
                socket.send("DISC\r\n".encode())
                break

            socket.send((message + " ").encode())

    # Exibe as mensagens trocadas entre os peers
    def print_peer_messages(self, socket, recipient):
        while True:
            message = self.received_messages(socket)

            if not self.thread_flags[recipient]:
                break
            elif message == "DISC\r\n":
                socket.close()
                self.peers_list.pop(recipient)
                self.thread_flags[recipient] = False
                print("Peer se desconectou. Envie qualquer mensagem para retornar ao menu.")
                break
            elif message == "":
                socket.close()
                self.peers_list.pop(recipient)
                self.thread_flags[recipient] = False
                break
            
            print(f"{recipient}: {message}")

    # Recebe mensagens
    def received_messages(self, socket):
        received_message = None

        try:
            received_message = socket.recv(1024)
        except TimeoutError:
            print("TimeoutError")
            return

        return received_message.decode()
    
    def close_connections(self):
        for sock in self.peers_list.values():
            sock.close()

