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

globais = threading.local()

#Movimentação
type vec2 = tuple[int, int]

direcoes: dict[str, vec2] = {
    "w": ( 0, -1),
    "a": (-1,  0),
    "s": ( 0,  1),
    "d": ( 1,  0),
}

#[]
def mudar_pos(mapa_novo: str, dest: vec2, mapa_velho: str, pos: vec2,
              jogador: str, direcao: vec2=(0,0)) -> tuple[str, vec2, int]:
    x, y = pos

    area_velha = area(mapa_velho)
    area_nova  = area(mapa_novo)

    if area_nova != area_velha:
        print(f"mudar_pos: {area_nova=} != {area_velha=}")
        print(f"mudar_pos:{x,y} -> {dest}: {mapa_velho=} != {mapa_novo=}")
        mapa_novo, (nx, ny), pts = mudar_area(mapa_novo, dest,
                                              mapa_velho, (x,y),
                                              jogador, direcao)
    elif mapa_velho != mapa_novo:
        print(f"mudar_pos: {area_nova=} == {area_velha=}")
        print(f"mudar_pos:{x,y} -> {dest}: {mapa_velho=} != {mapa_novo=}")
        nx,ny = nascer(mapa_novo, mapa_velho, direcao_pref=direcao)
        pts = teletransportar(mapa_novo, (nx,ny), mapa_velho, (x,y), jogador=jogador)
    else:
        print(f"mudar_pos:{x,y} -> {dest}: {mapa_velho=} == {mapa_novo=}")
        nx, ny = dest
        pts = teletransportar(mapa_novo, (nx,ny), mapa_velho, (x,y), jogador=jogador)

    return mapa_novo, (nx, ny), pts


def mudar_area(mapa_novo: str, dest: vec2, mapa_velho: str, pos: vec2,
               jogador: str, direcao: vec2=(0,0)) -> tuple[str, vec2, int]:
    x,y = pos

    area_velha = area(mapa_velho)
    area_nova  = area(mapa_novo)

    pts = 0
    if area_nova == 'hub':
        print(f"mudar_area ({jogador}, hub): {area_velha=} != {area_nova=}")
        print(f"mudar_area:{x,y} -> {dest}: {mapa_velho=} != {mapa_novo=}")
        globais.timer.cancel()

        vazio = not contar_tesouros(area_velha)
        if vazio or not dest:
            nx, ny = nascer(mapa_novo, area_velha, direcao_pref=direcao, comer=vazio)
        else:
            nx, ny = dest

        pts = teletransportar(mapa_novo, (nx,ny), mapa_velho, (x,y), comer=vazio,
                                                                     jogador=jogador)
        area_locks[area_velha].release()
        globais.ponto_fora = (mapa_novo, (nx,ny))
    else: #! fila
        print(f"mudar_area ({jogador}, else): {area_velha=} != {area_nova=}")
        print(f"mudar_area:{x,y} -> {dest}: {mapa_velho=} != {mapa_novo=}")
        if area_locks[area_nova].acquire(timeout=0.4):
            print(f"mudar_area ({jogador} conseguiu entrar) ")
            globais.ponto_fora = (mapa_velho, (x,y))
            globais.timer = threading.Timer(10, globais.tempo_esgotado.set)
            globais.timer.start()

            nx,ny = nascer(mapa_novo, mapa_velho, direcao_pref=direcao)
            pts = teletransportar(mapa_novo, (nx,ny), mapa_velho, (x,y), jogador=jogador)
        else:
            print(f"mudar_area ({jogador} não conseguiu entrar) ")
            mapa_novo, (nx,ny) = mapa_velho, (x,y)
            print(f"mudar_area:{x,y} -> {nx,ny}: {mapa_velho=} != {mapa_novo=}")
    return mapa_novo, (nx, ny), pts

#[]
def atualiza_cliente(conn, nome_mapa: str, jogador: str, pts: int, addr=None):
    if pts:
        if not contar_tesouros(): fim_jogo.set()
        
        pontos[jogador] += pts*5
        msg = ("qtd_pontos", pontos[jogador])
        send_object(conn, msg, addr)

    msg = ("mapa_novo", nome_mapa, mapas[nome_mapa])
    send_object(conn, msg, addr)

#Função da thread de cada cliente
def handle_client(conn, addr):
    jogador = jogadores.get()

    print(f"Jogador: {addr} conectado como {jogador}.")

    nome_mapa = "hub_principal"

    with map_lock:
        x,y = nascer(nome_mapa)
        teletransportar(nome_mapa, (x,y), jogador=jogador)

    globais.ponto_fora = (nome_mapa, (x,y))
    globais.tempo_esgotado = threading.Event()

    buff = []
    while True:
        if fim_jogo.wait(0):
            msg = ("placar", list(pontos.items()))
            send_object(conn, msg, addr)
            break

        if globais.tempo_esgotado.wait(0):
            mapa_novo, (nx, ny) = globais.ponto_fora

            mapa_velho, (x, y) = nome_mapa, (x, y)
            mapa_novo, (nx, ny), pts = mudar_pos(mapa_novo, (nx,ny),
                                                 mapa_velho, (x,y),
                                                 jogador, direcao)
            nome_mapa = mapa_novo
            x, y = (nx, ny)

            atualiza_cliente(conn, nome_mapa, jogador, pts, addr)
            globais.tempo_esgotado.clear()

        response = recv_object(conn, buff, addr)
        match response:
            case ("direcao", direcao):
                direcao = direcoes.get(direcao) or (0,0)
                #! fazer função
                with map_lock:
                    mapa_velho = nome_mapa
                    npos, mapa_novo = mover(nome_mapa, jogador, (x,y), direcao)

                    mapa_novo, (nx, ny), pts = mudar_pos(mapa_novo, npos,
                                                         mapa_velho, (x,y),
                                                         jogador, direcao)

                nome_mapa = mapa_novo
                x, y = (nx, ny)

                atualiza_cliente(conn, nome_mapa, jogador, pts, addr)
                if pts and not contar_tesouros(): fim_jogo.set()

            case ("atualizacao",):
                atualiza_cliente(conn, nome_mapa, jogador, 0, addr)

            case (comando, *resto):
                assert print(comando, resto)

            case None: break
    
    with map_lock:
        mapas[nome_mapa][y][x] = '_' #! setar melhor

    nome_area = area(nome_mapa)
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
                threads.append(t := threading.Thread(target=handle_client, args=(conn, ad)))
                t.start()
            except BlockingIOError:
                continue

    except KeyboardInterrupt:
        print("Saindo...")
    finally:
        for t in threads: t.join()
        sock.close()

