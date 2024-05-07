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

combinacoes_imp = {                 #### fecho nao aponta para fecho
    "BB": { 
        "right": ("BD", "FB", "FC", "FD", "LV", "VB", "VD"),
        "down": ("BB", "FB", "FD", "FE", "LH", "VB", "VE")},
    "BC": {
        "right": ("BD", "FB", "FC", "FD", "LV", "VB", "VD"), 
        "down": ("BD", "BE", "FC", "LV", "VC", "VD")},
    "BD": {
        "right": ("BD", "FB", "FC", "FD", "LV", "VB", "VD"), 
        "down": ("BB", "FB", "FD", "FE", "LH", "VB", "VE")}, 
    "BE": {
        "right": ("FE", "BB", "BC", "LH", "VC", "VE"), 
        "down": ("BB", "FB", "FD", "FE", "LH", "VB", "VE")},
    "FB": { 
        "right": ("FE", "BB", "BC", "LH", "VC", "VE"),
        "down": ("BB", "FB", "FD", "FE", "LH", "VB", "VE", "FC")},
    "FC": {
        "right": ("FE", "BB", "BC", "LH", "VC", "VE"),
        "down": ("BD", "BE", "FC", "LV", "VC", "VD")},
    "FD": {
        "right": ("BD", "FB", "FC", "FD", "LV", "VB", "VD", "FE"),
        "down": ("BD", "BE", "FC", "LV", "VC", "VD")},
    "FE": {
        "right": ("FE", "BB", "BC", "LH", "VC", "VE"),
        "down": ("BD", "BE", "FC", "LV", "VC", "VD")},
    "LH": { 
        "right": ("BD", "FB", "FC", "FD", "LV", "VB", "VD"),
        "down": ("BD", "BE", "FC", "LV", "VC", "VD")},
    "LV": {
        "right": ("FE", "BB", "BC", "LH", "VC", "VE"), 
        "down": ("BB", "FB", "FD", "FE", "LH", "VB", "VE")},
    "VB": {
        "right": ("BD", "FB", "FC", "FD", "LV", "VB", "VD"), 
        "down": ("BB", "FB", "FD", "FE", "LH", "VB", "VE")},
    "VC": { 
        "right": ("FE", "BB", "BC", "LH", "VC", "VE"),
        "down": ("BD", "BE", "FB", "FC", "LV", "VC", "VD")},
    "VD": {
        "right": ("BD", "FB", "FC", "FD", "LV", "VB", "VD"), 
        "down": ("BD", "BE", "FB", "FC", "LV", "VC", "VD")},
    "VE": { 
        "right": ("FE", "BB", "BC", "LH", "VC", "VE"),
        "down": ("BB", "FB", "FD", "FE", "LH", "VB", "VE")}
    }

direcoes = {
    'C': {'True': 'D', 'False': 'E'},
    'D': {'True': 'B', 'False': 'C'},
    'B': {'True': 'E', 'False': 'D'},
    'E': {'True': 'C', 'False': 'B'},
    'V': {'True': 'H', 'False': 'H'},
    'H': {'True': 'V', 'False': 'V'}
    }

    ["C", "D", "B", "E"]
    True == +1
    ["V", "H"]

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

        total_imp = 0
        ult_pos = self.board_size()-1
        for coluna in range(ult_pos+1):  
            for linha in range(ult_pos+1):
                peca = self.matriz_board[linha][coluna]
                peca_direita = None
                peca_baixo = None
                
                if linha != ult_pos:
                    peca_baixo = self.matriz_board[linha + 1][coluna]
                if coluna != ult_pos:
                    peca_direita = self.matriz_board[linha][coluna + 1]

                if peca_direita in combinacoes_imp[peca]["right"]:
                    total_imp += 1
                if peca_baixo in combinacoes_imp[peca]["down"]:
                    total_imp += 1   

        return total_imp
    

    def board_print(self):
        for linha in self.matriz_board:
            print(" ".join(linha))

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
        # True -> direcao ponteiro do relogio
        
        parte1, parte2 = peca[0], peca[1]
        nova_parte2 = direcoes[parte2][direcao]
        nova_peca = parte1 + nova_parte2
        return nova_peca

    def result(self, state: PipeManiaState, action):
        
        new_state = state.copy_state()  
        linha, coluna, direcao_bool = action  
        
        direcao = 'True' if direcao_bool else 'False'
        peca = new_state.board.matriz_board[linha][coluna]
        nova_peca = self.roda_peca(peca, direcao)
        new_state.board.matriz_board[linha][coluna] = nova_peca
        new_state.board.board_print()
    
        return new_state

    def goal_test(self, state: PipeManiaState):
        #state.board.board_print()
        ult_pos = state.board.board_size()-1
        if (state.board.matriz_board[0][0] in ("VD", "VC", "VE", "FE", "FC")):
            return False
        if (state.board.matriz_board[ult_pos][0] in ("VE", "VC", "VB", "FB", "FE")):
            return False
        if (state.board.matriz_board[0][ult_pos] in ("VB", "VD", "VC", "FD", "FC")):
            return False
        if (state.board.matriz_board[ult_pos][ult_pos] in ("VB", "VD", "VE", "FD", "FB")):
            return False

        for coluna in range(ult_pos):  
            for linha in range(ult_pos+1):
                peca = state.board.matriz_board[linha][coluna]
                peca_direita = None
                peca_baixo = None
                
                if linha != ult_pos:
                    peca_baixo = state.board.matriz_board[linha + 1][coluna]
                if coluna != ult_pos:
                    peca_direita = state.board.matriz_board[linha][coluna + 1]

                if peca_direita in combinacoes_imp[peca]["right"] or peca_baixo in combinacoes_imp[peca]["down"]:
                    return False   # Quer dizer que as pecas a direita ou em baixo estao numa posicao errada
        return True
                    
    def h(self, node: Node):
        self.roda_pecas_cantos(node.state)
        heuri = node.state.board.total_posicoes_imp()
        print("heuri ", heuri)

        return heuri

    # TODO: outros metodos da classe


if __name__ == "__main__":
    
    ## usar get_value e ver se horizontal value e vertical podem ajudar

    board = Board.parse_instance()
    problem = PipeMania(board)
    goal_node = greedy_search(problem)

    
    #print("is goal? ", problem.goal_test(problem))
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
