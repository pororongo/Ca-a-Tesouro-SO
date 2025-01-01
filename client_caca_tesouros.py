from socket import (socket, gethostbyname, gethostname,
                    AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR)

import threading
from queue import Queue

import interface


#Declaração da porta e do servidor
port = 65432
server = gethostbyname(gethostname())
addr = (server, port)

#[]
mapa = [['_']]


#Funções das threads de entrada
def receber(server_conn):
    pass

fila_teclado = Queue()
def ler_teclado(): #adaptado de https://stackoverflow.com/a/10079805
    import termios, select, sys, tty

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        while True:
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                fila_teclado.put(sys.stdin.read(1))
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

#[]
if __name__ == "__main__":
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)

    interface.clear()
    interface.menu(client_socket, addr)

    teclado = threading.Thread(target=ler_teclado, daemon=True)
    teclado.start() #! obs: tem que ser depois do menu
    
    response = client_socket.recv(1024)
    msg = eval(response)
    match msg:
        case ("mapa_novo", nome_mapa, mapa):
            interface.clear()
            interface.rend_mapa(mapa, nome_mapa)
        case (comando, *resto):
            assert print(comando, resto)

    while True:
        if not fila_teclado.empty():
            direcao = fila_teclado.get()
            if direcao in "wasd":
                msg = ("direcao", direcao)
                client_socket.send(repr(msg).encode()) 
                response = client_socket.recv(1024)
                match eval(response):
                    case ("mapa_novo", nome_mapa, mapa):
                        interface.clear()
                        interface.rend_mapa(mapa, nome_mapa)
                    case (comando, *resto):
                        assert print(comando, resto)

    client_socket.close()

