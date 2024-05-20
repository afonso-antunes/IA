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

"""pecas qeu nao podem estar"""
pecas_bordas_cantos = ( ("BB", "BC", "BE", "LH", "FE", "VC", "VE"),  # coluna esquerda
                        ("BC", "BD", "BE", "LV", "FC", "VD", "VC"),  # linha de cima
                        ("BB", "BD", "BE", "LV", "FB", "VE", "VB"),  # linha de baixo
                        ("BC", "BD", "BB", "LH", "FD", "VD", "VB"),) # coluna direita

coordenadas_fechadas = None

RODA_HORARIO = 1
RODA_ANTIHORARIO = 2
RODA_180 = 3

tipo_pecas = {
    "L": set(("LV", "LH")),
    "V": set(("VC", "VB", "VD", "VE")),
    "B": set(("BE", "BD", "BC", "BB")),
    "F": set(("FC", "FE", "FD", "FB"))
    }


# posicao que pecas podem estar nos cantos ou entre paralelas que funcionam como cantos
pos_cantos = {
    "right": set(("BE", "VC", "VE", "LV", "FC", "FB", "FE")),
    "left": set(("BD", "LV", "VB", "VD", "FB", "FC", "FD")),
    "up": set(("BB", "FD", "FE", "LH", "FB", "VE", "VB")),
    "down": set(("BC", "FE", "FD", "FC", "VC", "VD", "LH"))
    }


combinacoes_possiveis = {                   
        "BB": {
            "left": set(("BB", "BC", "BD", "FD", "LH", "VB", "VD")), 
            "right": set(("BB", "BC", "BE", "FE", "LH", "VC", "VE")),
            "down": set(("BC", "BD", "BE", "FC", "LV", "VC", "VD"))},
        "BC": {
            "left": set(("BB", "BC", "BD", "FD", "LH", "VB", "VD")),
            "right": set(("BB", "BC", "BE", "FE", "LH", "VC", "VE")), 
            "up": set(("BB", "BD", "BE", "FB", "LV", "VB", "VE"))},
        "BD": {
            "up": set(("BB", "BD", "BE", "FB", "LV", "VB", "VE")), 
            "right": set(("BB", "BC", "BE", "FE", "LH", "VC", "VE")), 
            "down": set(("BC", "BD", "BE", "FC", "LV", "VC", "VD"))},
        "BE": {
            "up": set(("BB", "BD", "BE", "FB", "LV", "VB", "VE")), 
            "left": set(("BB", "BC", "BD", "FD", "LH", "VB", "VD")), 
            "down": set(("BC", "BD", "BE", "FC", "LV", "VC", "VD"))},
        "FB": {
            "down": set(("BC", "BD", "BE", "LV", "VC", "VD"))},
        "FC": {
            "up": set(("BB", "BD", "BE", "LV", "VB", "VE"))},
        "FD": {
            "right": set(("BB", "BC", "BE", "LH", "VC", "VE"))},
        "FE": {
            "left": set(("BB", "BC", "BD", "LH", "VB", "VD"))},
        "LH": {
            "left": set(("BB", "BC", "BD", "FD", "LH", "VB", "VD")), 
            "right": set(("BB", "BC", "BE", "FE", "LH", "VC", "VE"))},
        "LV": {
            "down": set(("BC", "BD", "BE", "FC", "LV", "VC", "VD")), 
            "up": set(("BB", "BD", "BE", "FB", "LV", "VB", "VE"))},
        "VB": {
            "right": set(("BB", "BC", "BE", "FE", "LH", "VC", "VE")), 
            "down": set(("BC", "BD", "BE", "FC", "LV", "VC", "VD"))},
        "VC": {
            "left": set(("BB", "BC", "BD", "FD", "LH", "VB", "VD")), 
            "up": set(("BB", "BD", "BE", "FB", "LV", "VB", "VE"))},
        "VD": {
            "right": set(("BB", "BC", "BE", "FE", "LH", "VC", "VE")), 
            "up": set(("BB", "BD", "BE", "FB", "LV", "VB", "VE"))},
        "VE": {
            "left": set(("BB", "BC", "BD", "FD", "LH", "VB", "VD")), 
            "down": set(("BC", "BD", "BE", "FC", "LV", "VC", "VD"))}
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

    def bloqueia_pecas(self):
        ult_pos = b_size - 1
        changed = True
        while changed:
            changed = False
            for linha in range(ult_pos+1):
                for coluna in range(ult_pos+1):
                    
                    if coordenadas_fechadas[linha, coluna]: continue
                    peca_direita, peca_esquerda, peca_cima, peca_baixo = None, None, None, None
                    peca = self.matriz_board[linha][coluna]
                    

                    peca_cima = self.matriz_board[linha - 1][coluna] if linha > 0 else None
                    peca_esquerda = self.matriz_board[linha][coluna - 1] if coluna > 0 else None
                    peca_baixo = self.matriz_board[linha + 1][coluna] if linha < ult_pos else None
                    peca_direita = self.matriz_board[linha][coluna + 1] if coluna < ult_pos else None

                    coord_cima = (linha - 1, coluna) if linha > 0 else None
                    coord_baixo = (linha + 1, coluna) if linha < ult_pos else None
                    coord_dir = (linha, coluna + 1) if coluna < ult_pos else None
                    coord_esq = (linha, coluna - 1) if coluna > 0 else None

                    pipes_possiveis = set(tipo_pecas[peca[0]])
                    lista_final = pipes_possiveis.copy()

                    if peca_baixo != None and coordenadas_fechadas[coord_baixo[0], coord_baixo[1]]:
                        direcoes_possiveis = combinacoes_possiveis[peca_baixo].keys()
                        if "up" in direcoes_possiveis:
                            lista_final &= combinacoes_possiveis[peca_baixo]["up"]
                        else: lista_final &= pos_cantos["down"]
                    elif peca_baixo == None:
                        lista_final &= pos_cantos["down"]
                        
                    if peca_cima != None and coordenadas_fechadas[coord_cima[0], coord_cima[1]]:
                        direcoes_possiveis = combinacoes_possiveis[peca_cima].keys()
                        if "down" in direcoes_possiveis:
                            lista_final &= combinacoes_possiveis[peca_cima]["down"]
                        else: lista_final &= pos_cantos["up"]
                    elif peca_cima == None:
                        lista_final &= pos_cantos["up"]

                    if peca_direita != None and coordenadas_fechadas[coord_dir[0], coord_dir[1]]:
                        direcoes_possiveis = combinacoes_possiveis[peca_direita].keys()
                        if "left" in direcoes_possiveis:
                            lista_final &= combinacoes_possiveis[peca_direita]["left"]
                        else: lista_final &= pos_cantos["right"]
                    elif peca_direita == None:
                        lista_final &= pos_cantos["right"]

                    if peca_esquerda != None and coordenadas_fechadas[coord_esq[0], coord_esq[1]]:
                        direcoes_possiveis = combinacoes_possiveis[peca_esquerda].keys()
                        if "right" in direcoes_possiveis:
                            lista_final &= combinacoes_possiveis[peca_esquerda]["right"]
                        else: lista_final &= pos_cantos["left"]
                    elif peca_esquerda == None:
                        lista_final &= pos_cantos["left"]

            
                    aux= list(lista_final)
                    if len(aux) == 1:
                        self.matriz_board[linha][coluna] = aux[0]
                        coordenadas_fechadas[linha, coluna] = 1
                        changed = True



    def total_posicoes_imp(self):

        penalizacoes, penalizacoes_bordas, penalizacoes_fecho, penalizacoes_trinco, penalizacoes_reta, penalizacoes_v = 0 ,0, 0, 0, 0, 0
        ult_pos = b_size - 1

        for coluna in range(ult_pos+1):
            for linha in range(ult_pos+1):
                
                peca_direita, peca_esquerda, peca_cima, peca_baixo = None, None, None, None
                peca = self.matriz_board[linha][coluna]
                eh_canto, eh_fecho, eh_trinco, eh_reta, eh_v = False, False, False, False, False

                if peca[0] == "F": eh_fecho = True
                elif peca[0] == "B": eh_trinco = True
                elif peca[0] == "L": eh_reta = True
                elif peca[0] == "V": eh_v = True

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
                    
                    if eh_fecho and peca_esquerda != None and peca_esquerda[0] == "F": penalizacoes_fecho += 3
                    if eh_trinco and peca_esquerda != None: penalizacoes_trinco += 2
                    if eh_reta and peca_esquerda != None: penalizacoes_reta += 1
                    if eh_v and peca_esquerda != None: penalizacoes_v += 1
                    if eh_canto: penalizacoes_bordas += 2
                    
                    else:
                        penalizacoes += 1
                if "right" in direcoes_possiveis and peca_direita not in combinacoes_possiveis[peca]["right"]:
                    
                    if eh_fecho and peca_direita != None and peca_direita[0] == "F": penalizacoes_fecho += 3
                    if eh_trinco and peca_direita != None: penalizacoes_trinco += 2
                    if eh_reta and peca_direita != None: penalizacoes_reta += 1
                    if eh_v and peca_direita != None: penalizacoes_v += 1
                    if eh_canto: penalizacoes_bordas += 2
                    
                    else:
                        penalizacoes += 1
                if "up" in direcoes_possiveis and peca_cima not in combinacoes_possiveis[peca]["up"]:
                    
                    if eh_fecho and peca_cima != None and peca_cima[0] == "F": penalizacoes_fecho += 3
                    if eh_trinco and peca_cima != None: penalizacoes_trinco += 2
                    if eh_reta and peca_cima != None: penalizacoes_reta += 1
                    if eh_v and peca_cima != None: penalizacoes_v += 1
                    if eh_canto: penalizacoes_bordas += 2
                    
                    else:
                        penalizacoes += 1
                if "down" in direcoes_possiveis and peca_baixo not in combinacoes_possiveis[peca]["down"]:

                    if eh_fecho and peca_baixo != None and peca_baixo[0] == "F": penalizacoes_fecho += 3
                    if eh_trinco and peca_baixo != None: penalizacoes_trinco += 2
                    if eh_reta and peca_baixo != None: penalizacoes_reta += 1
                    if eh_v and peca_baixo != None: penalizacoes_v += 1
                    if eh_canto: penalizacoes_bordas += 2
                    
                    else:
                        penalizacoes += 1
                
        return penalizacoes, penalizacoes_bordas, penalizacoes_fecho, penalizacoes_trinco, penalizacoes_reta, penalizacoes_v
    
   

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
        global coordenadas_fechadas
        
        board = Board()
        linha_atual = stdin.readline().split()
        size = len(linha_atual) - 1
        coordenadas_fechadas = np.zeros((size+1,size+1),dtype=bool)
        linha_matriz = 0

        while linha_atual:
            board.matriz_board.append([])
            coluna = 0

            for peca in linha_atual:
                if coluna == 0 and linha_matriz == 0:
                    if peca[0] == "V":
                        peca = "VB"
                        coordenadas_fechadas[linha_matriz, coluna] = 1
                elif coluna == 0 and linha_matriz == size:
                    if peca[0] == "V":
                        peca = "VD"
                        coordenadas_fechadas[linha_matriz, coluna] = 1
                elif coluna == size and linha_matriz == 0:
                    if peca[0] == "V":
                        peca = "VE"
                        coordenadas_fechadas[linha_matriz, coluna] = 1
                elif coluna == size and linha_matriz == size:
                    if peca[0] == "V":
                        peca = "VC"
                        coordenadas_fechadas[linha_matriz, coluna] = 1
                elif coluna == 0:
                    if peca[0] == "B":
                        peca = "BD"
                        coordenadas_fechadas[linha_matriz, coluna] = 1
                    elif peca[0] == "L":
                        peca = "LV"
                        coordenadas_fechadas[linha_matriz, coluna] = 1
                elif linha_matriz == 0:
                    if peca[0] == "B":
                        peca = "BB"
                        coordenadas_fechadas[linha_matriz, coluna] = 1
                    elif peca[0] == "L":
                        peca = "LH" 
                        coordenadas_fechadas[linha_matriz, coluna] = 1
                elif coluna == size:
                    if peca[0] == "B":
                        peca = "BE"
                        coordenadas_fechadas[linha_matriz, coluna] = 1
                    elif peca[0] == "L":
                        peca = "LV"
                        coordenadas_fechadas[linha_matriz, coluna] = 1
                elif linha_matriz == size:
                    if peca[0] == "B":
                        peca = "BC"
                        coordenadas_fechadas[linha_matriz, coluna] = 1
                    elif peca[0] == "L":
                        peca = "LH"
                        coordenadas_fechadas[linha_matriz, coluna] = 1    

                board.matriz_board[linha_matriz].append(peca)
                coluna += 1
            linha_matriz += 1

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
                if coordenadas_fechadas[linha, coluna]: continue

                peca = state.board.matriz_board[linha][coluna]
                
                if peca[0] == "L":
                    yield (linha, coluna, RODA_HORARIO)

                else:
                    yield (linha, coluna, RODA_HORARIO)
                    yield (linha, coluna, RODA_ANTIHORARIO)
                    yield (linha, coluna, RODA_180)


    def roda_peca(self, peca, direcao):
        # True - direcao ponteiros do relogio
        parte1, parte2 = peca[0], peca[1]
        nova_parte2 = ""

        if parte2 in 'HV':
            nova_parte2 = 'V' if parte2 == 'H' else 'H'


        else:
            idx = direcoes.index(parte2)
            if direcao == RODA_HORARIO:
                nova_parte2 = direcoes[(idx + 1) % 4]
            elif direcao == RODA_ANTIHORARIO:
                nova_parte2 = direcoes[(idx - 1) % 4]
            elif direcao == RODA_180:
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
        
        for linha in range(ult_pos+1):  
            for coluna in range(ult_pos+1):
               
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
        
        erradas ,erros_borda,  erros_fecho ,  erros_trinco ,  erros_reta ,  erros_v = node.state.board.total_posicoes_imp()
        return erradas + erros_borda + erros_fecho + erros_trinco + erros_reta + erros_v 

    # TODO: outros metodos da classe



if __name__ == "__main__":
    
    

    board = Board.parse_instance()
    problem = PipeMania(board)
    
    b_size = board.board_size()

    
    
    problem.board.bloqueia_pecas()
    goal_node = recursive_best_first_search(problem)
    print(goal_node.state.board.board_print(), sep="")
    


    pass
