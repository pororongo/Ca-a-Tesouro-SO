from socket import (socket, gethostbyname, gethostname,
                    AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR)

import interface


#Declaração da porta e do servidor
port = 65432
server = gethostbyname(gethostname())
addr = (server, port)

#[]
mapa = [['_']]


#Funções das threads
def receber(server_conn):
    pass

def ler_teclado():
    pass


#[]
if __name__ == "__main__":
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    interface.menu(client_socket, addr)
    
    response = client_socket.recv(1024)
    msg = eval(response)
    match msg:
        case ("mapa_novo", nome_mapa, mapa):
            print("mapa_novo1")
            interface.clear()
            interface.rend_mapa(mapa, nome_mapa)
        case (comando, *resto):
            assert print(comando, resto)

    while True:
        direcao = input("wasd para se mover ")
        if direcao in "wasd":
            msg = ("direcao", direcao)
            client_socket.send(repr(msg).encode()) 
            response = client_socket.recv(1024)
            print(f"{response=}")
            match eval(response):
                case ("mapa_novo", nome_mapa, mapa):
                    interface.clear()
                    interface.rend_mapa(mapa, nome_mapa)
                case (comando, *resto):
                    assert print(comando, resto)

    client_socket.close()

