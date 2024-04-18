import pygame
import random

# Inicialización de pygame
pygame.init()

# Definición de colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Definición del tamaño de la pantalla y otros parámetros
WIDTH, HEIGHT = 50, 50
SCREEN_SIZE = (WIDTH * 10, HEIGHT * 10)
SPECIAL_CELL_COUNT = 5
SPECIAL_CELL_POINTS = 5

# Clase para representar a un jugador
class Player:
    def __init__(self, color, controls):
        self.color = color
        self.controls = controls
        self.x = random.randint(0, WIDTH - 1)
        self.y = random.randint(0, HEIGHT - 1)
        self.score = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = max(0, min(WIDTH - 1, self.x))
        self.y = max(0, min(HEIGHT - 1, self.y))

# Inicialización de jugadores
player1 = Player(GREEN, {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d})
player2 = Player(BLUE, {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT})

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

# Función para verificar si un jugador está en una casilla especial
def check_special_cells(player):
    for cell in special_cells:
        if (player.x, player.y) == cell['position']:
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

        check_special_cells(player1)
        check_special_cells(player2)

        draw_map(screen)
        pygame.display.flip()
        clock.tick(10)

        if not special_cells:
            running = False

    # Mostrar puntuación final
    print("Puntuación final:")
    print(f"Jugador 1 (verde): {player1.score} puntos")
    print(f"Jugador 2 (azul): {player2.score} puntos")

    pygame.quit()

if __name__ == "__main__":
    main()
