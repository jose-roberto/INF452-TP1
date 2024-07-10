from client import Client
import threading

INITIAL_PORT = 10001

comands_known = ["/list", "/send", "/help", "/exit"]

print("Bem-vindo ao chat!")

client = Client()
client.connect_to_central_server()
# client.keep()

username = input("Digite o seu nome de usuário: ")
port = client.create_port(username)

client.send_user_port(username, port)

def check_requests():
    while True:
        client.check_requests()

listener_thread = threading.Thread(target=check_requests)
listener_thread.daemon = True
listener_thread.start()

while True: 
    comand = input("\n---------- Menu ----------\nListar usuários: /list\nConectar-se: /addr\nEnviar mensagem: /send\nSair: /exit\n\nEscolha uma ação: ")
    
    if comand == "/list":
            client.get_list()
    elif comand == "/addr":
        recipient = input("\nDigite o nome do usuário ao qual deseja-se conectar: ")
        client.get_address(recipient)
    elif comand == "/send":
        client.send_message()
    elif comand == "/exit":
        # fechar conexões, etc
        break
    else:
        print("\n--- Comando inválido, tente novamente.")