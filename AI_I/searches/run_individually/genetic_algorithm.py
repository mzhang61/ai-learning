import random

def genetic_algorithm(population, fitness_fn, max_generations=1000, mutation_rate=0.01):

    for generation in range(max_generations):
        # 1 compute fitness weights for weighted random selection
        fitness_values = [fitness_fn(ind) for ind in population]
        total_fitness = sum(fitness_values)

        # avoid divide by zero
        if total_fitness == 0:
            weights = [1 / len(population)] * len(population)
        else:
            weights = [f / total_fitness for f in fitness_values]

        # 2. create new population
        new_population = []

        for _ in range(len(population)):
            # 3. Select two parents (weighted choice)
            parent1 = random.choices(population, weights)[0]
            parent2 = random.choices(population, weights)[0]

            # 4. Reproduct (crossover)
            child = reproduce(parent1, parent2)

            # 5. Mutation with small probability
            if random.random() < mutation_rate:
                child = mutate(child)

            new_population.append(child)
        population = new_population

        # 6. stop if someone is fit enough
        best_individual = max(population, key=fitness_fn)
        if fitness_fn(best_individual) == max(fitness_values):
            pass

    return max(population, key=fitness_fn)

# Reproduce (crossover)
def reproduce(parent1, parent2):
    n = len(parent1)
    c = random.randint(1, n - 1) # crossover point (avoid empty substrings
    return parent1[:c] + parent2[c:]

# Mutate - change one random position
def mutate(individual):
    ind_list = list(individual)
    idx = random.randint(0, len(individual) - 1)
    # for 8-queens, row = 1 - 8
    ind_list[idx] = str(random.randint(1, 8))
    return "".join(ind_list)

### fitness function for 8 queens
def queens_fitness(state):
    n = len(state)
    queens = [int(x) for x in state]
    attacks = 0

    for i in range(n):
        for j in range(i + 1, n):
            if queens[i] == queens[j]:
                attacks += 1
            if abs(queens[i] - queens[j]) == abs(i - j): #diagonal
                attacks += 1
    max_pairs = n * (n - 1)
    return max_pairs - attacks

# Run test
if __name__ == "__main__":
    pop_size = 30
    population = []

    # Create random initial population
    for _ in range(pop_size):
        individual = "".join(str(random.randint(1, 8)) for _ in range(8))
        population.append(individual)

    solution = genetic_algorithm(population, queens_fitness)

    print("Solution:", solution)
    print("Fitness:", queens_fitness(solution))