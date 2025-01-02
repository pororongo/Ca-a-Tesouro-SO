#Tipos de célula
O = '0'
I = '1'
T = '!'
_ = '_'

#Abreviações dos submapas principais
hp = 'hub_principal'
hn, hs = 'hub_norte', 'hub_sul'
hl, ho = 'hub_leste', 'hub_oeste'

ce = 'cemiterio_principal'
cv = 'caverna_principal'
ct = 'catedral_principal'
cs = 'castelo_principal'
mp = 'mansao_principal'

#Grafo/dicionário dos mapas
mapas = dict(
    hub_principal = [ [_,           _, 'hub_norte', _, _          ],
                      [_,           _, _,           _, _          ],
                      ['hub_oeste', _, mp,          _, 'hub_leste'],
                      [_,           _, _,           T, _          ],
                      [_,           _, 'hub_sul',   _, _          ] ],
    
    hub_sul =       [ [_, _, hp, _, _],
                      [_, _, _,  _, _],
                      [_, _, _,  _, _],
                      [_, _, _,  _, _],
                      [T, _, ct, _, _] ],
    
    hub_norte =     [ [_, _, cs, _, _],
                      [_, _, _,  _, _],
                      [_, _, _,  _, T],
                      [_, _, _,  _, _],
                      [_, _, hp, _, _] ],
    
    hub_oeste =     [ [_, _, _, _,  _],
                      [_, _, _, _,  _],
                      [ce, _, _, _, hp],
                      [_, _, _, _,  _],
                      [_, _, T, _,  _] ],
    
    hub_leste =     [ [_,  _, T, _, _],
                      [_,  _, _, _, _],
                      [hp, _, _, _, cv],
                      [_,  _, _, _, _],
                      [_,  _, _, _, _] ],
    
    
    cemiterio_principal = [ [_,                 _, 'cemiterio_norte', _, _],
                            [_,                 _, _,                 _, _],
                            ['cemiterio_oeste', _, _,                 _, ho],
                            [_,                 _, _,                 _, _],
                            [T,                 _, 'cemiterio_sul',   _, _] ],
    
    cemiterio_sul =       [ [_, _, ce, _, _],
                            [_, _,  _, _, _],
                            [_, _,  _, _, _],
                            [_, _,  _, _, _],
                            [_, _,  _, _, _] ],
    
    cemiterio_norte =     [ [_, _,  _, _, _],
                            [_, _,  _, _, _],
                            [_, _,  _, _, T],
                            [_, _,  _, _, _],
                            [_, _, ce, _, _] ],
    
    cemiterio_oeste =     [ [_, _, _, _,  _],
                            [_, _, _, _,  _],
                            [_, _, _, _, ce],
                            [_, _, _, _,  _],
                            [_, _, _, _,  _] ],
    
    
    mansao_principal =    [ [_,              _, 'mansao_norte', _, _],
                            [_,              _, _,              _, _],
                            ['mansao_oeste', _, hp,             _, 'mansao_leste'],
                            [_,              _, _,              _, _],
                            [_,              _, 'mansao_sul',   _, _] ],
    
    mansao_sul =          [ [_, _, mp, _, _],
                            [_, _, _,  _, _],
                            [_, _, T,  _, _],
                            [_, _, _,  _, _],
                            [_, _, _,  _, _] ],
    
    mansao_norte =        [ [_, _, _,  _, _],
                            [_, _, _,  _, _],
                            [_, _, _,  _, _],
                            [_, _, _,  _, _],
                            [_, _, mp, _, _] ],
    
    mansao_oeste =        [ [_, _, _, _,  _],
                            [_, _, _, _,  _],
                            [_, _, _, _, mp],
                            [_, _, _, _,  _],
                            [_, _, _, _,  _] ],
    
    mansao_leste =        [ [_,  _, _, _, T],
                            [_,  _, _, _, _],
                            [mp, _, _, _, _],
                            [_,  _, _, _, _],
                            [_,  _, _, _, _] ],
    
    
    caverna_principal =    [ [_,  _, 'caverna_norte', _, _],
                             [_,  _, _,               _, _],
                             [hl, _, T,               _, 'caverna_leste'],
                             [_,  _, _,               _, _],
                             [_,  _, 'caverna_sul',   _, _] ],
    
    caverna_sul =          [ [_, _, cv, _, _],
                             [_, _, _,  _, _],
                             [_, _, _,  _, _],
                             [_, _, _,  _, _],
                             [_, _, T,  _, _] ],
    
    caverna_norte =        [ [_, _, _,  _, _],
                             [_, _, _,  _, _],
                             [_, _, _,  _, _],
                             [_, _, _,  _, _],
                             [_, _, cv, _, _] ],
    
    caverna_leste =        [ [_,  _, _, _, _],
                             [_,  _, _, _, _],
                             [cv, _, _, _, _],
                             [_,  _, _, _, _],
                             [_,  _, _, _, _] ],
    
    
    catedral_principal =    [ [_,                _, hs,              _, _],
                              [_,                _, _,               _, _],
                              ['catedral_oeste', _, _,               _, 'catedral_leste'],
                              [_,                _, _,               _, _],
                              [_,                _, 'catedral_sul',  _, _] ],
    
    catedral_sul =          [ [_, _, ct, _, _],
                              [_, _, _,  _, _],
                              [_, _, _,  _, _],
                              [_, _, _,  _, _],
                              [_, _, _,  _, _] ],
    
    catedral_oeste =        [ [_, _, _, _, _],
                              [_, _, _, _, _],
                              [T, _, _, _, ct],
                              [_, _, _, _, _],
                              [_, _, _, _, _] ],
    
    catedral_leste =        [ [_,  _, _, _, _],
                              [_,  _, _, _, _],
                              [ct, _, _, _, T],
                              [_,  _, _, _, _],
                              [_,  _, _, _, _] ],
    
    
    castelo_principal =    [ [_,               _, 'castelo_norte',  _, _],
                             [_,               _, _,                _, _],
                             ['castelo_oeste', _, _,                _, 'castelo_leste'],
                             [_,               _, _,                _, _],
                             [_,               _, hn,               _, _] ],
    
    castelo_norte =        [ [_, _, _,  _, _],
                             [_, _, T,  _, _],
                             [_, _, _,  _, _],
                             [_, _, _,  _, _],
                             [_, _, cs, _, _] ],
    
    castelo_oeste =        [ [_, _, _, _, _],
                             [_, _, _, _, _],
                             [_, _, _, _, cs],
                             [_, _, _, _, _],
                             [_, _, _, _, _] ],
    
    castelo_leste =        [ [_,  _, _, _, _],
                             [_,  _, _, _, _],
                             [cs, _, _, _, _],
                             [_,  _, T, _, _],
                             [_,  _, _, _, _] ]
)

#Movimento

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



def mover(nome_mapa: str, jogador: str, pos: vec2, direcao: str, map_lock) -> tuple[vec2, str]:
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


#Funções de verificação de célula

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
