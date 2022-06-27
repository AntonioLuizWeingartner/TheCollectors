from __future__ import annotations
from tkinter import *
from typing import List, Tuple
from unittest import result
from tabuleiro import Posicao, ResultadosJogada, Tabuleiro

class GerenteInterfaceGrafica:
    """
    Essa classe é responsável por exibir o estado do jogo em uma janela.
    Pertence ao domínio da solução.
    """
    
    def __init__(self, tab : Tabuleiro, interface_jogador : 'InterfaceJogador') -> None:
        self.__tab = tab
        self.__interface = interface_jogador
        self.__janela_principal : Tk = None
        self.__quadro_principal : Frame = None
        self.__quadro_mensagem : Frame = None   
        self.__quadro_botoes : Frame = None
        self.__vazio : PhotoImage = None
        self.__moeda : PhotoImage = None
        self.__p1 : PhotoImage = None
        self.__p2 : PhotoImage = None
        self.__imgs_tabuleiro : List[List[Label]] = list()

        self.__mover_cima : Button = None
        self.__mover_baixo : Button = None 
        self.__mover_esquerda : Button = None 
        self.__mover_direita : Button = None    
        self.__passar : Button = None 
        self.__reiniciar : Button = None
        self.__label_mensagem : Button = None

    def atualizar_posicoes(self, resultado_jogada : ResultadosJogada) -> None:
        posicoes = resultado_jogada.obter_pos_modificadas()
        for pos in posicoes:
            img = self.__selecionar_imagem(pos)
            x = pos.x()
            y = pos.y()
            l = self.__get_label(x,y)
            l.configure(image=img)
            l.image = img

    def redefinir_mensagem(self) -> None:
        self.__label_mensagem['text'] = "Vez do jogador 1"
    
    def __gerar_msg_prox_jogador(self, j_atual : int) -> str:
        return "Vez do jogador {}".format(j_atual+1)

    def __gerar_msg_vencedor(self, j_atual : int) -> str:
        return "Jogador {} venceu".format(j_atual+1)

    def atualizar_mensagem(self, resultados_jogada : ResultadosJogada) -> None:
        j_atual = resultados_jogada.obter_prox_jogador()
        if resultados_jogada.obter_status_partida() is False:
            self.__label_mensagem['text'] = self.__gerar_msg_prox_jogador(j_atual)
        else:
            self.__label_mensagem['text'] = self.__gerar_msg_vencedor(j_atual)

    def construir_interface_grafica(self, estado_tabuleiro : List[List[Posicao]]) -> None:
        self.__construir_janela_principal()
        self.__construir_quadros()
        self.__carregar_imagens()
        
        self.__construir_tabuleiro()
        
        self.atualizar_interface_grafica(estado_tabuleiro)

        self.__construir_botoes()

        self.__janela_principal.mainloop()

    def __construir_janela_principal(self) -> None:
        self.__janela_principal = Tk()
        self.__janela_principal.title("The Collectors")
        self.__janela_principal.geometry("1000x1000")
        self.__janela_principal.resizable(False, False)
        self.__janela_principal["bg"] = "gray"

    def __construir_quadros(self) -> None:
        self.__quadro_principal = Frame(self.__janela_principal, padx=32, pady=25, bg="gray")
        self.__quadro_mensagem = Frame(self.__janela_principal, padx=4, pady=1, bg="gray")
        self.__quadro_botoes = Frame(self.__janela_principal, padx=4, pady=1, bg="gray")
        
        self.__quadro_principal.grid(row=0 , column=0)
        self.__quadro_botoes.grid(row=1, column=0)
        self.__quadro_mensagem.grid(row=2 , column=0)
    
    def __carregar_imagens(self) -> None:
        self.__vazio = PhotoImage(file="imagens/fundo.gif")
        self.__moeda = PhotoImage(file="imagens/fundo_moeda.gif")
        self.__p1 = PhotoImage(file="imagens/p1.gif")
        self.__p2 = PhotoImage(file="imagens/p2.gif")

    def __construir_tabuleiro(self) -> None:
        for x in range(12):
            linha : List[Label] = list()
            for y in range(12):
                l = Label(self.__quadro_principal, bd=0.5, relief='solid', image=self.__vazio)
                linha.append(l) 
                l.grid(row=x , column=y)
            self.__imgs_tabuleiro.append(linha)

    def __construir_botoes(self) -> None:
        self.__mover_cima = Button(self.__quadro_botoes, text="cima", command=lambda: self.__interface.mover_jogador(0, -1))
        self.__mover_cima.grid(row=0, column=0)
        self.__mover_baixo = Button(self.__quadro_botoes, text="baixo", command=lambda: self.__interface.mover_jogador(0, 1))
        self.__mover_baixo.grid(row=0, column=1)
        self.__mover_esquerda = Button(self.__quadro_botoes, text="esquerda", command=lambda: self.__interface.mover_jogador(-1, 0))
        self.__mover_esquerda.grid(row=0, column=2)
        self.__mover_direita = Button(self.__quadro_botoes, text="direita", command=lambda: self.__interface.mover_jogador(1, 0))
        self.__mover_direita.grid(row=0, column=3)
        self.__passar = Button(self.__quadro_botoes, text="passar a vez", command=lambda: self.__interface.passar_vez())
        self.__passar.grid(row=0, column=4)
        self.__reiniciar = Button(self.__quadro_botoes, text="reiniciar", command=lambda: self.__interface.reiniciar_partida())
        self.__reiniciar.grid(row=0, column=5)
        self.__label_mensagem = Label(self.__quadro_mensagem, bg="gray", text='Vez do jogador 1', font="arial 14")
        self.__label_mensagem.grid(row=0, column=0, columnspan=3)

    def __get_label(self, x : int, y : int) -> Label:
        return self.__imgs_tabuleiro[x][y]

    def __get_pos(self, estado_tabuleiro : List[List[Posicao]], x : int, y : int) -> Posicao:
        return estado_tabuleiro[x][y]

    def __get_label(self, x : int, y : int) -> Label:
        return self.__imgs_tabuleiro[y][x]

    def atualizar_interface_grafica(self, estado_tabuleiro : List[List[Posicao]]) -> None:
        for x in range(12):
            for y in range(12):
                pos = self.__get_pos(estado_tabuleiro, x, y)
                label = self.__get_label(x,y)
                img = self.__selecionar_imagem(pos)
                label.configure(image=img)
                label.image = img

    def __selecionar_imagem(self, pos : Posicao) -> PhotoImage:
        if pos.jogador1():
            return self.__p1
        elif pos.jogador2():
            return self.__p2
        elif pos.moeda():
            return self.__moeda
        else:
            return self.__vazio