from socket import *

class Server:
    def __init__(self):
        self.users = {}
        self.serverSocket = socket(AF_INET,SOCK_STREAM)
        self.serverSocket.bind(('',10000))
        self.serverSocket.listen(1)
        print("O servidor está ativo!")

    def get_command(self, instruction, c_socket):
        instruction = instruction.split(' ')

        if instruction[0] == 'USER':
            user, port = instruction[1].split(':')
            self.users[c_socket] = {
                'User': user,
                'Port':port,
                'Keepalive': 0,
                'Socket':c_socket
            }
        elif instruction[0] == 'LIST':
            print("Ativos(alem de voce):\n")
            for user, info in self.users.items():
                print(f"{info['User']}\n")
        elif instruction[0] == 'KEEP':
            print('ooiiiii')

    def running(self):
        while True:
            connectionSocket, addr = self.serverSocket.accept()
            sentence = connectionSocket.recv(1024)
            self.get_command(sentence, connectionSocket)
