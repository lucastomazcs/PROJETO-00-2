import pygame
from pygame.sprite import Sprite
import math
from mapa import Mapa
from bomba import Bomba
from personagens import Personagem

class Inimigo(Personagem, Sprite):  # Inimigo herda de Personagem e Sprite
    def __init__(self, posicao, vida, velocidade, direcao, mapa, tamanho):
        # Inicialização da classe base (Personagem)
        Personagem.__init__(self, vida, posicao, velocidade, range_bomba=2)

        # Inicialização da classe Sprite
        Sprite.__init__(self)
        
        self.mapa = mapa
        self.__direcao = direcao

        # Carregando imagens inimigo
        self.images = [
            pygame.transform.scale(pygame.image.load('Inimigo/inimigo_andando01.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Inimigo/inimigo_andando02.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Inimigo/inimigo_andando03.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Inimigo/inimigo_andando_lado01.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Inimigo/inimigo_andando_lado02.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Inimigo/inimigo_andando_lado03.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Inimigo/inimigo_andando_tras01.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Inimigo/inimigo_andando_tras02.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Inimigo/inimigo_andando_tras03.png').convert_alpha(), tamanho)
        ]

        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()

        # Definindo posição inicial do inimigo
        self.rect.bottomright = posicao

        # Tempo de troca de animação
        self.tempo_animacao = 1
        self.contador_tempo = 0
        self.tempo_ultimo_plante = 0
        self.intervalo_bomba = 3
        self.minhas_bombas = []
        self.invulneravel = False
        self.tempo_invulnerabilidade = 1.0  # tempo de invulnerabilidade em segundos
        self.ultimo_tempo_dano = 0

    @property
    def direcao(self):
        return self.__direcao

    def movimento(self, posicao_player, dt: float):
        posicao_original = self.rect.topleft
    
        # Calcula a direção para o jogador:
        delta_x = posicao_player[0] - self.rect.centerx
        delta_y = posicao_player[1] - self.rect.centery
        distancia = math.hypot(delta_x, delta_y)

        if distancia != 0:
            direcao_x = (delta_x / distancia) * self.velocidade * dt
            direcao_y = (delta_y / distancia) * self.velocidade * dt
        else:
            direcao_x = 0
            direcao_y = 0

        # Tentativa de movimento no eixo X
        self.rect.x += direcao_x

        # Checa colisões com blocos e bombas no eixo X
        if pygame.sprite.spritecollideany(self, self.mapa.blocos) or pygame.sprite.spritecollideany(self, self.mapa.bombas):
            self.rect.x = posicao_original[0]

        # Tentativa de movimento no eixo Y
        self.rect.y += direcao_y

        # Checa colisões com blocos e bombas no eixo Y
        if pygame.sprite.spritecollideany(self, self.mapa.blocos) or pygame.sprite.spritecollideany(self, self.mapa.bombas):
            self.rect.y = posicao_original[1]

        self._Personagem__posicao = self.rect.topleft  # Atualiza a posição herdada de Personagem

        if self.caminho_bloqueado():
            self.plantar_bomba()

    def caminho_bloqueado(self):
        for bloco in self.mapa.blocos:
            if bloco.destrutivel and self.rect.colliderect(bloco.rect.inflate(20, 20)):
                return True
        return False

    def plantar_bomba(self):
        if not self.alive(): # Verifica se o inimigo está vivo
            return

        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.tempo_ultimo_plante >= self.intervalo_bomba:
            bomba = Bomba(self.rect.topleft, self.range_bomba, 30, (40, 40), self.mapa, dono=self)
            self.minhas_bombas.append(bomba)
            self.mapa.bombas.add(bomba)
            self.tempo_ultimo_plante = current_time

    def set_vida(self, nova_vida):
        self.vida = nova_vida

    def sofrer_dano(self, fonte):
        
        current_time = pygame.time.get_ticks() / 1000

        # Evita dano de suas próprias bombas
        if fonte in self.minhas_bombas:
            return
        
        # Checa se inimigo está invulnerável
        if self.invulneravel and current_time - self.ultimo_tempo_dano < self.tempo_invulnerabilidade:
            return
        
        # Aplica o dano caso não esteja invulnerável:
        super().sofrer_dano(fonte)  # Usa o método herdado de Personagem
        
        # Ativa o modo invulnerável:
        self.invulneravel = True
        self.ultimo_tempo_dano = current_time

    def matar_jogador(self, jogador):
        if pygame.sprite.collide_rect(self, jogador):
            jogador.sofrer_dano(self)  # Aplica dano ao jogador

    def animacao(self, dt: float):
        self.contador_tempo += dt
        if self.contador_tempo >= self.tempo_animacao:
            self.contador_tempo = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

    def update(self, jogadores, dt: float):
        if not self.alive():
            return
        
        # Escolhe o jogador mais próximo:
        jogador_mais_proximo = self.encontrar_jogador_mais_proximo(jogadores)

        # Move em direção ao jogador mais próximo:
        self.movimento(jogador_mais_proximo.rect.topleft, dt)
        self.animacao(dt)

        # Tenta matar o jogador mais próximo se estiver a uma certa distância
        if abs(jogador_mais_proximo.rect.centerx - self.rect.centerx) <= 40 and abs(jogador_mais_proximo.rect.centery - self.rect.centery) <= 40:
            self.matar_jogador(jogador_mais_proximo)

        # Verifica se o inimigo está invulnerável
        if self.invulneravel:
            current_time = pygame.time.get_ticks() / 1000
            if current_time - self.ultimo_tempo_dano > self.tempo_invulnerabilidade:
                self.invulneravel = False

    def encontrar_jogador_mais_proximo(self, jogadores):
        jogador_mais_proximo = None
        menor_distancia = float('inf')  # Inicializa com um valor muito grande
    
        # Percorre todos os jogadores
        for jogador in jogadores:
            if jogador.alive():
                # Calcula a distância entre o inimigo e o jogador
                delta_x = jogador.rect.centerx - self.rect.centerx
                delta_y = jogador.rect.centery - self.rect.centery
                distancia = math.hypot(delta_x, delta_y)  # Distância euclidiana
            
                # Verifica se essa é a menor distância encontrada
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    jogador_mais_proximo = jogador
    
        return jogador_mais_proximo
    
    def calcular_distancia(self, posicao_jogador):
        delta_x = posicao_jogador[0] - self.rect.centerx
        delta_y = posicao_jogador[1] - self.rect.centery
        return math.hypot(delta_x, delta_y)
    
    def morrer(self):
        if self.vida <= 0:
            print("Inimigo morreu!")
            self.kill()  # Remove o inimigo do grupo e para de atualizá-lo