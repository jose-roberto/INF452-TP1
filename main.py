# Bibliotecas necessárias
from client import Client
import threading

# Endereço do servidor central
CENTRAL_SERVER_IP = "200.235.131.66"
CENTRAL_SERVER_PORT = 10001

# Comandos válidos
known_commands = ["/list", "/send", "/help", "/exit"]

print("Bem-vindo ao chat!")

username = input("Digite o seu nome de usuário: ")

# Inicializa o cliente
client = Client(username, CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT)

# Função para verificar se há novas mensagens
def check_requests():
    while True:
        client.check_requests()

# Inicia a thread para verificar novas mensagens
listener_thread = threading.Thread(target=check_requests)
listener_thread.daemon = True
listener_thread.start()

while True:
    command = input(
        "\n---------- Menu ----------\nListar usuários: /list\nConectar-se: /addr\nEnviar mensagem: /send\nSair: /exit\n\nEscolha uma ação: ")

    if command == "/list":
        client.get_list()
    elif command == "/addr":
        recipient = input(
            "\nDigite o nome do usuário ao qual deseja-se conectar: ")
        # client.get_address(recipient)
    elif command == "/send":
        # client.send_message()
        pass
    elif command == "/exit":
        # fechar conexões, etc
        break
    else:
        print("\n--- commando inválido, tente novamente.")
