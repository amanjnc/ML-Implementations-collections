import copy,random,math
knapsack_items = {
    'Phone': {'amount': 5, 'value': 1000, 'weight': 0.19},
    'Laptop':{ 'amount': 2, 'value': 700, 'weight': 1.1},
    'V' : {'amount': 10, 'value': 4900, 'weight': 0.27},
    'F': {'amount': 3, 'value': 550, 'weight': 3.75},
    'P': {'amount': 2, 'value': 3850, 'weight': 1.85},
    'J': {'amount': 6, 'value': 1750, 'weight': 0.84},
    'K': {'amount': 2, 'value': 4700, 'weight': 0.51},
    'N': {'amount': 9, 'value': 4750, 'weight': 1.35},
    'X': {'amount': 6, 'value': 3300, 'weight': 4.66},
    'B': {'amount': 3, 'value': 1450, 'weight': 0.77},
    'R': {'amount': 8, 'value': 1050, 'weight': 0.73},
    'G': {'amount': 1, 'value': 3150, 'weight': 2.74},
    'Y':{'amount': 7, 'value': 2650, 'weight': 3.0},
    'H': {'amount': 2, 'value': 2050, 'weight': 0.84},
    'M': {'amount': 3, 'value': 1050, 'weight': 4.53},
    'Q': {'amount': 10, 'value': 3650, 'weight': 1.88},
    'U': {'amount': 2, 'value': 3750, 'weight': 0.16},
    'E': {'amount': 2, 'value': 200, 'weight': 2.68},
    'O': {'amount': 9, 'value': 3750, 'weight': 1.6},
    'T': {'amount': 10, 'value': 4000, 'weight': 4.06}
}
weight_limit = 50
def fitness_fun(state):
    total_weight = 0
    fitness_value = 0

    for item, count in state.items():
        fitness_value += count * knapsack_items[item]['value']
        total_weight += count * knapsack_items[item]['weight']

    if total_weight > weight_limit:
        return -1

    return fitness_value
def generate_initial_state():
    total_weight=0
    
    initial_state = {}
    for item in knapsack_items.keys():
        
        is_choosen=random.randint(0, 1)==1
        initial_state[item] = 0
        if is_choosen:
            total_weight+=knapsack_items[item]['weight']
            initial_state[item] +=1
    
    return initial_state, total_weight

def generate_initial_valid_state():
    state, weight = generate_initial_state()
    while weight > weight_limit:
        state, weight = generate_initial_state()
        
    return state

def next_move(current_state):
    next_states = []

    # Remove an item from the current state
    for item in current_state.keys():
        if current_state[item] > 0:
            next_state = copy.deepcopy(current_state)
            next_state[item] -= 1
            next_states.append(next_state)

    # Add an item to the current state (based on value-to-weight ratio)
    for item in current_state:
        if current_state[item] < knapsack_items[item]['amount']:
            next_state = copy.deepcopy(current_state)
            next_state[item] += 1
            next_states.append(next_state)
    return next_states

            
def simulated_annealing_with_restart(num_restarts):
        best_value = 0
        best_arrangement = None
        best_weight = 0

        initial_state = generate_initial_valid_state()
        current_state = initial_state
        current_fitness = fitness_fun(current_state)
        

        temperature = 1000
        scheduling_factor = 0.999

        while temperature > 0.01:
            child_states = next_move(current_state)
            if not child_states:
                break

            max_fitness = current_fitness
            max_state = current_state

            for child_state in child_states:
                child_fitness = fitness_fun(child_state)
                if child_fitness > max_fitness:
                    max_fitness = child_fitness
                    max_state = child_state

            if max_fitness <= current_fitness:
                break

            probability = math.exp((max_fitness - current_fitness) / temperature)
            if random.random() < probability:
                current_state = max_state
                current_fitness = max_fitness

            temperature *= scheduling_factor

        value = fitness_fun(current_state)
        weight = sum(current_state[item] * knapsack_items[item]['weight'] for item in current_state)

        if value > best_value and weight <= weight_limit:
            best_value = value
            best_arrangement = current_state
            best_weight = weight

        return best_value, best_arrangement, best_weight

def best_neighbor(child_states):
    current_fitness = -float('inf')
    current_state = None
    for child_state in child_states:
        child_fitness = fitness_fun(child_state)
        if child_fitness > current_fitness:
            current_fitness = child_fitness
            current_state = child_state
            
    return current_fitness, current_state
    

def hill_climbing_with_restart():
        best_value = 0
        best_arrangement = None
        best_weight = 0

    
        initial_state = generate_initial_valid_state()
        current_state = initial_state
        current_fitness = fitness_fun(current_state)
        # print('init', initial_state, current_fitness)

        while True:
            child_states = next_move(current_state)
            best_fitness, best_child = best_neighbor(child_states)
            if best_fitness > current_fitness:
                current_fitness = best_fitness
                current_state = best_child
            else:
                break

        value = fitness_fun(current_state)
        weight = sum(current_state[item] * knapsack_items[item]['weight'] for item in current_state)

        if value > best_value and weight <= weight_limit:
            best_value = value
            best_arrangement = current_state
            best_weight = weight

        return best_value, best_arrangement, best_weight



population_size = 100

def generate_individual():
    individual = {}
    for item in knapsack_items:
        individual[item] = random.randint(0, knapsack_items[item]['amount'])
    return individual

def generate_initial_population():
    population = []
    for _ in range(100):
        individual = generate_individual()
        population.append(individual)
    return population
import copy
import random

def crossover(parent1, parent2):
    child = {}
    for item in knapsack_items:
        if random.random() < 0.5:
            child[item] = parent1[item]
        else:
            child[item] = parent2[item]
    return child

def mutate(individual):
    mutation_rate = 0.1
    mutated_individual = copy.deepcopy(individual)
    for item in mutated_individual:
        if random.random() < mutation_rate:
            mutated_individual[item] = random.randint(0, knapsack_items[item]['amount'])
    return mutated_individual

def selection(population):
    fitness_values = [fitness_fun(individual) + 1e-6 for individual in population]
    max_fitness = max(fitness_values)
    selected_individuals = [random.choice(population), random.choice(population)]
    return selected_individuals[0], selected_individuals[1]

def evolve(population, population_size):
    new_population = []
    while len(new_population) < population_size:
        parent1, parent2 = selection(population)
        child = crossover(parent1, parent2)
        mutated_child = mutate(child)
        new_population.append(mutated_child)
    return new_population

def genetic_algorithm():
    population = generate_initial_population()
    population_size = 100  # Define the population size here

    best_fitness = 0
    best_individual = None
    for generation in range(200):
        population = evolve(population, population_size)

        for individual in population:
            fitness = fitness_fun(individual)
            if fitness > best_fitness:
                best_fitness = fitness
                best_individual = individual

    return best_fitness, best_individual

print('hill',hill_climbing_with_restart())
print('simulated', simulated_annealing_with_restart(10))
print('genetic', genetic_algorithm())