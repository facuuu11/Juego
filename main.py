import pygame
import os

pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey Kong Zigzag")
clock = pygame.time.Clock()
FPS = 60


WHITE = (255, 255, 255)
BROWN = (139, 69, 19)


salto_sound = pygame.mixer.Sound("salto.wav")


player_img = pygame.image.load(os.path.join("img", "player.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, (30, 40))

donkey_img = pygame.image.load(os.path.join("img", "donkey_kong.png")).convert_alpha()
donkey_img = pygame.transform.scale(donkey_img, (50, 50))

princess_img = pygame.image.load(os.path.join("img", "princess.png")).convert_alpha()
princess_img = pygame.transform.scale(princess_img, (30, 40))

barrel_img = pygame.image.load(os.path.join("img", "barrel.png")).convert_alpha()
barrel_img = pygame.transform.scale(barrel_img, (20, 20))


platforms = [
    pygame.Rect(150, 150, 500, 20),
    pygame.Rect(50, 300, 700, 20),
    pygame.Rect(100, 450, 600, 20),
    pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
]

platform_directions = [1, -1, 1, 0]


donkey_kong = pygame.Rect(150, 100, 50, 50)


princess = pygame.Rect(700, 100, 30, 40)


player = pygame.Rect(200, HEIGHT - 60, 30, 40)
player_vel_y = 0
is_jumping = False
GRAVITY = 1


class Barrel:
    def __init__(self):
        self.platform_index = 0
        plat = platforms[self.platform_index]
        self.rect = pygame.Rect(donkey_kong.centerx, plat.top - 20, 20, 20)
        self.direction = platform_directions[self.platform_index]
        self.falling = False
        self.vel_y = 0

    def update(self):
        if self.falling:
            self.vel_y += GRAVITY
            self.rect.y += self.vel_y

            if self.platform_index + 1 < len(platforms):
                next_plat = platforms[self.platform_index + 1]
                if self.rect.colliderect(next_plat) and self.vel_y >= 0:
                    self.rect.bottom = next_plat.top
                    self.platform_index += 1
                    self.direction = platform_directions[self.platform_index]
                    self.falling = False
                    self.vel_y = 0
        else:
            self.rect.x += 2 * self.direction
            plat = platforms[self.platform_index]
            if self.rect.right > plat.right or self.rect.left < plat.left:
                self.falling = True

    def draw(self, surface):
        surface.blit(barrel_img, self.rect.topleft)

barrels = []

SPAWN_BARREL = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_BARREL, 15000)


running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN_BARREL:
            barrels.append(Barrel())

    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_SPACE] and not is_jumping:
        player_vel_y = -15
        is_jumping = True
        salto_sound.play()

   
    player.x = max(0, min(WIDTH - player.width, player.x))

    
    player_vel_y += GRAVITY
    player.y += player_vel_y

    
    for plat in platforms:
        if player.colliderect(plat) and player_vel_y >= 0:
            player.bottom = plat.top
            is_jumping = False
            player_vel_y = 0

    
    for plat in platforms:
        pygame.draw.rect(screen, BROWN, plat)

    
    screen.blit(donkey_img, donkey_kong.topleft)
    screen.blit(princess_img, princess.topleft)
    screen.blit(player_img, player.topleft)

    
    for barrel in barrels[:]:
        barrel.update()
        barrel.draw(screen)

        if player.colliderect(barrel.rect):
            print("¡Perdiste!")
            running = False

        if barrel.rect.top > HEIGHT:
            barrels.remove(barrel)

   
    if player.colliderect(princess):
        print("¡Ganaste!")
        running = False

    pygame.display.flip()

pygame.quit()
