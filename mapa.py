import pygame
from pygame.sprite import Sprite
from bloco import Bloco
import random
from poderes import Poder

class Mapa(Bloco):
    def __init__(self, num_blocos_x, num_blocos_y, tamanho_bloco, tela, dificuldade):

        super().__init__('Fundo/fundo.png', 0, 0, tamanho_bloco)

        
        self.dificuldade = dificuldade
        self.tela = tela
        self.num_blocos_x = num_blocos_x
        self.num_blocos_y = num_blocos_y
        self.tamanho_bloco = tamanho_bloco
        
        # Calculando a largura e a altura do mapa
        self.largura = num_blocos_x * tamanho_bloco
        self.altura = num_blocos_y * tamanho_bloco
               
        # Definindo mapa
        self.mapa = [
            "WWWWWWWWWWWWWWW",
            "WEEEDDDDDDDEEEW",
            "WEBEBEBEBEBDBEW",
            "WEDDDDDDEEEDDEW",
            "WDBEBEBEBEBDBDW",
            "WDDEDDDDDDEDDDW",
            "WDBEBEBDBEBDBDW",
            "WDDDDEEDEDDDDDW",
            "WDBEBEBDBEBDBDW",
            "WDDEDDDDDDDDDDW",
            "WDBEBEBDBEBDBDW",
            "WDDDEEEEDDDDDDW",
            "WEBEBEBEBEBEBEW",
            "WEEEDDDDDDDEEEW",
            "WWWWWWWWWWWWWWW"
        ]

        self.blocos = pygame.sprite.Group()
        self.bombas = pygame.sprite.Group()
        self.explosoes = pygame.sprite.Group()
        self.poderes = pygame.sprite.Group()

        self.blocos_destrutiveis = {} #Armazene blocos destrutiveis e os poderes associados
        
        self.criar_mapa()

    def criar_mapa(self):
        for y, linha in enumerate(self.mapa):
            for x, bloco in enumerate(linha):
                x_pos = x * self.tamanho_bloco
                y_pos = y * self.tamanho_bloco
                if bloco == 'W':
                    bloco_lateral = Bloco('Blocos/bloco_lateral4.png', x_pos, y_pos, self.tamanho_bloco)
                    self.blocos.add(bloco_lateral)
                elif bloco == 'B':
                    bloco_fixo = Bloco('Blocos/blocoEstrelas.png', x_pos, y_pos, self.tamanho_bloco)
                    self.blocos.add(bloco_fixo)
                elif bloco == 'E':
                    Bloco('Fundo/fundo.png', x_pos, y_pos, self.tamanho_bloco)  # Apenas um fundo vazio
                elif bloco == 'D':
                    bloco_destrutivel = Bloco('Blocos/bloco_destrutivel.png', x_pos, y_pos, self.tamanho_bloco, destrutivel=True)
                    self.blocos.add(bloco_destrutivel)
                
                    #Gera um poder mas não o desenha
                    poder = Poder.gerar_poder((x_pos, y_pos), (self.tamanho_bloco, self.tamanho_bloco), self.dificuldade)
                    if poder:
                        #Associa o poder ao bloco destrutivel
                        self.blocos_destrutiveis[(x_pos, y_pos)] = poder

    def desenhar(self, tela):
        self.blocos.draw(tela)
        self.bombas.draw(tela)
        self.poderes.draw(tela)

    def update(self, dt):
        self.blocos.update(dt)
        self.bombas.update(dt)
        self.explosoes.update(dt)
        
     # Verifica se algum bloco destrutível foi destruído
        for bloco in list(self.blocos_destrutiveis.keys()):
            bloco_obj = next((b for b in self.blocos if (b.rect.topleft == bloco) and b.destrutivel), None)
            if bloco_obj is None or not bloco_obj.alive():  # Verifica se o bloco foi destruído
                poder = self.blocos_destrutiveis.pop(bloco)
                self.poderes.add(poder)  # Adiciona o poder para ser desenhado e atualizado

        self.poderes.update(dt)

    def aumentar_tamanho_bloco(self, novo_tamanho):
        for bloco in self.blocos:
            bloco.aumentar_tamanho(novo_tamanho)

    def obter_blocos_destrutiveis(self):
        for bloco in self.blocos:
            if bloco.destrutivel:
                print(f"Bloco destrutível encontrado: {bloco.rect}")

