from server import Server
from client import Client

INITIAL_PORT = 10001
CLIENT_COUNT = 0

comands_known = ["/list", "/send", "/help", "/exit"]

server = Server()

while True:
    comand = input("----------- Menu -----------\nEntrar no bate-papo: 1\nSair: 2\n\nDigite um comando: ")

    if comand == "1":
        CLIENT_COUNT += 1
        
        print("\nEntrando no bate-papo")

        username = input("Digite o seu nome de usuário: ")
        port = INITIAL_PORT + CLIENT_COUNT

        client = Client(username, port)

        client.connect()

        comand = input("---------- Opcões ----------\nListar usuários: /list\nEnviar mensagem: /send\nAjuda: /help\nSair: /exit\n\nEscolha uma ação:")

    else:
        break