import random
import bisect

# Función: f(x) = (a + 2b + 3c + 4d) - 30

chromosomes = [[12, 5, 23, 8], 
              [2, 21, 18, 3],
              [10, 4, 13, 14],
              [20, 1, 10, 6],
              [1, 4, 13, 19],
              [20, 5, 17, 1]]

round_value = 9
number_chromosomes = 6

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
    random_numbers = [0.201, 0.284, 0.099, 0.822, 0.398, 0.501]

    #for _ in range (1, number_chromosomes):
    for random_number in random_numbers:
        #random_number = random.randint(1, 1000) / 1000
        reordered_chromosomes_i = bisect.bisect_right(cumulative, random_number)
        reordered_chromosomes.append(chromosomes[reordered_chromosomes_i])
    
    # Volver a sustituir por numeros random
    random_numbers = [0.191, 0.259, 0.760, 0.006, 0.159, 0.340]
    
    # Tengo varias preguntas, hasta aquí le voy dejar


    print(reordered_chromosomes)
