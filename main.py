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

number_players = 10
genetica.total_players = number_players

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
players_list = []
for _ in range(number_players):  # Aquí puedes cambiar el número de jugadores
    player_attributes = genetica.personajeInicial()
    controls = {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d} if len(players_list) == 0 else {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}
    player_attributes['controls'] = controls
    player = Player(**player_attributes)
    players_list.append(player)

for player in players_list:
    print("color: ", player.color)
    print("controles: ", player.controls)
    print("velocidad: ", player.speed)
    print('\n')



# Creación de las casillas especiales
def casillas_especiales():
    for _ in range(SPECIAL_CELL_COUNT):
        cell = {'position': (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)), 'points': SPECIAL_CELL_POINTS}
        special_cells.append(cell)

special_cells = []
casillas_especiales()


# Función para dibujar el mapa
def draw_map(screen):
    screen.fill(WHITE)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            color = WHITE
            for player in players_list:
                if (x, y) == (player.x, player.y) and player.is_alive:
                    color = player.color
            pygame.draw.rect(screen, color, (x * 10, y * 10, 10, 10))
    for cell in special_cells:
        pygame.draw.rect(screen, (255, 165, 0), (cell['position'][0] * 10, cell['position'][1] * 10, 10, 10))

    # Dibujar la salud de los jugadores
    for i, player in enumerate(players_list):
        if player.is_alive:
            health_color = GREEN if i == 0 else RED
            pygame.draw.rect(screen, health_color, (WIDTH * 10 + 10 + i * 30, 10, 20, player.health * 2))


# Función para manejar eventos
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    keys = pygame.key.get_pressed()
    for player in players_list:
        if keys[player.controls['up']]:
            player.move(0, -1)
        if keys[player.controls['down']]:
            player.move(0, 1)
        if keys[player.controls['left']]:
            player.move(-1, 0)
        if keys[player.controls['right']]:
            player.move(1, 0)
            

# Función para verificar colisiones y atacar
def check_collisions():
    for i, player in enumerate(players_list):
        if player.is_alive:
            for other_player in players_list[i + 1:]:
                if other_player.is_alive and player.x == other_player.x and player.y == other_player.y:
                    player.attack_enemy(other_player)
                    other_player.attack_enemy(player)

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
        
        for player in players_list:
            player.health = min(player.health + player.health_regeneration, player.max_health)

        draw_map(screen)
        pygame.display.flip()
        clock.tick(10)

        # Verificar si todos los jugadores están "fuera de combate"
        if all(not player.is_alive for player in players_list):
            running = False

        # Verificar si ya no quedan celdas especiales
        if not special_cells:
            # running = False
            datos = genetica.round_genetica(players_list)
            for i in range(0, len(players_list)):     
                players_list[i].redColor = datos[i][0]
                players_list[i].greenColor = datos[i][1]
                players_list[i].blueColor = datos[i][2]
                players_list[i].color = (datos[i][0], datos[i][1], datos[i][2])
                players_list[i].speed = datos[i][3]
                players_list[i].attack = datos[i][4]
                players_list[i].evasion = datos[i][5]
                players_list[i].accuracy = datos[i][6]
                players_list[i].health_regeneration = datos[i][7]
                players_list[i].velocity_recolection = datos[i][8]
                players_list[i].heal_by_damage = datos[i][9]
                players_list[i].points_increase = datos[i][10]
                
            casillas_especiales()

    
    

    pygame.quit()
    


if __name__ == "__main__":
     main()

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

#genetica.round_genetica(players_list)