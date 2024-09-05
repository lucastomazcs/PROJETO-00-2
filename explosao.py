import pygame
from pygame.sprite import Sprite, Group
from config import Configurações
from inimigoexplosivo import InimigoExplosivo

class Explosao(Sprite): #herança da classe Sprite
    def __init__(self, posicao, tamanho, tempo_animacao, mapa, dono = None, configuracoes = None):
        super().__init__()

        self.images = [
            pygame.transform.scale(pygame.image.load('Explosão/explosao.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Explosão/explosao2.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Explosão/explosao3.png').convert_alpha(), tamanho)

        ]

        #Carrega som da explosão:
        self.som_explosao = pygame.mixer.Sound('Explosão/Bomb Explodes.wav')

        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center = posicao)
        self.tempo_animacao = tempo_animacao
        self.contador_tempo = 0
        self.mapa = mapa
        self.dono = dono

        self.configuracoes = Configurações()

        #Verifica se o som está mutado antes de tocar a explosão
        if self.configuracoes:
            self.configuracoes.controlar_som_efeitos(self.som_explosao)

        self.som_explosao.play()


    def update(self, dt):
        self.contador_tempo += dt
        if self.contador_tempo >= self.tempo_animacao:
            self.contador_tempo = 0
            self.image_index += 1
            if self.image_index < len(self.images):
                self.image = self.images[self.image_index]
            else:
                self.causar_dano()
                self.kill()
        
            
    def causar_dano(self):
        from player import Player
        # Verifica se o dano é causado por uma bomba de jogador
        is_bomba_jogador = isinstance(self.dono, Player)

        for sprite in pygame.sprite.spritecollide(self, self.mapa.jogadores, False):
            sprite.sofrer_dano(self)

        for sprite in pygame.sprite.spritecollide(self, self.mapa.inimigos, False):
            if is_bomba_jogador and isinstance(sprite, InimigoExplosivo):
                # Se a explosão for de um jogador e atingir um InimigoExplosivo, matá-lo instantaneamente
                sprite.explodir(None)  # Detona o inimigo imediatamente
            elif sprite != self.dono:
                # Caso contrário, aplica dano normal
                sprite.sofrer_dano(self)



