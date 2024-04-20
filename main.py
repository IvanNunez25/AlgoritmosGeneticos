import pygame
import random
import genetica

# Inicialización de pygame

# Definición de colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Definición del tamaño de la pantalla y otros parámetros
WIDTH, HEIGHT = 50, 50
SCREEN_SIZE = (WIDTH * 10 + 100, HEIGHT * 10)  # Aumentamos el ancho de la pantalla para mostrar la salud
SPECIAL_CELL_COUNT = 5
SPECIAL_CELL_POINTS = 5

# Clase para representar a un jugador
class Player:
    def __init__(self, redColor, greenColor, blueColor, color, controls, speed, attack, evasion, accuracy, health_regeneration, velocity_recolection, heal_by_damage, points_increase):
        self.redColor = redColor
        self.greenColor = greenColor
        self.blueColor = blueColor
        self.color = color
        self.controls = controls
        self.x = random.randint(0, WIDTH - 1)
        self.y = random.randint(0, HEIGHT - 1)
        self.score = 0
        self.speed = speed
        self.attack = attack
        self.evasion = evasion
        self.accuracy = accuracy
        self.health = 100
        self.max_health = 100
        self.health_regeneration = health_regeneration
        self.velocity_recolection = velocity_recolection
        self.heal_by_damage = heal_by_damage
        self.points_increase = points_increase
        self.is_alive = True

    def move(self, dx, dy):
        if self.is_alive:
            self.x += dx * self.speed
            self.y += dy * self.speed
            self.x = max(0, min(WIDTH - 1, self.x))
            self.y = max(0, min(HEIGHT - 1, self.y))

    def attack_enemy(self, enemy):
        if self.is_alive and enemy.is_alive:
            if random.random() < self.accuracy:
                enemy.health -= self.attack
                self.health += self.heal_by_damage
                self.health = min(self.health, self.max_health)
                if enemy.health <= 0:
                    enemy.is_alive = False
            else:
                print(f"{self.color} missed the attack!")

# Inicialización de jugadores
# player1_attributes = {
#     'color': GREEN,
#     'controls': {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d},
#     'speed': 1,
#     'attack': 10,
#     'evasion': 0.1,
#     'accuracy': 0.8,
#     'health_regeneration': 2,
#     'velocity_recolection': 1,
#     'heal_by_damage': 2,
#     'points_increase': 2
# }

# player2_attributes = {
#     'color': BLUE,
#     'controls': {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT},
#     'speed': 1,
#     'attack': 10,
#     'evasion': 0.1,
#     'accuracy': 0.8,
#     'health_regeneration': 2,
#     'velocity_recolection': 1,
#     'heal_by_damage': 2,
#     'points_increase': 2
# }

player1_attributes = genetica.personajeInicial()
player1_attributes['controls'] = {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d}

player2_attributes = genetica.personajeInicial()
player2_attributes['controls'] = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}

player1 = Player(**player1_attributes)
player2 = Player(**player2_attributes)


##################################LO NUEVOOO
players={player1,player2}


'''
lo de players es el conjunto pero para usarlo mas facil lo converti en lista
'''
players_list = list(players)

# Acceder al segundo jugador (player2)
# second_player = players_list[1]

for player in players_list:
    print("color: ", player.color)
    print("controles: ", player.controls)
    print("velocidad: ", player.speed)
    print('\n')


# Acceder a los atributos del segundo jugador
# print("Color del segundo jugador:", second_player.color)
# print("Controles del segundo jugador:", second_player.controls)
# print("Velocidad del segundo jugador:", second_player.speed)
##aqui se termina la muestraaaaaaaaaaaaaaaaaa




# Creación de las casillas especiales
special_cells = []
for _ in range(SPECIAL_CELL_COUNT):
    cell = {'position': (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)), 'points': SPECIAL_CELL_POINTS}
    special_cells.append(cell)

# Función para dibujar el mapa
def draw_map(screen):
    screen.fill(WHITE)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            color = player1.color if (x, y) == (player1.x, player1.y) else player2.color if (x, y) == (player2.x, player2.y) else WHITE
            pygame.draw.rect(screen, color, (x * 10, y * 10, 10, 10))
    for cell in special_cells:
        pygame.draw.rect(screen, (255, 165, 0), (cell['position'][0] * 10, cell['position'][1] * 10, 10, 10))

    # Dibujar la salud de los jugadores
    pygame.draw.rect(screen, GREEN, (WIDTH * 10 + 10, 10, 20, player1.health * 2))
    pygame.draw.rect(screen, RED, (WIDTH * 10 + 40, 10, 20, player2.health * 2))

# Función para manejar eventos
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    keys = pygame.key.get_pressed()
    if keys[player1.controls['up']]:
        player1.move(0, -1)
    if keys[player1.controls['down']]:
        player1.move(0, 1)
    if keys[player1.controls['left']]:
        player1.move(-1, 0)
    if keys[player1.controls['right']]:
        player1.move(1, 0)
    if keys[player2.controls['up']]:
        player2.move(0, -1)
    if keys[player2.controls['down']]:
        player2.move(0, 1)
    if keys[player2.controls['left']]:
        player2.move(-1, 0)
    if keys[player2.controls['right']]:
        player2.move(1, 0)

# Función para verificar colisiones y atacar
def check_collisions():
    if player1.x == player2.x and player1.y == player2.y:
        player1.attack_enemy(player2)
        player2.attack_enemy(player1)

# Función para verificar si un jugador está en una casilla especial
def check_special_cells(player):
    for cell in special_cells:
        if (player.x, player.y) == cell['position']:
            if player.is_alive:
                player.score += player.points_increase
                cell['points'] -= 1
                if cell['points'] == 0:
                    special_cells.remove(cell)

# Función principal del juego
def main():
    
    # pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_events()

        check_collisions()
        for player in players_list:
            check_special_cells(player)
        
        # check_special_cells(player2)

        # Regeneración de salud
        # player1.health = min(player1.health + player1.health_regeneration, player1.max_health)
        # player2.health = min(player2.health + player2.health_regeneration, player2.max_health)
        
        # Iterar sobre la lista de jugadores
        for player in players_list:
            # Incrementar la salud y asegurarse de que no supere la salud máxima
            player.health = min(player.health + player.health_regeneration, player.max_health)


        draw_map(screen)
        pygame.display.flip()
        clock.tick(10)

        # Verificar si ambos jugadores están "fuera de combate"
        # if not player1.is_alive and not player2.is_alive:
        #     running = False

        # Verificar si todos los jugadores están "fuera de combate"
        if all(not player.is_alive for player in players_list):
            running = False

        # Verificar si ya no quedan celdas especiales
        if not special_cells:
            running = False

    # Mostrar puntuación final y estado de los jugadores
    # print("Resultado:")
    # print(f"Jugador 1 (verde): {player1.score} puntos, {'Fuera de combate' if not player1.is_alive else 'Salud: ' + str(player1.health)}")
    # print(f"Jugador 2 (azul): {player2.score} puntos, {'Fuera de combate' if not player2.is_alive else 'Salud: ' + str(player2.health)}")
    
    


# if __name__ == "__main__":
#     main()

#
#
#
#
#
#
# !!!!! IMPORTANTE 
# Ajustar la ventana para que se repita cuando se acaban los objetivos -----

# while len(players_list) > 0:
#     main()        
    
#     pygame.init()
#     players_list.pop()
    
#     genetica.round(players_list)
    
#     for player in players_list:
#         player.is_alive = True
    
# pygame.quit()

genetica.round_genetica(players_list)