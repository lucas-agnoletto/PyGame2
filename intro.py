import pygame
import sys

# Inicialização do PyGame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('The Godfather Original Theme Song.mp3')
pygame.mixer.music.play(loops=-1)

# Configurações da tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tela de Menu")

# Carregar imagem de fundo
imagem_fundo = pygame.image.load("Imagem de Intro - PyGame.jpg")
imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))

# Carregar imagem de título
imagem_titulo = pygame.image.load("Título Game.png")
imagem_titulo = pygame.transform.scale(imagem_titulo, (400, 400))
posicao_imagem = (LARGURA + 100 , 0)

# Configurações do texto
fonte = pygame.font.Font(None, 50)  # Fonte e tamanho do texto
texto = "Clique ESPAÇO para começar"
cor_texto = (255, 255, 255)  # Cor branca
posicao_texto = (LARGURA // 2, ALTURA // 2 + 200)


# Variável para controlar o piscar do texto
mostrar_texto = True
tempo_mudanca = pygame.time.get_ticks()

# Função principal
def main():
    global mostrar_texto, tempo_mudanca  # Declare as variáveis globais aqui
    rodando = True
    while rodando:
        tela.blit(imagem_fundo, (0, 0))  # Desenha a imagem de fundo
        tela.blit(imagem_titulo, (0, 0))

        # Verificar o tempo para alternar entre mostrar ou não o texto
        if pygame.time.get_ticks() - tempo_mudanca > 500:  # Alterna a cada 500 ms
            mostrar_texto = not mostrar_texto
            tempo_mudanca = pygame.time.get_ticks()

        # Desenhar o texto animado
        if mostrar_texto:
            texto_surface = fonte.render(texto, True, cor_texto)
            texto_rect = texto_surface.get_rect(center=posicao_texto)
            tela.blit(texto_surface, texto_rect)

        # Verificar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    rodando = False  # Sai do loop e inicia o jogo

        pygame.display.flip()  # Atualiza a tela
        pygame.time.Clock().tick(60)  # Controla a taxa de quadros (60 FPS)

# Executa a função principal
if __name__ == "__main__":
    main()
