import pygame
from assets import load_assets
from config import FPS, ALT, LARG

pygame.init()


window = pygame.display.set_mode((LARG,ALT))
pygame.display.set_caption('Máfia 5')
rect = pygame.Rect
# blocos para haver colisão
blocos_horizont = [rect(0,440, 335, 10),rect(195,590,150,10),rect(94,729,360,10),rect(445,630,430,10),rect(880,530,210,10),rect(1090,630,300,10),rect(1350,530,60,10),rect(1405,440,350,10),rect(1750,490,340,10),rect(2090,630,200,10)] 
blocos_vert = [rect(440,650,10,100),rect(875,530,10,100),rect(1090,535,10,100),rect(1350,530,10,100),rect(1400,445,10,100),rect(1750,440,10,60),rect(2090,500,10,150),rect(2280,630,10,200)]
# carregar assets
assets = load_assets()
STILL = 0
WALK = 1
WALK_BACK = 2
SHOT = 3
# Classe plataforma
class Platform(pygame.sprite.Sprite):
    def __init__(self,position,size):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.mask = pygame.mask.Mask(size, True)

platforms_horizont = []
for bloco in blocos_horizont:
    platforms_horizont.append(Platform((bloco.x, bloco.y), (bloco.width, bloco.height)))
platforms_vert = []
for bloco in blocos_vert:
    platforms_vert.append(Platform((bloco.x, bloco.y), (bloco.width, bloco.height)))

# Classe jogador
class Player(pygame.sprite.Sprite):
    def __init__(self,assets):
        pygame.sprite.Sprite.__init__(self)

        
        self.animations = {
            STILL: assets['personagem'][0:7],
            WALK: assets['andar'][0:10],
            WALK_BACK: assets['andar'][0:9],
            SHOT: assets['atira'][1:3]
        }
        
        
        self.state = STILL
        # Define animação atual
        self.animation = self.animations[self.state]
        # Inicializa o primeiro quadro da animação
        self.frame = 0
        self.image = self.animation[self.frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()
        self.rect.centerx = 240
        self.rect.bottom = 35
        self.speedx = 0
        self.speedy = 6
        self.assets = assets
        
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 200
 
    
    def update(self):
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:

            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1

            # Atualiza animação atual
            self.animation = self.animations[self.state]
            
            # Reinicia a animação caso o índice da imagem atual seja inválido
            if self.frame >= len(self.animation):
                self.frame = 0
            
            # Armazena a posição do centro da imagem
            center = self.rect.center
            # Atualiza imagem atual
            self.image = self.animation[self.frame]
            # Atualiza os detalhes de posicionamento
            self.rect = self.image.get_rect()
            self.rect.center = center
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > larg_fundo :
            self.rect.right = larg_fundo
        if self.rect.left < -60:
            self.rect.left = -60
        if self.rect.top < -70:
            self.rect.top = -70
        if self.rect.bottom > alt_fundo - self.rect.height:
            self.rect.bottom = alt_fundo - self.rect.height

player = Player(assets)


    
    
larg_fundo = assets['fundo'].get_width()
alt_fundo = assets['fundo'].get_height()

game = True
camera_x = 0
camera_y = 0
# Loop principal do jogo
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
            
        if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_d:
                player.speedx += 4
                player.state = WALK
            if event.key == pygame.K_a:
                player.speedx -= 4
                player.state = WALK_BACK
            if event.key == pygame.K_w:
                player.speedy -= 14
            if event.key == pygame.K_s:
                player.speedy += 4
            if event.key == pygame.K_SPACE:
                player.state = SHOT
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_d:
                player.speedx -= 4
                player.state = STILL
            if event.key == pygame.K_a:
                player.speedx += 4
                player.state = STILL
            if event.key == pygame.K_w:
                player.speedy += 14
            if event.key == pygame.K_s:
                player.speedy -= 4
            if event.key == pygame.K_SPACE:
                player.speedy = STILL   
    
    # posiciona a camera
    camera_x = player.rect.centerx - LARG // 2
    camera_y = player.rect.centery - ALT // 2
    
    
        
    

    # limita a camera 
    camera_x = max(0, min(camera_x, larg_fundo - LARG)) 
    camera_y = max(0, min(camera_y, alt_fundo - ALT))

    
    
    # Atualiza tela
    window.fill((255, 255, 255))  
    window.blit(assets['fundo'],(-camera_x,-camera_y)) # atualiza o fundo
    pygame.draw.rect(window, (0,0,0), player.rect.move(-camera_x,-camera_y))
    window.blit(player.image, (player.rect.x - camera_x, player.rect.y - camera_y)) # atualiza o jogador
    player.update()
    
    
        
    
    # Colisão entre player e bloco
    for bloco in platforms_horizont:
        if pygame.sprite.collide_mask(player, bloco):
            if player.speedy > 0:
                player.rect.y -= player.speedy
            
    for bloco in platforms_vert:
        if pygame.sprite.collide_mask(player, bloco):
            # if player.speedx > 0:
            player.rect.right -= player.speedx
            if player.speedy > 0:
                player.rect.y -= player.speedy
            # if player.speedx < 0:
                # player.rect.left = bloco.rect.right - 70
    
    # Desenha as plataformas para ver durante o desenvolvimento
    for bloco in blocos_horizont:
        pygame.draw.rect(window, (0, 255, 0), bloco.move(-camera_x,-camera_y))
    for bloco in blocos_vert:
        pygame.draw.rect(window, (0, 255, 0), bloco.move(-camera_x,-camera_y))
    
    

    pygame.display.flip()  # Atualiza a tela
    pygame.time.Clock().tick(FPS) 

pygame.quit()