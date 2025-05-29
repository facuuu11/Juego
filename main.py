import pygame
import sys

pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey Kong Zigzag")
clock = pygame.time.Clock()
FPS = 60


WHITE = (255, 255, 255)
BROWN = (139, 69, 19)


player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (40, 50))
donkey_img1 = pygame.image.load("donkey.png")
donkey_img2 = pygame.transform.flip(donkey_img1, True, False)  
princess_img = pygame.image.load("princess.png")
princess_img = pygame.transform.scale(princess_img, (30, 40))
barrel_img = pygame.image.load("barrel.png")
barrel_img = pygame.transform.scale(barrel_img, (25, 25))
salto_sonido = pygame.mixer.Sound("salto.wav")


platforms = [
    pygame.Rect(150, 150, 500, 20),
    pygame.Rect(50, 300, 700, 20),
    pygame.Rect(100, 450, 600, 20),
    pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
]
platform_directions = [1, -1, 1, 0]


donkey_rect = pygame.Rect(150, 100, 50, 50)
princess_rect = pygame.Rect(700, 100, 30, 40)
player = pygame.Rect(200, HEIGHT - 60, 30, 40)
player_vel_y = 0
is_jumping = False
GRAVITY = 0.8


puntos = 0
font = pygame.font.SysFont("Arial", 30)


donkey_timer = 0
donkey_frame = 0

class Barrel:
    def __init__(self):
        self.platform_index = 0
        plat = platforms[self.platform_index]
        self.rect = barrel_img.get_rect(midbottom=(donkey_rect.centerx, plat.top))
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
        surface.blit(barrel_img, self.rect)

barrels = []
SPAWN_BARREL = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_BARREL, 4000)


def mostrar_pantalla_inicio():
    screen.fill(WHITE)
    titulo = font.render("Donkey Kong Zigzag", True, (0,0,0))
    instruccion = font.render("Presiona ESPACIO para comenzar", True, (0,0,0))
    screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, HEIGHT//2 - 50))
    screen.blit(instruccion, (WIDTH//2 - instruccion.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    esperando = False

mostrar_pantalla_inicio()


running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN_BARREL:
            barrels.append(Barrel())

    
    donkey_timer += 1
    if donkey_timer % 30 == 0:
        donkey_frame = 1 - donkey_frame
    donkey_img = donkey_img1 if donkey_frame == 0 else donkey_img2

   
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_SPACE] and not is_jumping:
        player_vel_y = -15
        is_jumping = True
        salto_sonido.play()

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

    
    screen.blit(donkey_img, donkey_rect)
    screen.blit(princess_img, princess_rect)
    screen.blit(player_img, player)

   
    for barrel in barrels[:]:
        barrel.update()
        barrel.draw(screen)
        if player.colliderect(barrel.rect):
            print("¡Perdiste!")
            running = False
        if barrel.rect.top > HEIGHT:
            barrels.remove(barrel)

   
    if player.colliderect(princess_rect):
        puntos += 100
        print("¡Ganaste!")
        running = False

    
    puntos_texto = font.render(f"Puntos: {puntos}", True, (0,0,0))
    screen.blit(puntos_texto, (10,10))

    pygame.display.flip()

pygame.quit()
