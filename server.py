from socket import (socket, gethostbyname, gethostname,
                    AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR)

from collections import defaultdict

from fases import mapas, areas, area, nascer, mover, teletransportar, contar_tesouros
from serializador import send_object, recv_object

import threading
import queue


#Declaração da porta, servidor, máximo de jogadores permitidos e pontuação
port = 65432
server = gethostbyname(gethostname())
addr = (server, port)

pontos = defaultdict[str, int](int)
max_jogadores = 5


#Sincronização
jogadores = queue.Queue(max_jogadores)

fim_jogo   = threading.Event()
map_lock   = threading.Lock()
area_locks = {a: threading.Lock() for a in areas}


#Movimentação
type vec2 = tuple[int, int]

direcoes: dict[str, vec2] = {
    "w": ( 0, -1),
    "a": (-1,  0),
    "s": ( 0,  1),
    "d": ( 1,  0),
}

#Função da thread de cada cliente
def handle_client(conn, addr):
    jogador = jogadores.get()

    print(f"Jogador: {addr} conectado como {jogador}.")

    nome_mapa = "hub_principal"
    nome_area = area(nome_mapa)

    with map_lock:
        x,y = nascer(nome_mapa)
        teletransportar(nome_mapa, (x,y), jogador=jogador)

    buff = []
    while True:
        if fim_jogo.wait(0):
            msg = ("placar", list(pontos.items()))
            send_object(conn, msg, addr)
            break

        response = recv_object(conn, buff, addr)
        match response:
            case ("direcao", direcao):
                direcao = direcoes.get(direcao) or (0,0)
                #! fazer função
                with map_lock:
                    (nx, ny), mapa_novo = mover(nome_mapa, jogador, (x,y), direcao)

                    mapa_velho = nome_mapa
                    area_velha = nome_area

                    area_nova = area(mapa_novo)
                    if area_nova != area_velha:
                        if area_nova == 'hub':
                            vazio = not contar_tesouros(area_velha)

                            nx,ny = nascer(mapa_novo, mapa_velho, direcao_pref=direcao, comer=vazio)
                            _ = teletransportar(mapa_novo, (nx,ny), mapa_velho, (x,y), comer=vazio)
                            area_locks[nome_area].release()
                        else: #! tempo e fila
                            if area_locks[area_nova].acquire(timeout=0.4):
                                nx,ny = nascer(mapa_novo, mapa_velho, direcao_pref=direcao)
                            else:
                                mapa_novo, (nx,ny) = mapa_velho, (x,y)
                    elif mapa_velho != mapa_novo:
                        nx,ny = nascer(mapa_novo, mapa_velho, direcao_pref=direcao)

                    pts = teletransportar(mapa_novo, (nx,ny), mapa_velho, (x,y), jogador=jogador)

                nome_mapa = mapa_novo
                nome_area = area(nome_mapa)
                x, y = (nx, ny)

                if pts:
                    if not contar_tesouros(): fim_jogo.set()
                    
                    pontos[jogador] += pts*5
                    msg = ("qtd_pontos", pontos[jogador])
                    send_object(conn, msg, addr)

                msg = ("mapa_novo", nome_mapa, mapas[nome_mapa])
                send_object(conn, msg, addr)

            case ("atualizacao",):
                msg = ("mapa_novo", nome_mapa, mapas[nome_mapa])
                send_object(conn, msg, addr)

                #! msg = ("qtd_pontos", pontos[jogador])
                #! send_object(conn, msg, addr)

            case (comando, *resto):
                assert print(comando, resto)

            case None: break
    
    with map_lock:
        mapas[nome_mapa][y][x] = '_' #! setar melhor

    if nome_area != 'hub':
        if area_locks[nome_area].locked():
            area_locks[nome_area].release()

    conn.close()
    jogadores.put(jogador)

    print(f"Jogador: {addr} desconectado como {jogador}.")


if __name__ == "__main__":
    for i in range(max_jogadores):
        jogadores.put(f"p{i+1}")

    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        sock.setblocking(False)
        sock.bind(addr)

        print("Aguardando jogadores...\n")
        threads = []
        sock.listen(max_jogadores)
        while not fim_jogo.wait(0):
            try:
                conn, ad = sock.accept()
                threads.append(t := threading.Thread(target=handle_client,
                                                     args=(conn, ad)))
                t.start()
            except BlockingIOError:
                continue

    except KeyboardInterrupt:
        print("Saindo...")
    finally:
        for t in threads: t.join()
        sock.close()

