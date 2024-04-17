import random
import bisect
import math

# Función: f(x) = (a + 2b + 3c + 4d) - 30

chromosomes = [[12, 5, 23, 8], 
              [2, 21, 18, 3],
              [10, 4, 13, 14],
              [20, 1, 10, 6],
              [1, 4, 13, 19],
              [20, 5, 17, 1]]

round_value = 9
number_chromosomes = 6
number_genes = 4

for i in range(1):

    fx = []
    fitness = []    

    for chromosome in chromosomes:
        fx_i = round(((chromosome[0] + (2 * chromosome[1]) + (3 * chromosome[2]) + (4 * chromosome[3])) - 30), round_value)
        fx.append(fx_i)

        fitness_i = round((1 / (1 + fx_i)), round_value)
        fitness.append(fitness_i)

    total = sum(fitness)
    probability = []
    cumulative = []

    for fitness_chromosome in fitness:
        probability_i = round((fitness_chromosome / total), round_value)
        probability.append(probability_i)
    
    cumulative.append(probability[0])
    i = 0

    for i in range(1, len(probability)):
        cumulative_i = round(probability[i] + cumulative[i-1], round_value)
        cumulative.append(cumulative_i)

    reordered_chromosomes = []
    
    # Sustituir por números realmente randoms
    #random_numbers = [0.201, 0.284, 0.099, 0.822, 0.398, 0.501]
    random_numbers = []

    for i in range (0, number_chromosomes):
    #for random_number in random_numbers:
        random_number = random.randint(1, 1000) / 1000
        reordered_chromosomes_i = bisect.bisect_right(cumulative, random_number)
        reordered_chromosomes.append(chromosomes[reordered_chromosomes_i])
    

    # Volver a sustituir por numeros random
    #random_numbers = [0.191, 0.259, 0.760, 0.006, 0.159, 0.340]
    random_numbers = []

    for _ in range(1, number_chromosomes):
        random_numbers.append(random.randint(1, 1000) / 1000)

    cut_crossover = []
    positions = []

    # Random 
    #prueba = [1, 1, 2]
    #i = 0

    for random_number in random_numbers:
        if random_number < 0.250:
            positions.append((random_numbers.index(random_number)) + 1)
            cut_crossover.append(random.randint(1, number_chromosomes - 1))
            #i += 1
    
    old_positions = positions.copy()

    if len(positions) > 0:
        aux = positions.pop(0)
        positions.append(aux)

    crossed_chromosomes = reordered_chromosomes.copy()
    j = 0

    for position in positions:
        new_line = []
        for i in range(0, number_genes):
            if i < cut_crossover[j]:
                new_line.append(reordered_chromosomes[old_positions[j] - 1][i])
            else:
                new_line.append(reordered_chromosomes[position - 1][i])
            
        crossed_chromosomes[old_positions[j] - 1] = new_line
        j += 1

    # random
    #replace_positions = [12, 18]
    #replace_values = [2, 5]

    replace_positions = []
    replace_values = []

    
    for i in range(1, 2):
        replace_positions.append(random.randint(1, 24))
        replace_values.append(random.randint(1, 30))
    
    i = 0
    for value in replace_values:
        ren = math.ceil(replace_positions[i] / number_genes)
        col = replace_positions[i] % number_genes
        i += 1

        if ren >= 1:
            ren -= 1

        if col == 0:
            col = 3
        else:
            col -= 1

        crossed_chromosomes[ren][col] = value

    chromosomes = crossed_chromosomes.copy()
    print(crossed_chromosomes)
