# Bibliotecas necessárias
from client import *
import time

# Endereço do servidor central
CENTRAL_SERVER_IP = "200.235.131.66"
CENTRAL_SERVER_PORT = 10000

# Comandos válidos
known_commands = ["/list", "/chat", "/send", "/exit"]

print("Bem-vindo ao Whatsapp 2!")

username = input("Digite o seu nome de usuário: ")

# Inicializa o cliente
client = Client(username, CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT)

# Função para manter a conexão com o servidor central
def keepalive():
    while True:
        client.keepalive()
        time.sleep(5)

# Função para verificar se há novas mensagens
def check_requests():
    while True:
        client.check_requests()
        
# Inicia a thread para manter a conexão com o servidor central
keepalive_thread = threading.Thread(target=keepalive)
keepalive_thread.daemon = True
keepalive_thread.start()

# Inicia a thread para verificar novas mensagens
listener_thread = threading.Thread(target=check_requests)
listener_thread.daemon = True
listener_thread.start()

while True:
    command = input(
        "\n---------- Menu ----------\nListar usuários: /list\nEntrar em um bate-papo: /chat\nEnviar mensagem: /send\nSair: /exit\n\nEscolha uma ação: ")

    if command == "/list":
        client.get_list()
    elif command == "/chat":
        recipient = input(
            "\nCom qual usuário você deseja conversar: ")
        client.connect_to_peer(recipient)
    elif command == "/send":
        # client.send_message()
        pass
    elif command == "/exit":
        # fechar conexões, etc
        break
    else:
        print("\n--- commando inválido, tente novamente.")
