from socket import (socket, gethostbyname, gethostname,
                    AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR)

import threading
import queue

from fases import mapas, nascer, mover

#Declaração da porta, servidor e máximo de jogadores permitidos
port = 65432
server = gethostbyname(gethostname())
addr = (server, port)
max_jogadores = 5

#Multithreading
map_lock = threading.Lock()
jogadores = queue.Queue(max_jogadores)

#[]
def send_object(conn, obj, addr=None):
    conn.send(msg := repr(obj).encode()) #! sintaxe

    if addr: print(f"client: {addr}, send: {msg}")

def recv_object(conn, addr=None):
    response = conn.recv(1024)
    if addr: print(f"client: {addr}, recv: {response}")

    try:
        if response: return eval(response)
        else:        return None
    except SyntaxError: return None

def handle_client(conn, addr):
    jogador   = jogadores.get()
    nome_mapa = "hub_principal"

    print(f"Jogador: {addr} conectado como {jogador}.")

    with map_lock:
        x,y = nascer('_', nome_mapa)
        mapas[nome_mapa][y][x] = jogador #! setar melhor

    msg = ("mapa_novo", nome_mapa, mapas[nome_mapa])
    send_object(conn, msg, addr)

    while True:
        response = recv_object(conn, addr)
        match response:
            case ("direcao", direcao): #! lidar com direção errada
                print(f"Jogador {jogador} quer andar.") #!
                (x,y), nome_mapa = mover(nome_mapa, jogador, (x,y), direcao, map_lock)
                msg = ("mapa_novo", nome_mapa, mapas[nome_mapa])
                send_object(conn, msg, addr)
            case (comando, *resto):
                assert print(comando, resto)

            case None: break
    
    jogadores.put(jogador)
    mapas[nome_mapa][y][x] = '_' #! setar melhor
    conn.close()


if __name__ == "__main__":
    for i in range(max_jogadores):
        jogadores.put(f"p{i+1}")

    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.bind(addr)

        print("Aguardando jogadores...\n")
        threads = []
        sock.listen(max_jogadores)
        while True:
            conn, ad = sock.accept()
            threads.append(t := threading.Thread(target=handle_client,
                                                 args=(conn, ad)))
            t.start()
    except KeyboardInterrupt:
        print("Saindo...")
    finally:
        sock.close()

