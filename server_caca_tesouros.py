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

def move(nome_mapa: str, jogador: str, pos: vec2, direcao: str) -> vec2:
    x, y = pos
    dx, dy = direcoes.get(direcao) or (0,0)
    nx, ny = x+dx, y+dy

    if espaco_fora(nome_mapa, (nx,ny)): return x, y

    with map_lock:
        if espaco_vazio(nome_mapa, (nx,ny)): #! comparar melhor
            mapas[nome_mapa][ny][nx] = jogador
            mapas[nome_mapa][y][x] = '_' #! setar melhor
            x, y = nx, ny
    return x, y

def espaco_vazio(nome_mapa: str, pos: vec2) -> bool:
    x,y = pos
    return mapas[nome_mapa][y][x] == '_'

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
        x,y = (0, 0) #! lidar com outros jogadores
        if espaco_vazio(nome_mapa, (x,y)):
            mapas[nome_mapa][y][x] = jogador

    msg = ("mapa_novo", nome_mapa, mapas[nome_mapa])
    send_object(conn, msg, addr)

    while True:
        response = recv_object(conn, addr)
        match response:
            case ("direcao", direcao): #! lidar com direção errada
                #! lidar com outros jogadores
                x,y = move(nome_mapa, jogador, (x,y), direcao)
                msg = ("mapa_novo", "hub_principal", mapas["hub_principal"])
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

