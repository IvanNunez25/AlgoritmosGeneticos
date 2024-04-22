import random
import bisect
import math

'''
GENES DE CADA JUGADOR

                redColor:   0 - 255
              greenColor:   0 - 255
               blueColor:   0 - 255
                   color:   (redColor, greenColor, blueColor)
                   speed:   1 - 5
                  attack:   10 - 50
                 evasion:   0.0 - 1.0
                accuracy:   0.0 - 1.0
     health_regeneration:   1 - 10
    velocity_recolection:   1 - 5
          heal_by_damage:   1 - 5
         points_increase:   1 - 5
'''

# Definición de los rangos de los genes para cada jugador
genes = [
    (0, 255),                   # redColor
    (0, 255),                   # greenColor
    (0, 255),                   # blueColor
    (1, 5),                     # speed
    (10, 50),                   # attack
    (0, 100),                   # evasion
    (0, 100),                   # accuracy
    (1, 10),                    # health_regeneration
    (1, 5),                     # velocity_recolection
    (1, 5),                     # heal_by_damage
    (1, 5)                      # points_increase
]

total_players = 0
total_genes = len(genes) 
round_value = 6
total_changes = 0
scores = []

# Función para generar un jugador inicial aleatorio
def personajeInicial():
    redColor = random.randint(0, 255)
    greenColor = random.randint(0, 255)
    blueColor = random.randint(0, 255)
    color = (redColor, greenColor, blueColor)

    player = {
        'redColor': redColor,
        'greenColor': greenColor,
        'blueColor': blueColor,
        'color': color,
        'speed': 1,
        'attack': 10,
        'evasion': 0.1,
        'accuracy': 0.8,
        'health_regeneration': 2,
        'velocity_recolection': 3,
        'heal_by_damage': 2,
        'points_increase': 2
    }
    
    return player

# Función para realizar una ronda de la evolución genética
def round_genetica(players_list):
    new_players_list = datos(players_list)
    
    fitness = fitness_function(players_list)
    total = round(sum(fitness), round_value)
    probability = probability_function(fitness, total)
    
    cumulative = [probability[0]]
    cumulative_function(cumulative, probability)
    
    reordered_players = reorderes_players_function(len(new_players_list), cumulative, new_players_list)
    
    cut_crossover = []
    positions = []
    
    cut_crossover_function(cut_crossover, positions, new_players_list)
    
    old_positions = positions.copy()
    if len(positions) > 0:
        aux = positions.pop(0)
        positions.append(aux)
        
    crossed_players = reordered_players.copy()
    
    crossed_players_function(crossed_players, positions, cut_crossover, old_positions, reordered_players)
    
    replace_positions = []
    replace_values = []
    
    replace_function(replace_positions, replace_values)
    replace_values_function(replace_positions, replace_values, crossed_players)
    
    speed = []
    for player in crossed_players:
        speed.append(player[3])
    print(speed)
    
    return crossed_players.copy()

# Convertir datos de jugadores en una lista de listas
def datos(players):
    players_list = []
    for player in players:
        player_row = []
        player_row.append(player.redColor)
        player_row.append(player.greenColor)
        player_row.append(player.blueColor)
        player_row.append(player.speed)
        player_row.append(player.attack)
        player_row.append(player.evasion)
        player_row.append(player.accuracy)
        player_row.append(player.health_regeneration)
        player_row.append(player.velocity_recolection)
        player_row.append(player.heal_by_damage)
        player_row.append(player.points_increase)
        scores.append(player.score)
        
        players_list.append(player_row)
        
    return players_list 

# Calcular la aptitud de cada jugador
def fitness_function(players):
    fitness = []
    for player in players:
        fx_i = player.score + 1
        if fx_i > 0:
            fitness.append(round(1 / fx_i, round_value))
        else:
            fitness.append(0)
    return fitness

# Calcular la probabilidad de selección de cada jugador
def probability_function(fitness, total):
    probability = []
    for fit in fitness:
        if total != 0:
            probability_i = round((fit / total), round_value)
            probability.append(probability_i)
    return probability

# Calcular las sumas acumulativas de probabilidades
def cumulative_function(cumulative, probability):
    for i in range(1, len(probability)):
        cumulative_i = round(probability[i] + cumulative[i-1], round_value)
        cumulative.append(cumulative_i)

# Reordenar los jugadores según la selección por ruleta
def reorderes_players_function(total_players, cumulative, players):
    reordered_players = []
    for i in range(0, total_players):
        random_number = random.randint(1, 999) / 1000
        reordered_players_i = bisect.bisect_right(cumulative, random_number)
        reordered_players.append(players[reordered_players_i])
    return reordered_players

# Seleccionar puntos de corte para el crossover
def cut_crossover_function(cut_crossover, positions, players):
    random_numbers = []
    for _ in players:
        random_numbers.append((random.randint(1, 999) / 1000 ))
    for rand in random_numbers:
        if rand <= 0.250:
            positions.append((random_numbers.index(rand)) + 1)
            cut_crossover.append(random.randint(1, total_genes - 1))

# Realizar el crossover
def crossed_players_function(crossed_players, positions, cut_crossover, old_positions, reordered_players):
    j = 0
    for position in positions:
        new_player = []
        for i in range(0, total_genes):
            if i < cut_crossover[j] and (old_positions[j] - 1) < len(reordered_players):
                new_player.append(reordered_players[old_positions[j] - 1][i])
            elif position - 1 < len(reordered_players):
                new_player.append(reordered_players[position - 1][i])
        if old_positions[j] - 1 < len(crossed_players):
            crossed_players[old_positions[j] - 1] = new_player
        j += 1            

# Seleccionar genes para la mutación
def replace_function(replace_positions, replace_values):
    total_changes = math.floor(0.01 * total_genes * total_players)
    for _ in range(0, total_changes):
        position = random.randint(0, total_genes * total_players)
        replace_positions.append(position)
        value = 0
        case = position % total_genes
        if case in [0, 1, 2]:
            value = random.randint(0, 255)
        elif case == 3:
            value = random.randint(1, 5)
        elif case == 4:
            value = random.randint(10, 50)
        elif case in [5, 6]:
            value = random.randint(1, 99) / 100
        elif case == 7:
            value = random.randint(1, 10)
        elif case in [8, 9, 10]:
            value = random.randint(1, 5)
        replace_values.append(value)
            
# Aplicar mutación a los jugadores
def replace_values_function(replace_positions, replace_values, crossed_players):
    i = 0
    for value in replace_values:
        ren = math.ceil(replace_positions[i] / total_genes)
        col = replace_positions[i] % total_genes
        i += 1
        
        if ren >= 1 and ren <= total_players:
            ren -= 1
        
        if col == 0:
            col = col + total_genes - 1
        else:
            col -= 1
        
        if value >= genes[col][0] and value <= genes[col][1]:
            crossed_players[ren][col] = value

