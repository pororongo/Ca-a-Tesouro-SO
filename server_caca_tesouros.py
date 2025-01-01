from socket import (socket, gethostbyname, gethostname,
                    AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR)

import threading
import queue

from fases import mapas


#Declaração da porta, servidor e máximo de jogadores permitidos
port = 65432
server = gethostbyname(gethostname())
addr = (server, port)
max_jogadores = 5

#Multithreading
map_lock = threading.Lock()
jogadores = queue.Queue(max_jogadores)

#Movimentação
type vec2 = tuple[int, int]

direcoes: dict[str, vec2] = {
    "w": ( 0, -1),
    "a": (-1,  0),
    "s": ( 0,  1),
    "d": ( 1,  0),
}

rosa_dos_ventos = [
    ( 0, -1),
    (-1,  0),
    ( 0,  1),
    ( 1,  0),

    ( 1,  1),
    (-1, -1),
    ( 1, -1),
    (-1,  1),
]

def achar_celula(nome_mapa: str, procurado: str):
    pos = (0,0)
    for y, linha in enumerate(mapas[nome_mapa]):
        for x, cel in enumerate(linha):
            if cel == procurado: return x, y
    return pos

def nascer(mapa_velho: str, mapa_novo: str, direcao_pref: vec2=(0,0)) -> vec2: #! mapa velho opcional
    x, y = achar_celula(mapa_novo, mapa_velho)

    #! e se não tiver nenhum lugar?
    for direc in [direcao_pref] + rosa_dos_ventos:
        dx, dy = direc
        nx, ny = x+dx, y+dy
        if espaco_fora(mapa_novo, (nx,ny)): continue

        if espaco_vazio(mapa_novo, (nx,ny)):
            return nx, ny
    else:
        return x,y


def move(nome_mapa: str, jogador: str, pos: vec2, direcao: str) -> tuple[vec2, str]:
    x, y = pos
    dx, dy = direcoes.get(direcao) or (0,0)
    nx, ny = x+dx, y+dy

    if espaco_fora(nome_mapa, (nx,ny)): return (x, y), nome_mapa

    with map_lock:
        if portal(nome_mapa, (nx,ny)):
            mapas[nome_mapa][y][x] = '_' #! setar melhor

            mapa_novo = mapas[nome_mapa][ny][nx]
            nx, ny = nascer(nome_mapa, mapa_novo, direcao_pref=(dx, dy))
            mapas[mapa_novo][ny][nx] = jogador

            return (nx, ny), mapa_novo

        elif espaco_vazio(nome_mapa, (nx,ny)):
            mapa_novo = nome_mapa
            mapas[nome_mapa][y][x] = '_' #! setar melhor
            mapas[nome_mapa][ny][nx] = jogador
            return (nx, ny), mapa_novo

    return (x, y), nome_mapa

def portal(nome_mapa: str, pos: vec2) -> bool:
    x,y = pos
    return mapas[nome_mapa][y][x] in mapas.keys()

def jogador(nome_mapa: str, pos: vec2) -> bool:
    x,y = pos
    return mapas[nome_mapa][y][x].startswith("p")

def tesouro(nome_mapa: str, pos: vec2) -> bool:
    x,y = pos
    return mapas[nome_mapa][y][x] == '!' #!

def espaco_vazio(nome_mapa: str, pos: vec2) -> bool:
    x,y = pos
    return mapas[nome_mapa][y][x] == '_' #!

def espaco_fora(nome_mapa: str, pos: vec2) -> bool:
    x,y = pos

    len_x = len(mapas[nome_mapa][0])
    len_y = len(mapas[nome_mapa])

    return (0 > x or x >= len_x) or \
           (0 > y or y >= len_y)


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
                (x,y), nome_mapa = move(nome_mapa, jogador, (x,y), direcao)
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

