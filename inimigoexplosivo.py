from typing import Any
import pygame
from pygame.sprite import Sprite
import math
from explosao import Explosao

class InimigoExplosivo(Sprite):
    def __init__(self, posicao, tamanho, velocidade, mapa) -> None:
        super().__init__()
        self.__posicao = posicao
        self.__velocidade = velocidade
        self.tamanho = tamanho
        self.mapa = mapa
        self.__vida = 1 # O inimigo morre com uma explosão
        self.__dano_explosao = 9999

        # Variavel para controlar o tempo entre teleportes
        self.tempo_teleporte = 2.0
        self.tempo_ultimo_teleporte = 0

        #Carrega imagens do inimigo:
        self.imagens= {
            'direita': pygame.image.load('inimigo_explosivo/inimigo_novo_direita1.png').convert_alpha(),
            'esquerda': pygame.image.load('inimigo_explosivo/inimigo_novo_esquerda1.png').convert_alpha(),
            'frente': pygame.image.load('inimigo_explosivo/inimigo_novo.png').convert_alpha(),
            'tras': pygame.image.load('inimigo_explosivo/inimigo_novo_trás1.png').convert_alpha()
        }
        self.direcao = 'frente' # Direção Inicial
        self.image = self.imagens[self.direcao]
        self.rect = self.image.get_rect(topleft = posicao)

    @property
    def posicao(self):
        return self.__posicao
    @property
    def velocidade(self):
        return self.__velocidade
    @property
    def vida(self):
        return self.__vida
    @property
    def dano_explosao(self):
        return self.__dano_explosao
    
    def movimentar(self, dt):
        jogador_mais_proximo = self.encontrar_jogador_proximo()
        if jogador_mais_proximo:
            direcao = (jogador_mais_proximo.rect.centerx - self.rect.centerx,
                       jogador_mais_proximo.rect.centery - self.rect.centery)
            distancia = math.hypot(*direcao)
            if distancia != 0:
                direcao = (direcao[0] / distancia, direcao[1] / distancia)
                self.rect.x += direcao[0] * self.velocidade * dt
                self.rect.y += direcao[1] * self.velocidade * dt

                # Atualizar a direção com base no movimento
                if abs(direcao[0]) > abs(direcao[1]):
                    if direcao[0] > 0:
                        self.direcao = 'direita'
                    else:
                        self.direcao = 'esquerda'
                else:
                    if direcao[1] > 0:
                        self.direcao = 'frente'
                    else:
                        self.direcao = 'tras'
                
                # Atualizar a imagem com base na direção
                self.image = self.imagens[self.direcao]
                self.rect = self.image.get_rect(center=self.rect.center)
        
        # Checa tempo para teleporte
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.tempo_ultimo_teleporte >= self.tempo_teleporte:
            self.teletransportar_para_espaco_vazio_mais_proximo(jogador_mais_proximo)
            self.tempo_ultimo_teleporte = current_time

    def teletransportar_para_espaco_vazio_mais_proximo(self, jogador):
        # Direção do teleporte em direção ao jogador
        direcao = pygame.math.Vector2(jogador.rect.center) - pygame.math.Vector2(self.rect.center)
        direcao = direcao.normalize()  # Normaliza o vetor para obter direção

        # Distância máxima de teleporte
        distancia_max = 100  # Pode ajustar conforme necessário
        for distancia in range(int(distancia_max), 0, -10):  # Passos de 10 pixels
            nova_posicao = pygame.math.Vector2(self.rect.center) + direcao * distancia
            nova_posicao = (int(nova_posicao.x), int(nova_posicao.y))

            # Verifica se a nova posição é livre de blocos e inimigos
            if not any(bloco.rect.collidepoint(nova_posicao) for bloco in self.mapa.blocos) and \
               not any(inimigo.rect.collidepoint(nova_posicao) for inimigo in self.mapa.inimigos):
                self.rect.center = nova_posicao
               # Atualiza o rect para garantir que está posicionado corretamente
                self.rect = self.image.get_rect(center=self.rect.center)
                print(f"Teletransportado para: {self.rect.center}")  # Debug
                break
    
    def encontrar_jogador_proximo(self):
        jogador_mais_proximo = None
        menor_distancia = float('inf')
        for jogador in self.mapa.jogadores:
            distancia = math.hypot(jogador.rect.centerx - self.rect.centerx, jogador.rect.centery - self.rect.centery)
            if distancia < menor_distancia:
                menor_distancia = distancia
                jogador_mais_proximo = jogador
        return jogador_mais_proximo

    def verificar_colisoes(self):
        # Verifica colisão com jogadores
        jogador_colidido = pygame.sprite.spritecollideany(self, self.mapa.jogadores)
        if jogador_colidido:
            self.explodir(jogador_colidido)
        
        # Verifica se está no raio de explosão de uma bomba
        explosao_colidida = pygame.sprite.spritecollideany(self, self.mapa.explosoes)
        if explosao_colidida:
            self.sofrer_dano(explosao_colidida)
    
    def explodir(self, jogador):
        # Matar o jogador instantaneamente
        jogador.morrer()
        # Remover o inimigo do jogo
        self.kill()
    
    def sofrer_dano(self, explosao):
        self.__vida -= 1
        if self.__vida <= 0:
            self.kill()
    
    def update(self, dt ):
        self.movimentar(dt)
        self.verificar_colisoes()
    
    def draw(self, tela):
        tela.blit(self.image, self.rect)