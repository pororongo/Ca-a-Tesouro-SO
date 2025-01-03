"""Funções de lidar com a tela"""
import os
from enum import StrEnum

# adaptado de https://stackoverflow.com/a/287944
class Cor(StrEnum):
    PRETO        = '\033[30m'
    VERMELHO_ESC = '\033[31m'
    VERDE_ESC    = '\033[32m'
    LARANJA      = '\033[33m'
    AZUL         = '\033[34m'
    ROXO         = '\033[35m'
    CIANO_ESC    = '\033[36m'
    CINZA_CLA    = '\033[37m'

    CINZA_ESC    = '\033[90m'
    VERMELHO_CLA = '\033[91m'
    VERDE_CLA    = '\033[92m'
    AMARELO      = '\033[93m'
    AZUL_CLA     = '\033[94m'
    VIOLETA      = '\033[95m'
    CIANO        = '\033[96m'
    BRANCO       = '\033[97m'

    NEGRITO    = '\033[1m'
    SUBLINHADO = '\033[4m'

    FECHA = '\033[0m'


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
        print("[SAINDO]")
        exit()
    else:
        clear()
        print("[OPÇÃO INVÁLIDA]")
        menu(client, addr)

#Função do tutorial        
def tutorial(client, addr):
    print("\n------------------------- [TUTORIAL] -------------------------")
    print("\n")
    print("Ao iniciar o jogo, você compete com [4] jogadores")
    print("numa busca por [RELÍQUIAS PARANORMAIS].")
    print("Movimente-se pelo mapa usando [WASD].")
    print("Os mapas possuem extensões [SUL], [NORTE], [LESTE] e [OESTE].")
    print("As portas azuis te levam pelo [MAPA PRINCIPAL].")
    print("As portas brancas te levam pelas sala de [RELÍQUIAS].")
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
        print("[SAINDO]")
        exit()
    else:
        clear()
        print("[OPÇÃO INVÁLIDA]")
        tutorial(client, addr)

def cor_jogador(jogador: str) -> Cor:
    if   jogador[1] == '1': return Cor.VERDE_CLA
    elif jogador[1] == '2': return Cor.VERMELHO_CLA
    elif jogador[1] == '3': return Cor.CIANO
    elif jogador[1] == '4': return Cor.LARANJA
    elif jogador[1] == '5': return Cor.VIOLETA

    return Cor.VERDE_CLA

def rend_mapa(mapa: list[list], nome: str):
    print(nome.upper())

    for linha in mapa:
        print(end=' '*3)
        for cel in linha:
            fim = Cor.FECHA
            if   cel.startswith('p'):
                assert len(cel) == 2
                cor = cor_jogador(cel)                
            elif cel == '!': cor = Cor.NEGRITO + Cor.AMARELO
            elif cel == '_': cor = Cor.CINZA_ESC
            else:
                cor = Cor.NEGRITO
                if cel.startswith('hub'): cor += Cor.AZUL_CLA
                else:                     cor += Cor.CINZA_CLA
            print(cor + f'{cel}{cel}'[:2] + fim, end=' ')
        print()

def rend_tela(mapa: list[list], nome: str='', pontos: int=0):
    rend_mapa(mapa, nome)
    print(f"pontos: {pontos}")

def rend_placar(placar: list[tuple[str, int]]):
    print(f"[FIM DO JOGO]")
    print(f" {Cor.NEGRITO}PLACAR:{Cor.FECHA}")
    for i, (jogador, pontos) in enumerate(sorted(placar, key=lambda x: x[1], reverse=True)):
        cor = cor_jogador(jogador)
        print(f"   {i+1}º. {cor}{jogador}{Cor.FECHA}: {pontos}")

def clear():
    os.system('clear')

