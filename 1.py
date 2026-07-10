import sys, math, random
input = sys.stdin.readline


# Index represents the following components

components = ['Alu', 'Cache', 'Control Unit', 'Register File', 'Decoder', 'Floating Unit']

# Each components in Index labeled and (w, h) of each

block_size = {
    0: (5, 5),
    1: (7, 4),
    2: (4, 4),
    3: (6, 6),
    4: (5, 3),
    5: (5, 5)
}


# Fitness Evaluation

def wiring_dist(chromosomes):
    center = get_center(chromosomes)
    dist = 0

    for src in range(len(graph)):
        for dst in graph[src]:
            if src < dst:
                x1, y1 = center[src]
                x2, y2 = center[dst]
                dist += (math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
    return dist

def bounding_box(chromosomes):
    x_c = []
    y_c = []

    for i, (x, y) in enumerate(chromosomes):
        w, h = block_size[i]
        x_c.extend([x, x+w])
        y_c.extend([y, y+h])
    
    area = (max(x_c) - min(x_c)) * (max(y_c) - min(y_c))

    return area

def no_overlaps(chromosomes):
    count = 0

    for i in range(len(chromosomes)):
        x1, y1 = chromosomes[i]
        w1, h1 = block_size[i]
        for j in range(i+1, len(chromosomes)):
            x2, y2 = chromosomes[j]
            w2, h2 = block_size[j]

            if not (
                (x1+w1 <= x2) or
                (x1 >= x2+w2) or
                (y1 >= y2+h2) or
                (y1+h1 <= y2)
            ):
                count += 1
    
    return count

def get_center(chromosomes):
    all_center = []

    for i, (x, y) in enumerate(chromosomes):
        w, h = block_size[i]
        center = (x + w//2, y + h//2)
        all_center.append(center)
    
    return all_center

def points(chromosomes):
    wiring = wiring_dist(chromosomes)
    bounding_box_area = bounding_box(chromosomes)
    overlaps = no_overlaps(chromosomes)

    return wiring, bounding_box_area, overlaps 

def fitness(chromosomes, alpha=1000, beta=2, gamma=1):
    wiring, area, overlaps = points(chromosomes)
    score = - ((alpha * overlaps) + (beta * wiring) + (gamma * area))

    return score


# Inputs

num_comp, g_w, g_h = map(int, input().split())
population = []

for _ in range(len(components)):
    co_ords = list(map(int, input().split()))
    chromosomes = [(co_ords[i], co_ords[i+1]) for i in range(0, len(co_ords), 2)]
    population.append(chromosomes)

# Connections

graph = [[] for _ in range(num_comp)]
graph[0].extend([1, 3, 2])  # ALU - Cache, Register File, Control Unit
graph[1].extend([4, 0])     # Cache - Decoder, ALU
graph[2].append(0)          # Control Unit - ALU
graph[3].extend([0, 5])     # Register File - ALU, Floating Unit
graph[4].extend([5, 1])     # Decoder - Floating Unit, Cache
graph[5].extend([4, 3])     # Floating Unit - Decoder, Register File

print(graph)
print()

# 6 25 25
# 9 3 12 15 13 16 1 13 4 15 9 6
# 8 0 7 12 4 11 1 13 14 10 9 11
# 6 5 12 9 9 7 8 6 2 7 3 1
# 3 11 11 12 14 11 6 10 3 11 3 0
# 10 12 8 16 10 4 13 6 6 0 3 7
# 0 2 0 0 14 12 4 5 12 4 3 10


# Genetic Operations

def cross_over(p1, p2):
    a1, a2 = p1[:len(p1)//2], p1[len(p1)//2:]
    b1, b2 = p2[:len(p2)//2], p2[len(p2)//2:]

    child1 = a1 + b2
    child2 = b1 + a2

    return child1, child2

def two_point_cross_over(p1, p2):
    a = random.randint(0, len(p1)-1)
    b = random.randint(a, len(p1)-1)

    x1, x2, x3 = p1[:a], p1[a:b], p1[b:]
    y1, y2, y3 = p2[:a], p2[a:b], p2[b:]

    child1 = x1 + y2 + x3
    child2 = y1 + x2 + y3

    return child1, child2


def mutation(chromosome, rate=0.075, g_w=25, g_h=25):
    if random.random() < rate:
        idx = random.randint(0, len(chromosome)-1)

        new_x = random.randint(0, g_w)
        new_y = random.randint(0, g_h)

        chromosome[idx] = (new_x, new_y)
    

def roulette_selection(population, fitness, k):
    all_fitness_scores = [fitness(x) for x in population]

    max_score = max(all_fitness_scores)
    weights = [(max_score - i + 1) for i in all_fitness_scores] # Making the scores positive 
    select = random.choices(population, weights=weights, k=k)

    return select


best_fitness = float('inf')
negative = 0
gen = 0
max_gen = 15
plateau = 5

while gen < max_gen and negative < plateau:
    all_fitness_scores = [fitness(x) for x in population] 
    current_best = max(all_fitness_scores)
    best_layout = population[all_fitness_scores.index(current_best)]

    if current_best > best_fitness:
        best_fitness = current_best 
        negative = 0
    
    else:
        negative += 1

    fitness_idx = list(enumerate(all_fitness_scores))
    sorted_fitness_pair = sorted(fitness_idx, key=lambda x: x[1])
    elite_idx = [idx for idx,_ in sorted_fitness_pair]

    elites = [population[i] for i in elite_idx[:2]]

    offsprings = []
    while len(offsprings) < len(population) * 3: # Oversampling for better roulette result, more variety
        parent1, parent2 = random.sample(population, 2)
        child1, child2 = cross_over(parent1, parent2)
        mutation(child1)
        mutation(child2)    
        offsprings.append(child1)
        offsprings.append(child2)       

    needed = len(population) - len(elites) # Here I am making it dynamic if the number of components '6' is not fixed
    remaining = roulette_selection(offsprings, fitness, k=needed)

    new_population = elites + remaining
    population = new_population
    gen += 1


wiring, area, overlaps = points(best_layout)

print("Single Point Crossover: \n")

for name, (x, y) in zip(components, best_layout):
    print(f"{name}: ({x}, {y})")

print(
    f"Total Wiring Distance: {wiring:.2f}\nBounding Box Area: {area}\nOverlap Count: {overlaps}\nBest Fitness Score: {fitness(best_layout)}"
)




best_fitness = float('inf')
negative = 0
gen = 0
max_gen = 15
plateau = 5

while gen < max_gen and negative < plateau:
    all_fitness_scores = [fitness(x) for x in population] 
    current_best = max(all_fitness_scores)
    best_layout = population[all_fitness_scores.index(current_best)]

    if current_best > best_fitness:
        best_fitness = current_best 
        negative = 0

    else:
        negative += 1

    fitness_idx = list(enumerate(all_fitness_scores))
    sorted_fitness_pair = sorted(fitness_idx, key=lambda x: x[1])
    elite_idx = [idx for idx,_ in sorted_fitness_pair]

    elites = [population[i] for i in elite_idx[:2]]

    offsprings = []
    while len(offsprings) < len(population) * 3: # Oversampling for better roulette result, more variety
        parent1, parent2 = random.sample(population, 2)
        child1, child2 = two_point_cross_over(parent1, parent2)
        mutation(child1)
        mutation(child2)    
        offsprings.append(child1)
        offsprings.append(child2)       

    needed = len(population) - len(elites) # Here I am making it dynamic if the number of components '6' is not fixed
    remaining = roulette_selection(offsprings, fitness, k=needed)

    new_population = elites + remaining
    population = new_population
    gen += 1

wiring, area, overlaps = points(best_layout)
print()
print("Two Point Crossover:\n")

for name, (x, y) in zip(components, best_layout):
    print(f"{name}: ({x}, {y})")

print(
    f"Total Wiring Distance: {wiring:.2f}\nBounding Box Area: {area}\nOverlap Count: {overlaps}\nBest Fitness Score: {fitness(best_layout)}"
)
