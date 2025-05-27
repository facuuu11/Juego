import pygame
import random

# Inicializar pygame
pygame.init()

# Dimensiones
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)

# Pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey Kong Simple")
clock = pygame.time.Clock()

# Jugador
player = pygame.Rect(100, HEIGHT - 60, 30, 40)
player_vel_y = 0
is_jumping = False
GRAVITY = 1

# Plataformas
platforms = [
    pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
    pygame.Rect(100, 450, 600, 20),
    pygame.Rect(50, 300, 700, 20),
    pygame.Rect(150, 150, 500, 20),
]

# Barriles
barrels = []

# Princesa
princess = pygame.Rect(700, 100, 30, 40)

# Función para crear barriles
def spawn_barrel():
    barrels.append(pygame.Rect(50, 140, 20, 20))

# Reloj para barriles
barrel_timer = pygame.USEREVENT + 1
pygame.time.set_timer(barrel_timer, 2000)

# Bucle principal
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == barrel_timer:
            spawn_barrel()

    # Movimiento
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        player_vel_y = -15

    # Saltar y gravedad
    player_vel_y += GRAVITY
    player.y += player_vel_y

    # Colisión con plataformas
    for plat in platforms:
        if player.colliderect(plat) and player_vel_y >= 0:
            player.bottom = plat.top
            is_jumping = False
            player_vel_y = 0

    # Dibujar plataformas
    for plat in platforms:
        pygame.draw.rect(screen, BROWN, plat)

    # Dibujar jugador
    pygame.draw.rect(screen, BLUE, player)

    # Dibujar princesa
    pygame.draw.rect(screen, RED, princess)

    # Dibujar y mover barriles
    for barrel in barrels[:]:
        barrel.x += 3
        if barrel.x > WIDTH:
            barrels.remove(barrel)
        pygame.draw.ellipse(screen, (128, 0, 0), barrel)

        if player.colliderect(barrel):
            print("¡Perdiste!")
            running = False

    # Ganar
    if player.colliderect(princess):
        print("¡Ganaste!")
        running = False

    pygame.display.flip()

pygame.quit()
