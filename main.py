import pygame
import random

# Inicialización de pygame
pygame.init()

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
    def __init__(self, color, controls, attack,health):
        self.color = color
        self.controls = controls
        self.x = random.randint(0, WIDTH - 1)
        self.y = random.randint(0, HEIGHT - 1)
        self.score = 0
        self.attack = attack
        self.health = health
        self.is_alive = True

    def move(self, dx, dy):
        if self.is_alive:
            self.x += dx
            self.y += dy
            self.x = max(0, min(WIDTH - 1, self.x))
            self.y = max(0, min(HEIGHT - 1, self.y))

# Inicialización de jugadores
attack1=15
attack2=10
health1=100
health2=200

player1 = Player(GREEN, {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d},attack1, health1)
player2 = Player(BLUE, {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}, attack2, health2)

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
            color = GREEN if (x, y) == (player1.x, player1.y) else BLUE if (x, y) == (player2.x, player2.y) else WHITE
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
        if player1.is_alive and player2.is_alive:
            player1.health -= player2.attack
            player2.health -= player1.attack
        if player1.health <= 0:
            player1.is_alive = False
        if player2.health <= 0:
            player2.is_alive = False

# Función para verificar si un jugador está en una casilla especial
def check_special_cells(player):
    for cell in special_cells:
        if (player.x, player.y) == cell['position']:
            if player.is_alive:
                player.score += 1
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
        check_special_cells(player1)
        check_special_cells(player2)

        draw_map(screen)
        pygame.display.flip()
        clock.tick(10)

        # Verificar si ambos jugadores están "fuera de combate"
        if not player1.is_alive and not player2.is_alive:
            running = False

        # Verificar si ya no quedan celdas especiales
        if not special_cells:
            running = False

    # Mostrar puntuación final y estado de los jugadores
    print("Resultado:")
    print(f"Jugador 1 (verde): {player1.score} puntos, {'Fuera de combate' if not player1.is_alive else 'Salud: ' + str(player1.health)}")
    print(f"Jugador 2 (azul): {player2.score} puntos, {'Fuera de combate' if not player2.is_alive else 'Salud: ' + str(player2.health)}")

    pygame.quit()

if __name__ == "__main__":
    main()
