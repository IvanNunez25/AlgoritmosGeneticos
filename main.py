import pygame
import random
import genetica
import time

# Inicialización de pygame
pygame.init()

# Definición de colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Definición del tamaño de la pantalla y otros parámetros
WIDTH, HEIGHT = 50, 50
TEXT_WIDTH = 200  # Ancho para los textos
SCREEN_SIZE = (WIDTH * 10 + TEXT_WIDTH, HEIGHT * 10)
SPECIAL_CELL_COUNT = 10
SPECIAL_CELL_POINTS = 1

number_players = 40
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
        self.path = []

    def move(self, dx, dy):
        if self.is_alive:
            self.x += dx * self.speed
            self.y += dy * self.speed
            self.x = max(0, min(WIDTH - 1, self.x))
            self.y = max(0, min(HEIGHT - 1, self.y))

    def step(self):
        # Mueve al azar en una dirección
        move_direction = random.randint(0, 3)
        if move_direction == 0:
            self.move(0, -1)
        elif move_direction == 1:
            self.move(0, 1)
        elif move_direction == 2:
            self.move(-1, 0)
        elif move_direction == 3:
            self.move(1, 0)

    def attack_enemy(self, enemy):
        if self.is_alive and enemy.is_alive:
            if random.random() < self.accuracy:
                enemy.health -= self.attack
                self.health += self.heal_by_damage
                self.health = min(self.health, self.max_health)
                if enemy.health <= 0:
                    enemy.is_alive = False

# Inicialización de jugadores
players_list = []
for _ in range(number_players):  # Aquí puedes cambiar el número de jugadores
    player_attributes = genetica.personajeInicial()
    controls = {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d} if len(players_list) == 0 else {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}
    player_attributes['controls'] = controls
    player = Player(**player_attributes)
    players_list.append(player)

# Creación de las casillas especiales
def casillas_especiales():
    for _ in range(SPECIAL_CELL_COUNT):
        cell = {'position': (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)), 'points': SPECIAL_CELL_POINTS}
        special_cells.append(cell)

special_cells = []
casillas_especiales()

# Función para dibujar el mapa
def draw_map(screen, players_alive, special_cells_left, generations_passed):
    screen.fill(WHITE)
    
    # Dibujar campo de juego
    for x in range(WIDTH):
        for y in range(HEIGHT):
            color = WHITE
            for player in players_list:
                if (x, y) == (player.x, player.y) and player.is_alive:
                    color = player.color
            pygame.draw.rect(screen, color, (x * 10, y * 10, 10, 10))
            
    
    for cell in special_cells:
        pygame.draw.rect(screen, (255, 165, 0), (cell['position'][0] * 10, cell['position'][1] * 10, 10, 10))


    # Dibujar línea vertical divisoria
    pygame.draw.line(screen, BLACK, ((WIDTH * 10), 0), ((WIDTH * 10), SCREEN_SIZE[1]), 2)

    # Dibujar contadores
    font = pygame.font.SysFont(None, 24)
    players_alive_text = font.render("Jugadores vivos: {}".format(players_alive), True, BLACK)
    special_cells_text = font.render("Madera faltante: {}".format(special_cells_left), True, BLACK)
    generations_text = font.render("Nro de Generaciones: {}".format(generations_passed), True, BLACK)
    screen.blit(players_alive_text, (WIDTH * 10 + 10, 10))
    screen.blit(special_cells_text, (WIDTH * 10 + 10, 40))
    screen.blit(generations_text, (WIDTH * 10 + 10, 70))

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
                cell['points'] -= player.velocity_recolection
                if cell['points'] <= 0:
                    special_cells.remove(cell)

# Función principal del juego
def main():
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    running = True
    generations_passed = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_events()

        check_collisions()

        for player in players_list:
            player.step()
            check_special_cells(player)

        for player in players_list:
            player.health = min(player.health + player.health_regeneration, player.max_health)

        draw_map(screen, count_players_alive(), len(special_cells), generations_passed)
        pygame.display.flip()
        clock.tick(30)

        # Verificar si todos los jugadores están "fuera de combate"
        if all(not player.is_alive for player in players_list):
            running = False

        # Verificar si ya no quedan celdas especiales
        if not special_cells:
            time.sleep(3)
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

            generations_passed += 1

    pygame.quit()

def count_players_alive():
    count = 0
    for player in players_list:
        if player.is_alive:
            count += 1
    return count

if __name__ == "__main__":
    main()
