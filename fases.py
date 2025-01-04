#Tipos de célula
O = '0'
I = '1'
T = '!'
_ = '_'

#Abreviações dos submapas principais
hp = 'hub_principal'
hn, hs = 'hub_norte', 'hub_sul'
hl, ho = 'hub_leste', 'hub_oeste'

ce = 'cemiterio'
cv = 'caverna'
ct = 'catedral'
cs = 'castelo'
mp = 'mansao'

#Áreas pras locks e função para saber a área
areas = [ ce, cv, ct, cs, mp ]

def area(nome_mapa: str) -> str:
    return nome_mapa.split('_')[0]

#Grafo/dicionário dos mapas
mapas = dict(
    hub_principal =  [ [_,  _, hn, _, _ ],
                       [_,  _, _,  _, _ ],
                       [ho, _, mp, _, hl],
                       [_,  _, _,  T, _ ],
                       [_,  _, hs, _, _ ] ],
    
    hub_sul       =  [ [_, _, hp, _, _],
                       [_, _, _,  _, _],
                       [_, _, _,  _, _],
                       [_, _, _,  _, _],
                       [T, _, ct, _, _] ],
    
    hub_norte     =  [ [_, _, cs, _, _],
                       [_, _, _,  _, _],
                       [_, _, _,  _, T],
                       [_, _, _,  _, _],
                       [_, _, hp, _, _] ],
    
    hub_oeste     =  [ [_, _, _, _,  _],
                       [_, _, _, _,  _],
                       [ce, _, _, _, hp],
                       [_, _, _, _,  _],
                       [_, _, T, _,  _] ],
    
    hub_leste     =  [ [_,  _, T, _, _],
                       [_,  _, _, _, _],
                       [hp, _, _, _, cv],
                       [_,  _, _, _, _],
                       [_,  _, _, _, _] ],
    
    
    cemiterio       =  [ [_,                 _, 'cemiterio_norte', _, _],
                         [_,                 _, _,                 _, _],
                         ['cemiterio_oeste', _, _,                 _, ho],
                         [_,                 _, _,                 _, _],
                         [T,                 _, 'cemiterio_sul',   _, _] ],
    
    cemiterio_sul   =  [ [_, _, ce, _, _],
                         [_, _,  _, _, _],
                         [_, _,  _, _, _],
                         [_, _,  _, _, _],
                         [_, _,  _, _, _] ],
    
    cemiterio_norte =  [ [_, _,  _, _, _],
                         [_, _,  _, _, _],
                         [_, _,  _, _, T],
                         [_, _,  _, _, _],
                         [_, _, ce, _, _] ],
    
    cemiterio_oeste =  [ [_, _, _, _,  _],
                         [_, _, _, _,  _],
                         [_, _, _, _, ce],
                         [_, _, _, _,  _],
                         [_, _, _, _,  _] ],
    
    
    mansao       =  [ [_,              _, 'mansao_norte', _, _],
                      [_,              _, _,              _, _],
                      ['mansao_oeste', _, hp,             _, 'mansao_leste'],
                      [_,              _, _,              _, _],
                      [_,              _, 'mansao_sul',   _, _] ],
    
    mansao_sul   =  [ [_, _, mp, _, _],
                      [_, _, _,  _, _],
                      [_, _, T,  _, _],
                      [_, _, _,  _, _],
                      [_, _, _,  _, _] ],
    
    mansao_norte =  [ [_, _, _,  _, _],
                      [_, _, _,  _, _],
                      [_, _, _,  _, _],
                      [_, _, _,  _, _],
                      [_, _, mp, _, _] ],
    
    mansao_oeste =  [ [_, _, _, _,  _],
                      [_, _, _, _,  _],
                      [_, _, _, _, mp],
                      [_, _, _, _,  _],
                      [_, _, _, _,  _] ],
    
    mansao_leste =  [ [_,  _, _, _, T],
                      [_,  _, _, _, _],
                      [mp, _, _, _, _],
                      [_,  _, _, _, _],
                      [_,  _, _, _, _] ],
    
    
    caverna       =  [ [_,  _, 'caverna_norte', _, _              ],
                       [_,  _, _,               _, _              ],
                       [hl, _, T,               _, 'caverna_leste'],
                       [_,  _, _,               _, _              ],
                       [_,  _, 'caverna_sul',   _, _              ] ],
    
    caverna_sul   =  [ [_, _, cv, _, _],
                       [_, _, _,  _, _],
                       [_, _, _,  _, _],
                       [_, _, _,  _, _],
                       [_, _, T,  _, _] ],
    
    caverna_norte =  [ [_, _, _,  _, _],
                       [_, _, _,  _, _],
                       [_, _, _,  _, _],
                       [_, _, _,  _, _],
                       [_, _, cv, _, _] ],
    
    caverna_leste =  [ [_,  _, _, _, _],
                       [_,  _, _, _, _],
                       [cv, _, _, _, _],
                       [_,  _, _, _, _],
                       [_,  _, _, _, _] ],
    
    
    catedral       =  [ [_,                _, hs,              _, _               ],
                        [_,                _, _,               _, _               ],
                        ['catedral_oeste', _, _,               _, 'catedral_leste'],
                        [_,                _, _,               _, _               ],
                        [_,                _, 'catedral_sul',  _, _               ] ],
    
    catedral_sul   =  [ [_, _, ct, _, _],
                        [_, _, _,  _, _],
                        [_, _, _,  _, _],
                        [_, _, _,  _, _],
                        [_, _, _,  _, _] ],
    
    catedral_oeste =  [ [_, _, _, _, _],
                        [_, _, _, _, _],
                        [T, _, _, _, ct],
                        [_, _, _, _, _],
                        [_, _, _, _, _] ],
    
    catedral_leste =  [ [_,  _, _, _, _],
                        [_,  _, _, _, _],
                        [ct, _, _, _, T],
                        [_,  _, _, _, _],
                        [_,  _, _, _, _] ],
    
    
    castelo       =  [ [_,               _, 'castelo_norte',  _, _              ],
                       [_,               _, _,                _, _              ],
                       ['castelo_oeste', _, _,                _, 'castelo_leste'],
                       [_,               _, _,                _, _              ],
                       [_,               _, hn,               _, _              ] ],
    
    castelo_norte =  [ [_, _, _,  _, _],
                       [_, _, T,  _, _],
                       [_, _, _,  _, _],
                       [_, _, _,  _, _],
                       [_, _, cs, _, _] ],
    
    castelo_oeste =  [ [_, _, _, _, _],
                       [_, _, _, _, _],
                       [_, _, _, _, cs],
                       [_, _, _, _, _],
                       [_, _, _, _, _] ],
    
    castelo_leste =  [ [_,  _, _, _, _],
                       [_,  _, _, _, _],
                       [cs, _, _, _, _],
                       [_,  _, T, _, _],
                       [_,  _, _, _, _] ]
)

#Movimentação
type vec2 = tuple[int, int]

rosa_dos_ventos: list[vec2] = [
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

def nascer(mapa_novo: str, mapa_velho: str='_', direcao_pref: vec2=(0,0), comer: bool=False) -> vec2:
    x, y = achar_celula(mapa_novo, mapa_velho)

    if comer: return x, y

    #! e se não tiver nenhum lugar?
    for direc in [direcao_pref] + rosa_dos_ventos:
        dx, dy = direc
        nx, ny = x+dx, y+dy
        if espaco_fora(mapa_novo, (nx,ny)): continue

        if espaco_vazio(mapa_novo, (nx,ny)):
            return nx, ny
    else:
        return x,y

def mover(nome_mapa: str, jogador: str, pos: vec2, direcao: vec2) -> tuple[vec2 | None, str]:
    x, y = pos
    dx, dy = direcao
    nx, ny = x+dx, y+dy

    if espaco_fora(nome_mapa, (nx,ny)): return (x, y), nome_mapa

    t = 0
    if portal(nome_mapa, (nx,ny)):
        mapa_novo = mapas[nome_mapa][ny][nx]
        return None, mapa_novo

    elif espaco_vazio(nome_mapa, (nx,ny)) or \
         tesouro(nome_mapa, (nx,ny)):
        return (nx, ny), nome_mapa

    return (x, y), nome_mapa

def teletransportar(mapa_novo: str, dest: vec2,
                    mapa_velho: str='', pos: vec2 | None=None,
                    jogador: str='', comer=False) -> bool:
    nx, ny = dest
    if pos:
        x, y = pos
        if not jogador:
            assert mapas[mapa_velho][y][x].startswith('p')
            jogador = mapas[mapa_velho][y][x]
        mapas[mapa_velho][y][x] = '_' #! setar melhor
    else:
        mapa_velho = mapa_novo
        assert jogador

    t = False
    if (v := espaco_vazio(mapa_novo, (nx,ny))) or \
       (t := tesouro(mapa_novo, (nx,ny))) or comer:
        mapas[mapa_novo][ny][nx] = jogador
    return t


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

def contar_tesouros(nome_area: str='') -> int:
    tesouros = 0
    for nome_mapa, mapa in mapas.items():
        if nome_area and area(nome_mapa) != nome_area:
            continue 

        for y, linha in enumerate(mapa):
            for x, _ in enumerate(linha):
                tesouros += tesouro(nome_mapa,(x,y))

    return tesouros

