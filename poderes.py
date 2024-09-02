import pygame
import random
from pygame.sprite import Group

class Poder(pygame.sprite.Sprite):
    def __init__(self, posicao, tamanho, tipo):
        super().__init__()
        
        self.tipo = tipo
        if self.tipo == 'velocidade':
            self.image = pygame.image.load('poderes/poder_mais_rapido.png').convert_alpha()
        elif self.tipo == 'vida':
            self.image = pygame.image.load('poderes/poder_vida.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, tamanho)
        self.rect = self.image.get_rect()
        self.rect.topleft = posicao

    def aplicar_poder(self, jogador):
        if self.tipo == 'velocidade':
            jogador.aumentar_velocidade()
        elif self.tipo == 'vida':
            jogador.aumentar_vida()
    
    @staticmethod
    def gerar_poder(posicao, tamanho, dificuldade):
        chance = random.random()
        if dificuldade == 'Fácil':
            if chance < 0.15:
                return Poder(posicao, tamanho, 'velocidade')
            elif chance < 0.30:
                return Poder(posicao, tamanho, 'vida')
        elif dificuldade == 'Médio':
            if chance < 0.12:
                return Poder(posicao, tamanho, 'velocidade')
            elif chance < 0.24:
                return Poder(posicao, tamanho, 'vida')
        elif dificuldade == 'Difícil':
            if chance < 0.10:
                return Poder(posicao, tamanho, 'velocidade')
            elif chance < 0.20:
                return Poder(posicao, tamanho, 'vida')
        return None
        