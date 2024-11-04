import pygame


    
def load_spritesheet(spritesheet, rows, columns):
    # Calcula a largura e altura de cada sprite.
    sprite_width = spritesheet.get_width() // columns
    sprite_height = spritesheet.get_height() // rows
    
    # Percorre todos os sprites adicionando em uma lista.
    sprites = []
    for row in range(rows):
        for column in range(columns):
            # Calcula posição do sprite atual
            x = column * sprite_width
            y = row * sprite_height
            # Define o retângulo que contém o sprite atual
            dest_rect = pygame.Rect(x, y, sprite_width, sprite_height)

            # Cria uma imagem vazia do tamanho do sprite
            image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            # Copia o sprite atual (do spritesheet) na imagem
            image.blit(spritesheet, (0, 0), dest_rect)
            sprites.append(image)
    return sprites
def load_assets():
    assets = {}

    personagem = pygame.image.load('assets/img/Idle.png').convert_alpha()
    personagem = load_spritesheet(personagem,1,6)
    personagem = personagem[0]
    escala = 1.5  
    nova_largura = int(personagem.get_width() * escala)
    nova_altura = int(personagem.get_height() * escala)
    assets['personagem'] = pygame.transform.scale(personagem, (nova_largura, nova_altura))

    fundo = pygame.image.load('assets/img/fundo.png').convert_alpha()
    fundo_larg = int(fundo.get_width()*3)
    fundo_alt = int(fundo.get_height()*3)

    assets['fundo'] = pygame.transform.scale(fundo,(fundo_larg,fundo_alt))
    return assets
