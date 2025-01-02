from socket import (socket, gethostbyname, gethostname,
                    AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR)

from collections import defaultdict

from fases import mapas, nascer, mover
from serializador import send_object, recv_object

import threading
import queue


#Declaração da porta, servidor, máximo de jogadores permitidos e pontuação
port = 65432
server = gethostbyname(gethostname())
addr = (server, port)

pontos = defaultdict[str, int](int)
max_jogadores = 5

#Multithreading
map_lock = threading.Lock()
jogadores = queue.Queue(max_jogadores)

#Função da thread de cada cliente
def handle_client(conn, addr):
    jogador   = jogadores.get()
    nome_mapa = "hub_principal"

    print(f"Jogador: {addr} conectado como {jogador}.")

    with map_lock:
        x,y = nascer('_', nome_mapa)
        mapas[nome_mapa][y][x] = jogador #! setar melhor

    pts = 0
    buff = []
    while True:
        response = recv_object(conn, buff, addr)
        match response:
            case ("direcao", direcao): #! lidar com direção errada
                (x,y), nome_mapa, pts = mover(nome_mapa, jogador, (x,y), direcao, map_lock)
                msg = ("mapa_novo", nome_mapa, mapas[nome_mapa])
                send_object(conn, msg, addr)

                pontos[jogador] += pts
                if pts:
                    msg = ("qtd_pontos", pontos[jogador])
                    send_object(conn, msg, addr)

            case ("atualizacao",):
                msg = ("mapa_novo", nome_mapa, mapas[nome_mapa])
                send_object(conn, msg, addr)

                if pts:
                    msg = ("qtd_pontos", pontos[jogador])
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

