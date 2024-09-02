import pygame
import sys
from mapa import Mapa
from player import Player
from inimigo import Inimigo
from tkinter import *
from config import Configurações

#lala
pygame.init()
#ajusta o tamanho da tela de acordo com o monitor do usuário
root = Tk()
monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()

num_blocos_x = 15
num_blocos_y = 15
tamanho_bloco = (monitor_height // num_blocos_y) - 5

largura = num_blocos_x * tamanho_bloco
altura =  num_blocos_y * tamanho_bloco

tela = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)

pygame.display.set_caption("Bomberman")

preto = (0,0,0)

def game_over_d(tela):
    game_over_imagem = pygame.image.load("telas/Tela_Game_Overr.png")
    game_over_imagem = pygame.transform.scale(game_over_imagem,(largura, altura))
    tela.blit(game_over_imagem, (0,0))
    pygame.display.flip()

def tela_vitoria(tela):
    vitoria_imagem = pygame.image.load("telas/tela_Vitoriaa.png")
    vitoria_imagem = pygame.transform.scale(vitoria_imagem, (largura, altura))
    tela.blit(vitoria_imagem, (0,0))
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    rodando = True
    game_over = False
    vitoria = False

    mapa = Mapa(num_blocos_x, num_blocos_y, tamanho_bloco, tela)
    tamanho_imagem = (tamanho_bloco - 9, tamanho_bloco - 9)
    tamanho_imagem_inimigo = (tamanho_bloco - 9, tamanho_bloco - 9)
    jogador = Player((60, 60), 100, 2, 3, mapa, tamanho= tamanho_imagem)
    inimigo = Inimigo((tamanho_bloco * 14, tamanho_bloco * 14), 3, 15, 'direcao', mapa, tamanho = tamanho_imagem_inimigo)

    mapa.jogadores = [jogador]
    mapa.inimigos = [inimigo]

    sprites = pygame.sprite.Group()
    sprites.add(jogador)
    sprites.add(inimigo)

    while rodando:
        dt = clock.tick(60) / 100
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               rodando = False
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    main() #Reinicia o jogo
                elif game_over and event.key == pygame.K_q:
                    rodando = False
                elif vitoria and event.key == pygame.K_r:
                    main() #Reinicia o jogo
                elif vitoria and event.key == pygame.K_q:
                    rodando = False


        if not game_over and not vitoria:           
            jogador.update(dt)
            inimigo.update(jogador.rect.topleft, dt)

            tela.fill(preto)
            mapa.desenhar(tela)
            mapa.bombas.update(dt)
            mapa.bombas.draw(tela)
            sprites.draw(tela)

            # Atualização dos sprites
            mapa.explosoes.update(dt)

            # Desenho dos sprites
            mapa.explosoes.draw(mapa.tela)

            mapa.update(dt)
        
            pygame.display.flip()
            if not jogador.alive():
                game_over = True
            if not inimigo.alive():
                vitoria = True
                

        elif game_over:
            game_over_d(tela)
            clock.tick(60)
        elif vitoria:
            tela_vitoria(tela)
            clock.tick(60)

    pygame.quit()
    sys.exit()


main()