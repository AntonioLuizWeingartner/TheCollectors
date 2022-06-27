from typing import Tuple
import tabuleiro
import graficos

class InterfaceJogador:
    """
    Interface com o jogador, ponto inicial da aplicação.
    """

    def __init__(self) -> None:
        self.__tab = tabuleiro.Tabuleiro()
        self.__int_grafica = graficos.GerenteInterfaceGrafica(self.__tab, self)
        
    def inicializar(self) -> None:
        self.__tab.estado_inicial()
        estado_atual_tabuleiro = self.__tab.obter_estado_atual()
        self.__int_grafica.construir_interface_grafica(estado_atual_tabuleiro)

    def mover_jogador(self, x_dir : int, y_dir : int) -> None:
        resultados = self.__tab.mover_jogador(x_dir, y_dir)
        self.__int_grafica.atualizar_posicoes(resultados)
        self.__int_grafica.atualizar_mensagem(resultados)

    def reiniciar_partida(self) -> None:
        self.__tab.estado_inicial()
        estado_atual_tabuleiro = self.__tab.obter_estado_atual()
        self.__int_grafica.atualizar_interface_grafica(estado_atual_tabuleiro)
        self.__int_grafica.redefinir_mensagem()
    
    def passar_vez(self) -> None:
        resultados = self.__tab.passar_vez()
        self.__int_grafica.atualizar_mensagem(resultados)

InterfaceJogador().inicializar()