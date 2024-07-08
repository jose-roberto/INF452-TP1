from client import Client

INITIAL_PORT = 10000
CLIENT_COUNT = 0

comands_known = ["/list", "/send", "/help", "/exit"]

while True:
    comand = input("----------- Menu -----------\nEntrar no bate-papo: 1\nSair: 2\n\nDigite um comando: ")

    if comand == "1":
        CLIENT_COUNT += 1
        
        print("\nEntrando no bate-papo")

        username = input("Digite o seu nome de usuário: ")
        port = INITIAL_PORT + CLIENT_COUNT

        client = Client(username, port)

    else:
        break