import pygame
import random

pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey Kong Simple")
clock = pygame.time.Clock()
FPS = 60


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BARREL_COLOR = (128, 0, 0)


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


princess = pygame.Rect(700, 100, 30, 40)


class Barrel:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.direction = 1 
        self.falling = False
        self.vel_y = 0

    def update(self):
        if self.falling:
            self.vel_y += GRAVITY
            self.rect.y += self.vel_y
            
            for plat in platforms:
                if self.rect.colliderect(plat) and self.vel_y >= 0:
                    self.rect.bottom = plat.top
                    self.falling = False
                    self.vel_y = 0
                    self.direction *= -1  
        else:
            self.rect.x += 2 * self.direction
            
            under_platform = None
            for plat in platforms:
                if plat.collidepoint(self.rect.midbottom):
                    under_platform = plat
                    break
            if not under_platform:
                self.falling = True

    def draw(self, screen):
        pygame.draw.ellipse(screen, BARREL_COLOR, self.rect)


barrels = []


SPAWN_BARREL = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_BARREL, 2000)


running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN_BARREL:
            barrels.append(Barrel(50, 130))

    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5

    
    player.x = max(0, min(WIDTH - player.width, player.x))

    
    if keys[pygame.K_SPACE] and not is_jumping:
        player_vel_y = -15
        is_jumping = True

    
    player_vel_y += GRAVITY
    player.y += player_vel_y

    
    for plat in platforms:
        if player.colliderect(plat) and player_vel_y >= 0:
            player.bottom = plat.top
            is_jumping = False
            player_vel_y = 0

    
    for plat in platforms:
        pygame.draw.rect(screen, BROWN, plat)

    
    pygame.draw.rect(screen, RED, princess)

    
    pygame.draw.rect(screen, BLUE, player)

    
    for barrel in barrels[:]:
        barrel.update()
        barrel.draw(screen)

        if barrel.rect.top > HEIGHT:
            barrels.remove(barrel)

        if player.colliderect(barrel.rect):
            print("¡Perdiste!")
            running = False

    if player.colliderect(princess):
        print("¡Ganaste!")
        running = False

    pygame.display.flip()

pygame.quit()
