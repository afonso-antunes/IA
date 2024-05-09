# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# ist1106242 Afonso Antunes

import numpy as np
from sys import stdin
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


direcoes = ("C", "D", "B", "E")


combinacoes_possiveis = {                   
        "BB": {
            "left": ["BB", "BC", "BD", "FD", "LH", "VB", "VD"], 
            "right": ["BB", "BC", "BE", "FE", "LH", "VC", "VE"],
            "down": ["BC", "BD", "BE", "FC", "LV", "VC", "VD"]},
        "BC": {
            "left": ["BB", "BC", "BD", "FD", "LH", "VB", "VD"],
            "right": ["BB", "BC", "BE", "FE", "LH", "VC", "VE"], 
            "up": ["BB", "BD", "BE", "FB", "LV", "VB", "VE"]},
        "BD": {
            "up": ["BB", "BD", "BE", "FB", "LV", "VB", "VE"], 
            "right": ["BB", "BC", "BE", "FE", "LH", "VC", "VE"], 
            "down": ["BC", "BD", "BE", "FC", "LV", "VC", "VD"]},
        "BE": {
            "up": ["BB", "BD", "BE", "FB", "LV", "VB", "VE"], 
            "left": ["BB", "BC", "BD", "FD", "LH", "VB", "VD"], 
            "down": ["BC", "BD", "BE", "FC", "LV", "VC", "VD"]},
        "FB": {
            "down": ["BC", "BD", "BE", "LV", "VC", "VD"]},
        "FC": {
            "up": ["BB", "BD", "BE", "LV", "VB", "VE"]},
        "FD": {
            "right": ["BB", "BC", "BE", "LH", "VC", "VE"]},
        "FE": {
            "left": ["BB", "BC", "BD", "LH", "VB", "VD"]},
        "LH": {
            "left": ["BB", "BC", "BD", "FD", "LH", "VB", "VD"], 
            "right": ["BB", "BC", "BE", "FE", "LH", "VC", "VE"]},
        "LV": {
            "down": ["BC", "BD", "BE", "FC", "LV", "VC", "VD"], 
            "up": ["BB", "BD", "BE", "FB", "LV", "VB", "VE"]},
        "VB": {
            "right": ["BB", "BC", "BE", "FE", "LH", "VC", "VE"], 
            "down": ["BC", "BD", "BE", "FC", "LV", "VC", "VD"]},
        "VC": {
            "left": ["BB", "BC", "BD", "FD", "LH", "VB", "VD"], 
            "up": ["BB", "BD", "BE", "FB", "LV", "VB", "VE"]},
        "VD": {
            "right": ["BB", "BC", "BE", "FE", "LH", "VC", "VE"], 
            "up": ["BB", "BD", "BE", "FB", "LV", "VB", "VE"]},
        "VE": {
            "left": ["BB", "BC", "BD", "FD", "LH", "VB", "VD"], 
            "down": ["BC", "BD", "BE", "FC", "LV", "VC", "VD"]}
        }



class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    def copy_state(self):
        new_board = Board()
        new_board.matriz_board = np.copy(self.board.matriz_board)
        new_state = PipeManiaState(new_board)
        new_state.id = self.id 
        return new_state
    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    matriz_board = []

    def __init__(self):
        self.matriz_board = []


    def total_posicoes_imp(self):

        penalizacoes = 0
        ult_pos = self.board_size()-1

        for coluna in range(ult_pos+1):
            for linha in range(ult_pos+1):
                peca_direita, peca_esquerda, peca_cima, peca_baixo = None, None, None, None
                peca = self.matriz_board[linha][coluna]

                if linha != 0:
                    peca_cima = self.matriz_board[linha - 1][coluna]
                if coluna != 0:
                    peca_esquerda = self.matriz_board[linha][coluna - 1]
                if linha != ult_pos:
                    peca_baixo = self.matriz_board[linha + 1][coluna]
                if coluna != ult_pos:
                    peca_direita = self.matriz_board[linha][coluna + 1]

                direcoes_possiveis = combinacoes_possiveis[peca].keys()
                if "left" in direcoes_possiveis and peca_esquerda not in combinacoes_possiveis[peca]["left"]:
                    penalizacoes += 1
                if "right" in direcoes_possiveis and peca_direita not in combinacoes_possiveis[peca]["right"]:
                    penalizacoes += 1
                if "up" in direcoes_possiveis and peca_cima not in combinacoes_possiveis[peca]["up"]:
                    penalizacoes += 1
                if "down" in direcoes_possiveis and peca_baixo not in combinacoes_possiveis[peca]["down"]:
                    penalizacoes += 1

        return penalizacoes
    
   
                

    def board_print(self):
        for linha in self.matriz_board:
            print("\t".join(linha))

    def board_size(self):
        if len(board.matriz_board) > 0:
            return len(self.matriz_board)
        else:
            return 0  
       
    def get_value(self, row: int, col: int) -> str:
        if 0 <= row < len(self.matriz_board) and 0 <= col < len(self.matriz_board[0]):
            return self.matriz_board[row][col]
        else: 
            return None

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        acima = None
        abaixo = None

        if 0 <= row < len(self.matriz_board) and 0 <= col < len(self.matriz_board[0]):
            if row > 0:
                acima = self.matriz_board[row - 1][col]

            if row < len(self.matriz_board) - 1:
                abaixo = self.matriz_board[row + 1][col]

        return (acima, abaixo)

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):

        esquerda = None
        direita = None

        if 0 <= row < len(self.matriz_board) and 0 <= col < len(self.matriz_board[0]):
            if col > 0:
                esquerda = self.matriz_board[row][col - 1]

            if col < len(self.matriz_board[0]) - 1:
                direita = self.matriz_board[row][col + 1]

        return (esquerda, direita)

    @staticmethod
    def parse_instance():
        board = Board()
        linha = 0
        linha_atual = stdin.readline().split()

        while linha_atual:
            board.matriz_board.append([])

            for peca in linha_atual:
                board.matriz_board[linha].append(peca)
            
            linha += 1
            linha_atual = stdin.readline().split()


        return board
       
    

class PipeMania(Problem):
    def __init__(self, board: Board):
        self.board = board
        self.initial = PipeManiaState(board)

    def actions(self, state: PipeManiaState):
        for linha in range(state.board.board_size()):                # actions pode limitar as pecas
            for coluna in range(state.board.board_size()):
                yield (linha, coluna, 'True')
                yield (linha, coluna, 'False')

        
    
    def roda_pecas_cantos(self, state):
        ult_lin_col = state.board.board_size()-1

        if state.board.get_value(ult_lin_col, ult_lin_col)[0] == 'V':    # canto inf dir
            state.board.matriz_board[ult_lin_col][ult_lin_col] = 'VC'
             
        if state.board.get_value(0, 0)[0] == 'V': # canto sup esq
            state.board.matriz_board[0][0] = 'VB'
    
        if state.board.get_value(0, ult_lin_col)[0] == 'V': # canto sup dir
            state.board.matriz_board[0][ult_lin_col] =  'VE'
        
        if state.board.get_value(ult_lin_col, 0)[0] == 'V': # canto  inf esq
            state.board.matriz_board[ult_lin_col][0] =  'VD'

        return 
    

    def roda_peca(self, peca, direcao):
        # True - direcao ponteiros do relogio
        parte1, parte2 = peca[0], peca[1]
        nova_parte2 = ""

        if parte2 == "H":
            nova_parte2 = "V"
        elif parte2 == "V":
            nova_parte2 = "H"
        else:
            if direcao == "True":
                nova_parte2 = direcoes[(direcoes.index(parte2) + 1) % 4]
            elif direcao == "False":
                nova_parte2 = direcoes[(direcoes.index(parte2) - 1) % 4]

        nova_peca = parte1 + nova_parte2
    
        return nova_peca


    def result(self, state: PipeManiaState, action):
        
        new_state = state.copy_state()  
        linha, coluna, direcao_bool = action  
        
        direcao = 'True' if direcao_bool else 'False'
        peca = new_state.board.matriz_board[linha][coluna]
        nova_peca = self.roda_peca(peca, direcao)
        new_state.board.matriz_board[linha][coluna] = nova_peca
        ###new_state.board.board_print()
    
        return new_state

    def goal_test(self, state: PipeManiaState):
        #state.board.board_print()

        ult_pos = state.board.board_size()-1
        
        for coluna in range(ult_pos):  
            for linha in range(ult_pos+1):
                peca_direita, peca_esquerda, peca_cima, peca_baixo = None, None, None, None
                peca = state.board.matriz_board[linha][coluna]
                
                if linha != 0:
                    peca_cima = state.board.matriz_board[linha - 1][coluna]
                if coluna != 0:
                    peca_esquerda = state.board.matriz_board[linha][coluna - 1]
                if linha != ult_pos:
                    peca_baixo = state.board.matriz_board[linha + 1][coluna]
                if coluna != ult_pos:
                    peca_direita = state.board.matriz_board[linha][coluna + 1]

                direcoes_possiveis = combinacoes_possiveis[peca].keys()
                if "left" in direcoes_possiveis and peca_esquerda not in combinacoes_possiveis[peca]["left"]:
                    return False
                if "right" in direcoes_possiveis and peca_direita not in combinacoes_possiveis[peca]["right"]:
                    return False
                if "up" in direcoes_possiveis and peca_cima not in combinacoes_possiveis[peca]["up"]:
                    return False
                if "down" in direcoes_possiveis and peca_baixo not in combinacoes_possiveis[peca]["down"]:
                    return False
 
        return True
                    
    def h(self, node: Node):
        #self.roda_pecas_cantos(node.state)
        heuri = node.state.board.total_posicoes_imp()
        print("heuri ", heuri)

        return heuri

    # TODO: outros metodos da classe


if __name__ == "__main__":
    
    ## usar get_value e ver se horizontal value e vertical podem ajudar

    board = Board.parse_instance()
    problem = PipeMania(board)
    #print("is goal? ", problem.goal_test(problem))
    problem.board.board_print()
    
    goal_node = greedy_search(problem)
    goal_node.state.board.board_print()

    
    
    #problem.board.board_print()

    """"
    s0 = PipeManiaState(board)
    problem.board.board_print()
    print("Is goal?", problem.goal_test(s0))
    """

    
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
