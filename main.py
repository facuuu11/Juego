import pygame
import random


pygame.init()


WIDTH, HEIGHT = 800, 600
FPS = 60


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey Kong Simple")
clock = pygame.time.Clock()


player = pygame.Rect(100, HEIGHT - 60, 30, 40)
player_vel_y = 0
is_jumping = False
GRAVITY = 1


platforms = [
    pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
    pygame.Rect(100, 450, 600, 20),
    pygame.Rect(50, 300, 700, 20),
    pygame.Rect(150, 150, 500, 20),
]


barrels = []


princess = pygame.Rect(700, 100, 30, 40)


def spawn_barrel():
    barrels.append(pygame.Rect(50, 140, 20, 20))


barrel_timer = pygame.USEREVENT + 1
pygame.time.set_timer(barrel_timer, 2000)


running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == barrel_timer:
            spawn_barrel()

    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        player_vel_y = -15

    
    player_vel_y += GRAVITY
    player.y += player_vel_y

 
    for plat in platforms:
        if player.colliderect(plat) and player_vel_y >= 0:
            player.bottom = plat.top
            is_jumping = False
            player_vel_y = 0


    for plat in platforms:
        pygame.draw.rect(screen, BROWN, plat)

 
    pygame.draw.rect(screen, BLUE, player)

 
    pygame.draw.rect(screen, RED, princess)

    
    for barrel in barrels[:]:
        barrel.x += 3
        if barrel.x > WIDTH:
            barrels.remove(barrel)
        pygame.draw.ellipse(screen, (128, 0, 0), barrel)

        if player.colliderect(barrel):
            print("¡Perdiste!")
            running = False

    
    if player.colliderect(princess):
        print("¡Ganaste!")
        running = False

    pygame.display.flip()

pygame.quit()
