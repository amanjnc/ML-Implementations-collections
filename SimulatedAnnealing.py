import random
import math
import matplotlib
def generateRandomBoard(size):
    board = []
    used_num = set()
    for _ in range(size):
        picked_num = random.randint(0, size - 1) 
        while picked_num in used_num:
            picked_num = random.randint(0, size - 1) 
        
        board.append(picked_num)
        used_num.add(picked_num)

    return board

def printBoard(board):
    chess_board = [['.' for _ in range(len(board))] for _ in range(len(board))]

    for row, board_val in enumerate(board):
        chess_board[board_val][row] = "Q"

    for row in chess_board:
        print(' '.join(row))

def fitness(board):
    fitness_value = 0

    for queen_idx, queen_pos in enumerate(board):
        for another_queen_idx, another_queen_pos in enumerate(board):
            is_same_queen = queen_idx == another_queen_idx
            if is_same_queen:
                continue

            can_attack_horizontally = queen_pos == another_queen_pos
            can_attack_diagonally = abs(queen_idx - another_queen_idx) == abs(queen_pos - another_queen_pos)

            if can_attack_horizontally or can_attack_diagonally:
                fitness_value += 1

    return fitness_value


def get_neighbors_with_score(idx, board):
    n = len(board)
    fitness_neighbor = []

    for d in (-1, 1):
        board[idx] += d
        is_valid_placement = 0 <= board[idx] < n 
        
        if is_valid_placement:
            fitness_neighbor.append((fitness(board), idx, board[idx]))

        board[idx] -= d

    return fitness_neighbor

def get_all_neighbors(board):
    neighbor_fitness = []

    for idx in range(len(board)):
        neighbor_fitness.extend(get_neighbors_with_score(idx, board))

    return neighbor_fitness

def simulatedAnnealing(board):
    fitness_value = fitness(board)
    energy = fitness(board)
    temperature = 100

    while fitness_value > 0:
        next_state_config = get_all_neighbors(board)
        random_value = random.randint(0, len(next_state_config) - 1)
        chosen_energy, idx, value = next_state_config[random_value]
        energy = fitness(board) - chosen_energy


        probability_of_bad_choice = math.e **(energy / (temperature + 1))

        if chosen_energy < fitness(board):
            board[idx] = value
            fitness_value = fitness(board)

        elif random.uniform(0.0, 1.0) < probability_of_bad_choice:
            board[idx] = value
            fitness_value = fitness(board)

        elif temperature == 0 and fitness(board) < min(next_state_config)[0]:
            return board
        
        temperature *= 0.99
        temperature //= 1
    
    return board


# x = generateRandomBoard(8)
# print(fitness(x))
# printBoard(x)

print(simulatedAnnealing([1,5,6,6,5,4,5,4]))

print(fitness(simulatedAnnealing([1,5,6,6,5,4,5,4])))
print(fitness([1,5,6,6,5,4,5,4]))