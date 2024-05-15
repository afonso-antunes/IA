# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 116:
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

pecas_bordas_cantos = ( ("BB", "BC", "BE", "LH", "FE", "VC", "VE"),  # coluna esquerda
                        ("BC", "BD", "BE", "LV", "FC", "VD", "VC"),  # linha de cima
                        ("BB", "BD", "BE", "LV", "FB", "VE", "VB"),  # linha de baixo
                        ("BC", "BD", "BB", "LH", "FD", "VD", "VB"),) # coluna direita

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

    #matriz_board = []

    def __init__(self):
        self.matriz_board = []


    def total_posicoes_imp(self):

        penalizacoes = 0
        ult_pos = b_size - 1

        for coluna in range(ult_pos+1):
            for linha in range(ult_pos+1):
                num_erradas = 0
                peca_direita, peca_esquerda, peca_cima, peca_baixo = None, None, None, None
                peca = self.matriz_board[linha][coluna]
                eh_canto = False

                if linha != 0:
                    peca_cima = self.matriz_board[linha - 1][coluna]
                if coluna != 0:
                    peca_esquerda = self.matriz_board[linha][coluna - 1]
                if linha != ult_pos:
                    peca_baixo = self.matriz_board[linha + 1][coluna]
                if coluna != ult_pos:
                    peca_direita = self.matriz_board[linha][coluna + 1]

                if peca_esquerda == None or peca_direita == None or peca_baixo == None or peca_cima == None:
                    eh_canto = True
                direcoes_possiveis = combinacoes_possiveis[peca].keys()
                if "left" in direcoes_possiveis and peca_esquerda not in combinacoes_possiveis[peca]["left"]:
                    penalizacoes += 1
                    num_erradas += 1
                if "right" in direcoes_possiveis and peca_direita not in combinacoes_possiveis[peca]["right"]:
                    penalizacoes += 1
                    num_erradas += 1
                if "up" in direcoes_possiveis and peca_cima not in combinacoes_possiveis[peca]["up"]:
                    penalizacoes += 2
                    num_erradas += 1
                if "down" in direcoes_possiveis and peca_baixo not in combinacoes_possiveis[peca]["down"]:
                    penalizacoes += 1
                    num_erradas += 1

        return penalizacoes
    
   
    def penalizacao_bordas_cantos(self):
        
        ult_pos = b_size - 1
        penalizacao = 0

        for i in range(ult_pos+1):
            pecaBordaEsq = self.matriz_board[i][0]
            pecaBordaCima = self.matriz_board[0][i]
            pecaBordaBaixo = self.matriz_board[ult_pos][i]
            pecaBordaDir = self.matriz_board[i][ult_pos]

            if i == 0:
                if pecaBordaEsq in pecas_bordas_cantos[0] or pecaBordaEsq in pecas_bordas_cantos[1]:
                    penalizacao += 3
            
            elif i == ult_pos:
                if pecaBordaEsq in pecas_bordas_cantos[0] or pecaBordaEsq in pecas_bordas_cantos[2]:
                    penalizacao += 3
                
                if pecaBordaCima in pecas_bordas_cantos[1] or pecaBordaCima in pecas_bordas_cantos[3]:
                    penalizacao += 3
                
                if pecaBordaBaixo in pecas_bordas_cantos[2] or pecaBordaBaixo in pecas_bordas_cantos[3]:
                    penalizacao += 3
            
            else:
                if pecaBordaEsq in pecas_bordas_cantos[0]:
                    penalizacao += 3
                
                if pecaBordaCima in pecas_bordas_cantos[1]:
                    penalizacao += 3
                
                if pecaBordaBaixo in pecas_bordas_cantos[2]:
                    penalizacao += 3

                if pecaBordaDir in pecas_bordas_cantos[3]:
                    penalizacao += 3

        return penalizacao 


    def board_print(self):
        board_lines = []
        for linha in self.matriz_board:
            board_lines.append("\t".join(linha))
        return "\n".join(board_lines)

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
        ult_pos = b_size - 1
        for linha in range(ult_pos+1):                
            for coluna in range(ult_pos+1):
                peca = state.board.matriz_board[linha][coluna]
                if peca[0] == "L":
                    yield (linha, coluna, "RODA_HORARIO")
            
                if peca == "VC" and coluna == 0:
                    yield (linha, coluna, "RODA_HORARIO")
                    yield (linha, coluna, "RODA_180")
                elif peca == "VE" and coluna == 0:
                    yield (linha, coluna, "RODA_180")
                    yield (linha, coluna, "RODA_ANTIHORARIO")
                elif peca == "VD" and linha == 0:
                    yield (linha, coluna, "RODA_HORARIO")
                    yield (linha, coluna, "RODA_180")
                elif peca == "VC" and linha == 0:
                    yield (linha, coluna, "RODA_ANTIHORARIO")
                    yield (linha, coluna, "RODA_180")
                elif peca == "VD" and coluna == ult_pos:
                    yield (linha, coluna, "RODA_ANTIHORARIO")
                    yield (linha, coluna, "RODA_180")
                elif peca == "VB" and coluna == ult_pos:
                    yield (linha, coluna, "RODA_HORARIO")
                    yield (linha, coluna, "RODA_180")
                
                else:
                    yield (linha, coluna, "RODA_HORARIO")
                    yield (linha, coluna, "RODA_ANTIHORARIO")
                    yield (linha, coluna, "RODA_180")


    def roda_peca(self, peca, direcao):
        # True - direcao ponteiros do relogio
        parte1, parte2 = peca[0], peca[1]
        nova_parte2 = ""

        if parte2 in 'HV':
            nova_parte2 = 'V' if parte2 == 'H' else 'H'
        
        else:
            idx = direcoes.index(parte2)
            if direcao == "RODA_HORARIO":
                nova_parte2 = direcoes[(idx + 1) % 4]
            elif direcao == "RODA_ANTIHORARIO":
                nova_parte2 = direcoes[(idx - 1) % 4]
            elif direcao == "RODA_180":
                nova_parte2 = direcoes[(idx + 2) % 4]
        nova_peca = parte1 + nova_parte2
    
        return nova_peca


    def result(self, state: PipeManiaState, action):
        
        new_state = state.copy_state()  
        linha, coluna, direcao_bool = action  
        peca = new_state.board.matriz_board[linha][coluna]
        nova_peca = self.roda_peca(peca, direcao_bool)
        new_state.board.matriz_board[linha][coluna] = nova_peca    
        return new_state

    def goal_test(self, state: PipeManiaState):
        ult_pos = b_size - 1
        
        for coluna in range(ult_pos+1):  
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
        
        erradas = node.state.board.total_posicoes_imp()
        border_error = node.state.board.penalizacao_bordas_cantos()
        print(node.state.board.board_print(), erradas, border_error)
        print("\n")
        #print("heuri ", heuri , " - erros bordas ", border_error)
       
        #print(heuri)
        return erradas + border_error

    # TODO: outros metodos da classe



if __name__ == "__main__":
    
    ## usar get_value e ver se horizontal value e vertical podem ajudar

    board = Board.parse_instance()
    problem = PipeMania(board)
    #print("is goal? ", problem.goal_test(problem))
    #problem.board.board_print()
    b_size = board.board_size()
    goal_node = recursive_best_first_search(problem)
    print(goal_node.state.board.board_print(), sep="")
    

    
    #print(problem.board.penalizacao_bordas_cantos())
    #problem.board.board_print()
    pass
