from server import Server
from client import Client

INITIAL_PORT = 10001

comands_known = ["/list", "/send", "/help", "/exit"]

print("Bem-vindo ao chat!")

client = Client()
client.connect()
# client.keep()

username = input("Digite o seu nome de usuário: ")
port = client.create_port(username)

user_port = f"USER {username}:{port}\r\n"
client.send_user_port(user_port)

while True: 
    comand = input("\n---------- Menu ----------\nListar usuários: /list\nConectar-se: /addr\nEnviar mensagem: /send\nSair: /exit\n\nEscolha uma ação: ")
    
    if comand == "/list":
            client.list()
    elif comand == "/addr":
        recipient = input("\nDigite o nome do usuário que deseja se conectar: ")
        client.address(recipient)
    elif comand == "/send":
        client.send_message()
    elif comand == "/exit":
        break
    else:
        print("\n--- Comando inválido, tente novamente.")