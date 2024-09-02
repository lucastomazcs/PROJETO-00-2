import pygame
from pygame.sprite import Sprite
import random
from explosao import Explosao

class InimigoExplosivo(Sprite):
    def __init__(self, posicao, tamanho, tempo_animacao, mapa, dono=None, configuracoes=None, velocidade=1, dano_explosao=2, intervalo_movimento=2):
        super().__init__()

        # Configura as propriedades do inimigo explosivo
        self.image = pygame.Surface(tamanho)
        self.image.fill((255, 0, 0))  # Cor vermelha para o inimigo bomba
        self.rect = self.image.get_rect(topleft=posicao)
        self.mapa = mapa
        self.velocidade = velocidade
        self.dano_explosao = dano_explosao
        self.timer_explosao = pygame.time.get_ticks() / 1000
        self.tempo_animacao = tempo_animacao
        self.explodido = False
        self.intervalo_movimento = intervalo_movimento
        self.contador_intervalo = 0
        
        # Define a direção inicial para o movimento
        self.direcao = random.choice(['esquerda', 'direita'])

    def update(self, dt):
        if not self.explodido:
            # Atualiza o contador de intervalo de movimento
            self.contador_intervalo += dt
            
            if self.contador_intervalo >= self.intervalo_movimento:
                self.contador_intervalo = 0
                self.mover()

            # Verifica a colisão com o jogador
            jogador_colidido = pygame.sprite.spritecollideany(self, self.mapa.jogadores)
            if jogador_colidido:
                self.explodir(jogador_colidido)

    def mover(self):
        if self.direcao == 'esquerda':
            self.rect.x -= self.velocidade
            if self.rect.left < 0:
                self.direcao = 'direita'
        elif self.direcao == 'direita':
            self.rect.x += self.velocidade
            if self.rect.right > self.mapa.largura:
                self.direcao = 'esquerda'

        # Verifica a colisão com blocos
        for bloco in self.mapa.bloco:
            if self.rect.colliderect(bloco.rect):
                self.direcao = 'esquerda' if self.direcao == 'direita' else 'direita'

    def explodir(self, jogador=None):
        if not self.explodido:
            self.explodido = True
            explosao = Explosao(self.rect.center, (self.rect.width, self.rect.height), self.tempo_animacao, self.mapa)
            self.mapa.explosoes.add(explosao)
            if jogador:
                jogador.sofrer_dano(self)
            self.kill()
