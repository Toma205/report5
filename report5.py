import random

def initialize_population(population_size, n):
    """Initializes a population of random board configurations."""
    population = []
    for _ in range(population_size):
        # Each individual is a list representing column placement of queens for each row
        individual = random.sample(range(n), n)
        population.append(individual)
    return population

def calculate_fitness(individual):
    """Calculates the fitness of a board configuration (lower is better)."""
    n = len(individual)
    conflicts = 0
    # Check for row and diagonal conflicts
    for i in range(n):
        for j in range(i + 1, n):
            # Same column conflict
            if individual[i] == individual[j]:
                conflicts += 1
            # Diagonal conflicts
            elif abs(individual[i] - individual[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def selection(population, fitnesses):
    """Selects parents for the next generation using roulette wheel selection."""
    max_fitness = max(fitnesses)
    # Invert fitness so higher fitness is better for selection
    inverted_fitnesses = [max_fitness - f + 1 for f in fitnesses]
    total_fitness = sum(inverted_fitnesses)
    probabilities = [f / total_fitness for f in inverted_fitnesses]
    parents = random.choices(population, weights=probabilities, k=2)
    return parents

def crossover(parent1, parent2):
    """Performs crossover (single-point) to create two offspring."""
    n = len(parent1)
    crossover_point = random.randint(1, n - 1)
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    return offspring1, offspring2

def mutate(individual, mutation_rate):
    """Performs mutation by randomly changing the position of a queen."""
    n = len(individual)
    mutated_individual = list(individual)  # Create a copy
    if random.random() < mutation_rate:
        index1, index2 = random.sample(range(n), 2)
        mutated_individual[index1], mutated_individual[index2] = mutated_individual[index2], mutated_individual[index1]
    return mutated_individual

def genetic_algorithm(n, population_size=100, generations=500, mutation_rate=0.01):
    """Solves the N-Queens problem using a genetic algorithm."""
    population = initialize_population(population_size, n)

    for generation in range(generations):
        fitnesses = [calculate_fitness(individual) for individual in population]

        # Check if a solution is found
        if 0 in fitnesses:
            best_individual = population[fitnesses.index(0)]
            print(f"Solution found in generation {generation + 1}: {best_individual}")
            return best_individual

        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = selection(population, fitnesses)
            offspring1, offspring2 = crossover(parent1, parent2)
            new_population.append(mutate(offspring1, mutation_rate))
            new_population.append(mutate(offspring2, mutation_rate))

        population = new_population

        # Print the best fitness of the current generation (optional)
        best_fitness = min(fitnesses)
        print(f"Generation {generation + 1}, Best Fitness: {best_fitness}")

    print(f"Maximum generations reached. No optimal solution found.")
    best_fitness = min(fitnesses)
    best_individual = population[fitnesses.index(best_fitness)]
    print(f"Best solution found: {best_individual} with fitness: {best_fitness}")
    return best_individual

def print_board(solution):
    """Prints the N-Queens board configuration."""
    n = len(solution)
    for row in range(n):
        line = ""
        for col in range(n):
            if solution[row] == col:
                line += "Q "
            else:
                line += ". "
        print(line)

if __name__ == "__main__":
    n_queens = 8  # Change this to solve for a different board size
    solution = genetic_algorithm(n_queens)
    if solution:
        print("\nBoard Configuration:")
        print_board(solution)