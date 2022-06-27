from __future__ import annotations
from tkinter import *
from typing import List, Tuple

class Posicao:
    
    def __init__(self, x : int, y : int):
        self.__moeda : bool = False
        self.__jogador1 : bool = False
        self.__jogador2 : bool = False
        self.__x : int = x
        self.__y : int = y

    def moeda(self) -> bool:
        return self.__moeda
    
    def jogador1(self) -> bool:
        return self.__jogador1
    
    def jogador2(self) -> bool:
        return self.__jogador2
    
    def x(self) -> int:
        return self.__x
    
    def y(self) -> int:
        return self.__y
    
    def set_x(self, x : int) -> None:
        self.__x = x

    def set_y(self, y : int) -> None:
        self.__y = y

    def set_jogador1(self) -> None:
        self.__moeda = False
        self.__jogador2 = False
        self.__jogador1 = True

    def set_jogador2(self) -> None:
        self.__moeda = False
        self.__jogador1 = False
        self.__jogador2 = True

    def set_moeda(self) -> None:
        self.__moeda = True
        self.__jogador1 = False
        self.__jogador2 = False

    def set_vazio(self) -> None:
        self.__moeda = False
        self.__jogador1 = False
        self.__jogador2 = False

class Jogador:
    
    def __init__(self, pos : Posicao) -> None:
        self.__pos = pos
        self.__energia = 5
        self.__moedas = 0

    def adicionar_moeda(self) -> None:
        self.__moedas += 1

    def consumir_energia(self, qtd : int) -> None:
        self.__energia = max(self.__energia-qtd, 0)
    
    def adicionar_energia(self, qtd : int) -> None:
        self.__energia += qtd

    def obter_posicao(self) -> Posicao:
        return self.__pos

    def energia(self) -> int:
        return self.__energia
    
    def moedas(self) -> int:
        return self.__moedas


class ResultadosJogada:

    def __init__(self, m_pos : List[Posicao], prox_jogador : int, partida_encerrada : bool):
        self.__posicoes_modificadas = m_pos
        self.__prox_jogador = prox_jogador
        self.__partida_encerrada = partida_encerrada

    def __repr__(self) -> str:
        return "{} {} {}".format(self.__posicoes_modificadas, self.__prox_jogador, self.__partida_encerrada)

    def obter_pos_modificadas(self) -> List[Posicao]:
        return self.__posicoes_modificadas
    
    def obter_prox_jogador(self) -> int:
        return self.__prox_jogador
    
    def obter_status_partida(self) -> bool:
        return self.__partida_encerrada

class Tabuleiro:
    """
    Essa classe é responsável pela lógica do jogo. 
    Armazena o estado do jogo e computa o próximo estado quando um jogador realiza uma ação.
    Pertence ao domínio do problema.
    """
    def __init__(self) -> None:
        self.__jogador1 : Jogador = Jogador(Posicao(0, 0))
        self.__jogador2 : Jogador = Jogador(Posicao(11, 11))
        self.__jogador_atual : int = 0
        self.__x_dir_j_atual : int = 0
        self.__y_dir_j_atual : int = 0
        self.__posicoes : List[List[Posicao]] = list()
        self.__partida_finalizada : bool = False

    def __obter_jogador_atual(self) -> Jogador:
        if self.__jogador_atual == 0:
            return self.__jogador1
        else:
            return self.__jogador2

    def estado_inicial(self) -> None:
        self.__jogador1 : Jogador = Jogador(Posicao(0, 0))
        self.__jogador2 : Jogador = Jogador(Posicao(11, 11))
        self.__jogador_atual : int = 0
        self.__x_dir_j_atual : int = 0
        self.__y_dir_j_atual : int = 0
        self.__posicoes : List[List[Posicao]] = list()
        self.__partida_finalizada : bool = False

        for x in range(12):
            linha : List[Posicao] = list()
            for y in range(12):
                pos = Posicao(x,y)
                if x == 0 and y == 0:
                    pos.set_jogador1()
                elif x == 11 and y == 11:
                    pos.set_jogador2()
                elif ((x % 2 == 0 and y % 2 != 0) or (x % 2 != 0 and y % 2 == 0)) and (x != 0 and y != 0 and x != 11 and y != 11):
                    pos.set_moeda()

                linha.append(pos)
            self.__posicoes.append(linha)
    
    def obter_estado_atual(self) -> List[List[Posicao]]:
        return self.__posicoes
    
    def mover_jogador(self, x : int, y : int) -> List[Posicao]:
        if self.obter_status_partida():
            return ResultadosJogada([], self.__jogador_atual, True)

        posicoes_modificadas = list()
        jogador_atual = self.__obter_jogador_atual()
        original_pos_jogador = jogador_atual.obter_posicao()

        x_atual = original_pos_jogador.x()
        y_atual = original_pos_jogador.y()
        novo_x = x_atual + x
        novo_y = y_atual + y

        if self.__avaliar_validade_do_movimento(x_atual, y_atual, x, y) is False:
            return ResultadosJogada(posicoes_modificadas, self.__jogador_atual, False)

        original_pos_tabuleiro = self.__posicoes[x_atual][y_atual]
        nova_pos = self.__posicoes[novo_x][novo_y]

        jogo_vencido = self.__efetuar_movimento(jogador_atual, original_pos_tabuleiro, nova_pos, x, y)
        self.__definir_direcao_de_movimento(x,y)

        posicoes_modificadas.append(original_pos_tabuleiro)
        posicoes_modificadas.append(nova_pos)

        if jogo_vencido:
            self.__partida_finalizada = True
            return ResultadosJogada(posicoes_modificadas, self.__jogador_atual, True)
        else: 
            if jogador_atual.energia() == 0:
                self.passar_vez()
            return ResultadosJogada(posicoes_modificadas, self.__jogador_atual, False)

    def __definir_direcao_de_movimento(self, x : int, y : int):
        if self.__x_dir_j_atual == 0 and self.__y_dir_j_atual == 0:
            self.__x_dir_j_atual = x
            self.__y_dir_j_atual = y

    def __avaliar_validade_do_movimento(self, x_atual : int, y_atual : int, x_dir : int, y_dir : int) -> bool:
        novo_x = x_atual + x_dir
        novo_y = y_atual + y_dir
        if novo_y > 11 or novo_y < 0 or novo_x > 11 or novo_x < 0:
            return False
        return True

    def __encerrar_partida(self) -> None:
        self.__partida_finalizada = True

    def __efetuar_movimento(self, j_atual : Jogador, pos_original : Posicao, pos_final : Posicao, x_dir : int, y_dir : int) -> bool:
        pos_original.set_vazio()
        
        partida_encerrada = False

        if pos_final.jogador1() or pos_final.jogador2():
            partida_encerrada = True

        if pos_final.moeda():
            j_atual.adicionar_energia(1)
            j_atual.adicionar_moeda()
            if j_atual.moedas() > 25:
                partida_encerrada = True
        
        if self.__jogador_atual == 0:
            pos_final.set_jogador1()
        else:
            pos_final.set_jogador2()
        
        pos_j_atual = j_atual.obter_posicao()
        pos_j_atual.set_x(pos_final.x())
        pos_j_atual.set_y(pos_final.y())

        energia_gasta = self.__computar_consumo_de_energia(x_dir, y_dir)
        j_atual.consumir_energia(energia_gasta)

        return partida_encerrada

    def __computar_consumo_de_energia(self, x_dir : int, y_dir : int) -> int:
        if self.__x_dir_j_atual == 0 and self.__y_dir_j_atual == 0:
            return 1
        elif self.__x_dir_j_atual == x_dir and self.__y_dir_j_atual == y_dir:
            return 1
        else:
            return 5

    def __redefinir_direcao_de_movimento(self) -> None:
        self.__x_dir_j_atual = 0
        self.__y_dir_j_atual = 0

    def obter_status_partida(self) -> bool:
        return self.__partida_finalizada

    def passar_vez(self) -> ResultadosJogada:
        if self.obter_status_partida():
            return ResultadosJogada([], self.__jogador_atual, self.__partida_finalizada)

        self.__redefinir_direcao_de_movimento()
        if self.__jogador_atual == 0:
            self.__jogador_atual = 1
            self.__jogador1.adicionar_energia(5)
        else:
            self.__jogador_atual = 0
            self.__jogador2.adicionar_energia(5)
        return ResultadosJogada([], self.__jogador_atual, self.__partida_finalizada)

