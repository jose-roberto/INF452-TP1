# Bibliotecas necessárias
from client import *
import time

# Endereço do servidor central
CENTRAL_SERVER_IP = "200.235.131.66"
CENTRAL_SERVER_PORT = 10000

# Função para manter a conexão com o servidor central
def keepalive(client):
    while True:
        client.keepalive()
        time.sleep(5)

# Função para verificar se há novas mensagens
def check_requests(client):
    while True:
        client.check_requests()

if __name__ == "__main__":
    print("Bem-vindo ao Whatsapp 2!")

    username = input("Digite o seu nome de usuário: ")

    # Inicializa o cliente
    client = Client(username, CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT)
            
    # Inicia a thread para manter a conexão com o servidor central
    keepalive_thread = threading.Thread(target=keepalive, args=(client,))
    keepalive_thread.daemon = True
    keepalive_thread.start()

    # Inicia a thread para verificar novas mensagens
    listener_thread = threading.Thread(target=check_requests, args=(client,))
    listener_thread.daemon = True
    listener_thread.start()

    while True:
        command = input(
            "\n---------- Menu ----------\nListar usuários: /list\nIniciar bate-papo: /chat\nEnviar mensagem: /send\nSair: /exit\n\nEscolha uma ação: ")

        if command == "/list":
            client.print_list()
        elif command == "/chat":
            recipient = input("\nCom qual usuário você deseja conversar: ")
            if client.connect_to_peer(recipient):
                print("Conectado com sucesso!")
        elif command == "/send":
            client.print_peers_list()
            recipient = input("\nPara quem você deseja enviar a mensagem: ")
            print("Entrou no chat! Para disconectar digite /disconnect. Para sair do chat digite /exit.")
            client.send_message_to_peer(recipient)
        elif command == "/exit":
            # fechar conexões, etc
            break
        # else:
        #     print("\n--- commando inválido, tente novamente.")
