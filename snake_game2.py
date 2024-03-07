import pygame
from pygame.locals import *
from sys import exit
from random import randint

def reiniciar_jogo():
    global pontos, velocidade, x_cobra, y_cobra, morreu, tamanho_cobra, lista_cobra, x_controle, y_controle
    pontos = 0
    velocidade = 5
    x_controle = velocidade
    y_controle = 0
    x_cobra = largura / 2 - largura_padrao / 2
    y_cobra = altura / 2 - altura_padrao / 2
    morreu = False
    tamanho_cobra = 3
    sorteio_maca()
    lista_cobra = []

def desenhar_cobra(lista_cobra):
    for XeY in lista_cobra: #lista dentro lista
        pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], largura_padrao, altura_padrao))

def sorteio_maca():
    global x_maca, y_maca 
    lista_maca = lista_cobra[0]
    while lista_maca in lista_cobra:
        lista_maca = []
        x_maca = randint(0, 620)
        y_maca = randint(0, 460)
        lista_maca.append(x_maca)
        lista_maca.append(y_maca)

pygame.init()

#dimensão de tela, tela e nome da tela
largura = 640
altura = 480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Snake Game")

#variáveis facilitadoras
velocidade = 5
largura_padrao = 20
altura_padrao = 20

#variáveis de controle
x_controle = velocidade
y_controle = 0
pontos = 0
morreu = False
tamanho_cobra = 3

#valores da cobra - nascer no meio
x_cobra = largura / 2 - largura_padrao / 2
y_cobra = altura / 2 - altura_padrao / 2

#cobra
lista_cobra = []

#valores da maçã - randomizados
x_maca = randint(0, 620)
y_maca = randint(0, 460)

#fps
relogio = pygame.time.Clock()

#texto
tamanho_fonte1 = 50
fonte1 = pygame.font.SysFont("arial", tamanho_fonte1, True, False)
tamanho_fonte2 = 20
fonte2 = pygame.font.SysFont("arial", tamanho_fonte2, True, True)

#efeitos sonoros
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.load("./Trilhas/background.mp3")
pygame.mixer.music.play(-1)

som_colisao = pygame.mixer.Sound("./Trilhas/apple.wav")
som_colisao.set_volume(0.3)

#jogo
while True:
    mensagem1 = f"Pontos: {pontos}"
    texto_formatado1 = fonte1.render(mensagem1, True, (0, 0, 0))
    ret_texto1 = texto_formatado1.get_rect()
    ret_texto1.center = (largura / 2 , tamanho_fonte1 / 2)
    relogio.tick(60)
    tela.fill((255, 255, 255))
    #interações com botões
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_w:
                if y_controle == velocidade:
                    pass
                else:
                    y_controle = -velocidade
                    x_controle = 0
            if event.key == K_a:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle = - velocidade
                    y_controle = 0
            if event.key == K_s:
                if y_controle == - velocidade:
                    pass
                else: 
                    y_controle = velocidade
                    x_controle = 0 
            if event.key == K_d:
                if x_controle == - velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0
    #movimento contínuo
    x_cobra += x_controle
    y_cobra += y_controle

    #"objetos"
    cobra = pygame.draw.rect(tela, (0, 255, 0), (x_cobra, y_cobra, largura_padrao, altura_padrao))
    maca = pygame.draw.rect(tela, (255, 0, 0), (x_maca, y_maca, largura_padrao, altura_padrao))

    #colisão
    if cobra.colliderect(maca):
        som_colisao.play()
        pontos += 1
        tamanho_cobra += 1
        velocidade += 0.2
        sorteio_maca()
        #ajustando controle de acordo com a nova velocidade para permitir verificação de eventos
        if x_controle != 0:
            if x_controle > 0:
                x_controle = velocidade
            else: 
                x_controle = - velocidade
        else:
            if y_controle > 0:
                y_controle = velocidade
            else:
                y_controle = - velocidade
        
    #montagem cabeça    
    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)

    #morte
    if lista_cabeca in lista_cobra:
        morreu = True
        mensagem2 = "GAME OVER! Pressione a tecla R para jogar novamente."
        texto_formatado2 = fonte2.render(mensagem2, True, (0, 0, 0))
        ret_texto2 = texto_formatado2.get_rect()
        ret_texto2.center = (largura / 2, altura / 2)

        while morreu:
            tela.fill((255, 255, 255))
            tela.blit(texto_formatado2, ret_texto2)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()
            pygame.display.update()
    else:
        lista_cobra.append(lista_cabeca)

    #controle cobra
    if len(lista_cobra) > tamanho_cobra:
        del lista_cobra[0]
    desenhar_cobra(lista_cobra)

    #limitando escopo
    if x_cobra > largura: 
        x_cobra = 0
    elif x_cobra < 0:
        x_cobra = largura
    if y_cobra > altura:
        y_cobra = 0
    elif y_cobra < 0:
        y_cobra = altura


    tela.blit(texto_formatado1, ret_texto1)
    pygame.display.update()
