from socket import (socket, gethostbyname, gethostname,
                    AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR)

import threading
import queue
import atexit
import time

from serializador import send_object, recv_object
import interface


#Declaração da porta e do servidor
port = 65432
server = gethostbyname(gethostname())
addr = (server, port)

#Variáveis recebidas do servidor
nome_mapa = ''
mapa = [['_']]
pontos = 0

#[]
def delta_t(intervalo: float):
    t0 = 0

    def dt():
        nonlocal t0

        if time.time() - t0 > intervalo:
            t0 = time.time()
            return True
        else:
            return False

    return dt

#Funções das threads de entrada
def receber(server_conn):
    global pontos, mapa, nome_mapa

    buff = []
    while True:
        msg = recv_object(server_conn, buff)
        match msg:
            case ("mapa_novo", nome_novo, mapa_novo):
                nome_mapa = nome_novo
                mapa      = mapa_novo
            case ("qtd_pontos", pts):
                pontos = pts
            case _:
                assert print(msg)

fila_teclado = queue.Queue()
def ler_teclado(): #adaptado de https://stackoverflow.com/a/10079805
    import termios, select, sys, tty

    old_settings = termios.tcgetattr(sys.stdin)

    @atexit.register
    def resetar_terminal():
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    try:
        tty.setcbreak(sys.stdin.fileno())
        while True:
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                fila_teclado.put(sys.stdin.read(1))
    finally:
        resetar_terminal()

#Programa principal
if __name__ == "__main__":
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)

    try:
        interface.clear()
        interface.menu(client_socket, addr)

        teclado = threading.Thread(target=ler_teclado, daemon=True)
        teclado.start() #! obs: tem que ser depois do menu

        recebedor = threading.Thread(target=receber, args=[client_socket], daemon=True)
        recebedor.start()

        atualizar_estado = delta_t(.60)
        atualizar_tela   = delta_t(.02)

        while True:
            if atualizar_estado():
                msg = ("atualizacao",)
                send_object(client_socket, msg)

            if atualizar_tela():
                interface.clear()
                interface.rend_tela(mapa, nome_mapa, pontos)

            if not fila_teclado.empty():
                direcao = fila_teclado.get()
                if direcao in "wasd":
                    msg = ("direcao", direcao)
                    send_object(client_socket, msg) 

    except KeyboardInterrupt:
        interface.clear()
        print("[SAINDO]")
    finally:
        client_socket.close()

