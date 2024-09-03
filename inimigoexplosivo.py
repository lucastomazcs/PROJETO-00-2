import pygame
from pygame.sprite import Sprite
import random
import math
from explosao import Explosao
from player import Player

class InimigoExplosivo(Sprite):
    def __init__(self, posicao, tamanho, velocidade, mapa, raio_explosao) -> None:
        super().__init__()
        self.__posicao = posicao
        self.__velocidade = velocidade
        self.tamanho = tamanho
        self.mapa = mapa
        self.__vida = 1  # O inimigo morre com uma explosão
        self.__dano_explosao = 9999
        self.__raio_explosao = raio_explosao

        # Variável para controlar o tempo entre mudanças de direção
        self.tempo_mudanca_direcao = 2.0  # Tempo em segundos para mudar de direção
        self.tempo_ultima_mudanca = 0

        # Variável para controlar o tempo entre teleportes
        self.tempo_teleporte = 20.0
        self.tempo_ultimo_teleporte = 0

        # Carrega imagens do inimigo
        self.imagens = {
            'direita': pygame.image.load('inimigo_explosivo/inimigo_novo_direita1.png').convert_alpha(),
            'esquerda': pygame.image.load('inimigo_explosivo/inimigo_novo_esquerda1.png').convert_alpha(),
            'frente': pygame.image.load('inimigo_explosivo/inimigo_novo.png').convert_alpha(),
            'tras': pygame.image.load('inimigo_explosivo/inimigo_novo_trás1.png').convert_alpha()
        }
        self.direcao = 'frente'  # Direção inicial
        self.image = self.imagens[self.direcao]
        self.rect = self.image.get_rect(topleft=posicao)
        self.target_posicao = pygame.Vector2(posicao)
        self.explodindo = False  # Estado de explosão

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

    @property
    def raio_explosao(self):
        return self.__raio_explosao

    def encontrar_jogador_mais_proximo(self):
        jogadores = pygame.sprite.spritecollide(self, self.mapa.jogadores, False)
        if jogadores:
            return min(jogadores, key=lambda jogador: self.rect.centerx - jogador.rect.centerx)
        return None

    def movimentar(self, dt):
        if self.explodindo:
            return  # Não permite movimento durante a explosão

        # Tempo atual
        current_time = pygame.time.get_ticks() / 1000

        jogador_proximo = self.encontrar_jogador_mais_proximo()
        if jogador_proximo:
            jogador_posicao = pygame.Vector2(jogador_proximo.rect.center)
            direcao = jogador_posicao - pygame.Vector2(self.rect.center)
            distancia = direcao.length()
            if distancia > 0:
                direcao.normalize_ip()
                self.target_posicao = pygame.Vector2(self.rect.center) + direcao * self.velocidade * dt

        # Interpolação suave do movimento
        self.rect.centerx += (self.target_posicao.x - self.rect.centerx) * 0.1
        self.rect.centery += (self.target_posicao.y - self.rect.centery) * 0.1

        # Atualizar a imagem com base na direção
        if jogador_proximo:
            if abs(self.target_posicao.x - self.rect.centerx) > abs(self.target_posicao.y - self.rect.centery):
                self.direcao = 'direita' if self.target_posicao.x > self.rect.centerx else 'esquerda'
            else:
                self.direcao = 'frente' if self.target_posicao.y > self.rect.centery else 'tras'

        self.image = self.imagens[self.direcao]
        self.rect = self.image.get_rect(center=self.rect.center)

        # Verificar se está colidindo com um bloco ou saiu dos limites do mapa
        if any(bloco.rect.colliderect(self.rect) for bloco in self.mapa.blocos):
            # Reverter o movimento se colidiu
            self.target_posicao = pygame.Vector2(self.rect.center)

        # Checa tempo para teleporte
        if current_time - self.tempo_ultimo_teleporte >= self.tempo_teleporte:
            self.teletransportar_para_posicao_aleatoria_vazia()
            self.tempo_ultimo_teleporte = current_time

    def teletransportar_para_posicao_aleatoria_vazia(self):
        if self.explodindo:
            return  # Não teletransporta durante a explosão

        # Obter todas as posições possíveis para teletransporte
        posicoes_validas = []

        for y, linha in enumerate(self.mapa.mapa):
            for x, tile in enumerate(linha):
                if tile == 'E':  # 'E' representa um espaço vazio no mapa
                    posicao = (x * self.mapa.tamanho_bloco, y * self.mapa.tamanho_bloco)
                    # Verifica se a posição não está ocupada por outros inimigos
                    if not any(inimigo.rect.colliderect(pygame.Rect(posicao, (self.rect.width, self.rect.height))) for inimigo in self.mapa.inimigos):
                        posicoes_validas.append(posicao)

        # Verifica se há posições válidas disponíveis
        if posicoes_validas:
            nova_posicao = random.choice(posicoes_validas)
            self.rect.topleft = nova_posicao
            self.__posicao = nova_posicao  # Atualiza a posição interna
            print(f"Teletransportado para: {self.rect.center}")  # Debug
        else:
            print("Nenhuma posição válida encontrada para teletransporte.")

    def verificar_colisoes(self):
        if self.explodindo:
            return  # Não verifica colisões durante a explosão

        # Verifica colisão com jogadores
        jogador_colidido = pygame.sprite.spritecollideany(self, self.mapa.jogadores)
        if jogador_colidido:
            self.explodir(jogador_colidido)

        # Verifica se está no raio de explosão de uma bomba
        explosao_colidida = pygame.sprite.spritecollideany(self, self.mapa.explosoes)
        if explosao_colidida:
            self.sofrer_dano(explosao_colidida)

    def explodir(self, jogador):
        if self.explodindo:
            return  # Não explode novamente

        self.explodindo = True  # Marca como explodindo

        # Cria explosão com fade-out
        explosao = Explosao(self.rect.center, (self.__raio_explosao * 2, self.__raio_explosao * 2), 0.5, self.mapa)
        self.mapa.explosoes.add(explosao)

        # Se o jogador colidiu, matá-lo
        if jogador is not None:
            jogador.morte_instantanea()

        # Remover o inimigo do jogo após a explosão
        self.kill()

    def sofrer_dano(self, explosao):
        if isinstance(explosao.dono, Player):
            self.__vida -= 1
            if self.__vida <= 0:
                self.explodir(None)  # Explode ao morrer, mesmo que não haja um jogador específico

    def update(self, dt):
        self.movimentar(dt)
        self.verificar_colisoes()

    def draw(self, tela):
        tela.blit(self.image, self.rect)
