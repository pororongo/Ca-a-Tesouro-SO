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

