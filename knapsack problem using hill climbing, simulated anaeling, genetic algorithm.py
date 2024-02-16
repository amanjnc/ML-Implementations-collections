import random,math,copy

knapsack_items = {
    'a': {'weight': 4, 'value': 2, 'amount': 4},
    'b': {'weight': 4, 'value': 2, 'amount': 4},
    'c': {'weight': 4, 'value': 2, 'amount': 1},
    'd': {'weight': 4, 'value': 8, 'amount': 4},
    'desktop': {'weight': 3, 'value': 8, 'amount': 4},
}
weight_limit = random.randint(20, 50)
def fitness_fun(state):
    total_weight = 0
    fitness_value = 0

    for item, count in state.items():
        fitness_value += count * knapsack_items[item]['value']
        total_weight += count * knapsack_items[item]['weight']

    if total_weight > weight_limit:
        return 0

    return fitness_value
def generate_initial_state():
    initial_state = {}
    for item in knapsack_items:
        initial_state[item] = random.randint(0, knapsack_items[item]['amount'])
    return initial_state



def next_move(current_state):
    next_states = []

    # Remove an item from the current state
    for item in current_state:
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

            
def simulated_anaeling(initial_state):
    current_state = initial_state
    current_fitness = fitness_fun(current_state)
    
    
    temperature=1000
    scheduling_factor=0.97
    

    while temperature > 0.01:
        child_states = next_move(current_state)
        if not child_states:
            return current_state

        max_fitness = current_fitness
        max_state = current_state

        for child_state in child_states:
            child_fitness = fitness_fun(child_state)
            if child_fitness > max_fitness:
                max_fitness = child_fitness
                max_state = child_state

        if max_fitness <= current_fitness:
            return current_state

        probability = math.exp((max_fitness - current_fitness) / temperature)
        if random.random() < probability:
            current_state = max_state
            current_fitness = max_fitness

        temperature *= scheduling_factor

    return current_state





def simulated_random_restart(num_restarts):
    best_value = 0
    best_arrangement = None
    best_weight = 0

    for _ in range(num_restarts):
        initial_state = generate_initial_state()
        final_state = simulated_anaeling(initial_state)

        value = fitness_fun(final_state)
        weight = sum(final_state[item] * knapsack_items[item]['weight'] for item in final_state)

        if value > best_value and weight <= weight_limit:
            best_value = value
            best_arrangement = final_state
            best_weight = weight
    return best_value, best_arrangement, best_weight,weight_limit


#########################################################


def hill_random_restart(num_restarts):
    best_value = 0
    best_arrangement = None
    best_weight = 0

    for _ in range(num_restarts):
        initial_state = generate_initial_state()
        final_state = hillclimbing(initial_state)

        value = fitness_fun(final_state)
        weight = sum(final_state[item] * knapsack_items[item]['weight'] for item in final_state)

        if value > best_value and weight <= weight_limit:
            best_value = value
            best_arrangement = final_state
            best_weight = weight

    return best_value, best_arrangement, best_weight,weight_limit



def hillclimbing(initial_state):
    current_state = initial_state
    current_fitness = fitness_fun(current_state)

    while True:
        child_states = next_move(current_state)
        if not child_states:
            return current_state

        max_fitness = current_fitness
        max_state = current_state

        for child_state in child_states:
            child_fitness = fitness_fun(child_state)
            if child_fitness > max_fitness:
                max_fitness = child_fitness
                max_state = child_state

        if max_fitness <= current_fitness:
            return current_state

        current_state = max_state
        current_fitness = max_fitness



# num_restarts = random.randint(80, 1000)
# result = multiplerestart(num_restarts)
# print(result,weight_limit)
print(simulated_random_restart(100))
print(hill_random_restart(10))


##################################






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

def selection(population):
    fitness_values = [fitness_fun(individual) for individual in population]
    max_fitness = max(fitness_values)
    selected_individuals = random.choices(population, weights=fitness_values, k=2)
    return selected_individuals[0], selected_individuals[1]

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

def evolve(population):
    new_population = []
    while len(new_population) < population_size:
        parent1, parent2 = selection(population)
        child = crossover(parent1, parent2)
        mutated_child = mutate(child)
        new_population.append(mutated_child)
    return new_population

def genetic_algorithm():
    population = generate_initial_population()

    best_fitness = 0
    best_individual = None
    # best_generation = 0

    for generation in range(400):
        population = evolve(population)

        for individual in population:
            fitness = fitness_fun(individual)
            if fitness > best_fitness:
                best_fitness = fitness
                best_individual = individual
                # best_generation = generation + 1

    return best_fitness,best_individual  # best_generation

print(genetic_algorithm(),weight_limit)
