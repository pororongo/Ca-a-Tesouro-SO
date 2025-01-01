"""Funções de lidar com a tela"""

import os


#Função do menu
def menu(client, addr):
    print("\n-------------- [BEM-VINDO À CAÇA ÀS RELíQUIAS!] --------------")
    print("\n"*16, end='') #! usar o número de linhas do tutorial
    print("Escolha uma opção para prosseguir.")
    print("1 -    Jogar")
    print("2 - Tutorial")
    print("0 -     Sair")

    opcao = input()
    if opcao == "1":
        clear()
        client.connect(addr) 
    elif opcao == "2":
        clear()
        tutorial(client, addr)
    elif opcao == "0":
        clear()
        print("Encerrando o jogo...")
        exit()
    else:
        clear()
        print("--------- [OPÇÃO INVÁLIDA] ---------")
        menu(client, addr)

#Função do tutorial        
def tutorial(client, addr):
    print("\n------------------------- [TUTORIAL] -------------------------")
    print("\n")
    print("Ao iniciar o jogo, você compete com [4] jogadores")
    print("numa busca por [RELÍQUIAS PARANORMAIS].")
    print("Movimente-se pelo mapa usando [WASD].")
    print("Os mapas possuem extensões [SUL], [NORTE], [LESTE] e [OESTE].")
    print("O símbolo 0 te leva para uma dessas extensões.")
    print("O símbolo 1 te leva para uma sala das [RELÍQUIAS].")
    print("O símbolo ! representa uma [RELÍQUIA].")

    print("Nas salas de [RELÍQUIAS], o [TEMPO] de estadia é [LIMITADO].")
    print("Encontre uma [RELÍQUIA] dentro de 15s para [OBTÊ-LA].")
    print("Quando todas as [RELÍQUIAS] forem [OBTIDAS],")
    print("a [BUSCA] é encerrada.")
    print("O [JOGADOR] com o maior número de [RELÍQUIAS] é vencedor.")
    print("\n")
    print("Escolha uma opção para prosseguir.")
    print("1 -    Jogar")
    print("2 -     Menu")
    print("0 -     Sair")

    opcao = input()
    if opcao == '1':
        clear()
        client.connect(addr)
    elif opcao == '2':
        clear()
        menu(client, addr)
    elif opcao == '0':
        clear()
        print("Encerrando o jogo...")
        exit()
    else:
        clear()
        print("--------- [OPÇÃO INVÁLIDA] ---------\n")
        tutorial(client, addr)
        
def rend_mapa(mapa: list[list], nome: str=''):
    print(nome.upper())

    for linha in mapa:
        print(end=' '*3)
        for cel in linha:
            print(f'{cel}{cel}'[:2], end=' ')
        print()

def clear():
    os.system('clear')

