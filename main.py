# José Roberto Martins Costa Júnior - 105480
# Thiago Zimerer Duarte - 108206

# Bibliotecas necessárias
from peer import *
import time

# Endereço do servidor central
CENTRAL_SERVER_IP = "200.235.131.66"
CENTRAL_SERVER_PORT = 10000

# Função para manter a conexão com o servidor central
def keepalive(peer):
    while True:
        peer.keepalive()
        time.sleep(5)

# Função para verificar se há solicitações de conexão
def check_requests(peer):
    while True:
        peer.check_requests()


if __name__ == "__main__":
    print("Bem-vindo ao Whatsapp 2!")

    username = input("Digite o seu nome de usuário: ")

    # Inicializa o peere
    peer = Peer(username, CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT)

    # Inicia a thread para manter a conexão com o servidor central
    keepalive_thread = threading.Thread(target=keepalive, args=(peer,))
    keepalive_thread.daemon = True
    keepalive_thread.start()

    # Inicia a thread para verificar novas mensagens
    listener_thread = threading.Thread(target=check_requests, args=(peer,))
    listener_thread.daemon = True
    listener_thread.start()

    # Menu principal
    while True:
        command = input(
            "\n---------- Menu ----------\nListar usuários: /list\nIniciar bate-papo: /chat\nEnviar mensagem: /send\nSair: /exit\n\nEscolha uma ação: ")

        if command == "/list":
            peer.print_list()
        elif command == "/chat":
            recipient = input("\nCom qual usuário você deseja conversar: ")

            if peer.connect_to_peer(recipient):
                print("Conectado com sucesso!\n")
        elif command == "/send":
            if peer.print_peers_list():
                recipient = input(
                    "\nPara quem você deseja enviar a mensagem: ")
                peer.send_message_to_peer(recipient)
        elif command == "/exit":
            peer.close_connections()
            break
        else:
            print("\n- Comando inválido, tente novamente.")
