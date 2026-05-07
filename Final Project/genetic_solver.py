import time
import random

def solve_genetic(items, bin_capacity, pop_size=50, generations=100, mutation_rate=0.1):
    def first_fit(chromosome):
        bins = []
        for item in chromosome:
            placed = False
            for b in bins:
                if sum(b) + item <= bin_capacity:
                    b.append(item)
                    placed = True
                    break
            if not placed:
                bins.append([item])
        return bins

    def calculate_fitness(bins):
        fitness = 0
        for b in bins:
            fitness += ((sum(b) / bin_capacity) ** 2)
        return fitness / len(bins)

    def create_population():
        population = []
        for _ in range(pop_size):
            shuffled = items.copy()
            random.shuffle(shuffled)
            population.append(shuffled)
        return population

    def crossover(parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        child = [-1] * size
        child[start:end] = parent1[start:end]
        
        remaining_items = parent2.copy()
        for item in child[start:end]:
            remaining_items.remove(item)
            
        rem_idx = 0
        for i in range(size):
            if child[i] == -1:
                child[i] = remaining_items[rem_idx]
                rem_idx += 1
        return child

    def mutate(chromosome):
        if random.random() < mutation_rate:
            idx1, idx2 = random.sample(range(len(chromosome)), 2)
            chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
        return chromosome

    start_time = time.time()
    
    population = create_population()
    best_overall_fitness = 0
    best_overall_bins = []
    
    for gen in range(generations):
        fitnesses = [calculate_fitness(first_fit(chrom)) for chrom in population]
        
        current_best_idx = fitnesses.index(max(fitnesses))
        if fitnesses[current_best_idx] > best_overall_fitness:
            best_overall_fitness = fitnesses[current_best_idx]
            best_overall_bins = first_fit(population[current_best_idx])
        
        new_population = []
        for _ in range(pop_size // 2):
            selected_indices1 = random.sample(range(pop_size), 3)
            p1 = population[max(selected_indices1, key=lambda i: fitnesses[i])]
            
            selected_indices2 = random.sample(range(pop_size), 3)
            p2 = population[max(selected_indices2, key=lambda i: fitnesses[i])]
            
            new_population.extend([mutate(crossover(p1, p2)), mutate(crossover(p2, p1))])
            
        population = new_population
        
    end_time = time.time()
    
    return best_overall_bins, (end_time - start_time)