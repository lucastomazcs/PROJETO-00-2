import pygame
from pygame.sprite import Sprite
import random

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
        self.tempo_mudanca_direcao = 10.0  # Tempo em segundos para mudar de direção
        self.tempo_ultima_mudanca = 0

        # Carrega imagens do inimigo
        self.imagens = {
            'direita': pygame.image.load('inimigo_explosivo/inimigo_pq_direito0.png').convert_alpha(),
            'esquerda': pygame.image.load('inimigo_explosivo/inimigo_pq_esquerdo0.png').convert_alpha(),
            'frente': pygame.image.load('inimigo_explosivo/inimigo_pq0.png').convert_alpha(),
            'tras': pygame.image.load('inimigo_explosivo/inimigo_pq_trás0.png').convert_alpha()
        }
        self.direcao = 'frente'  # Direção inicial
        self.image = self.imagens[self.direcao]
        self.rect = self.image.get_rect(topleft=posicao)

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

    @vida.setter
    def vida(self, valor):
        if valor >= 0:
            self.__vida = valor
        
    
    @raio_explosao.setter
    def raio_explosao(self, valor):
        if valor >= 0:
            self.__raio_explosao = valor
        
    
    def movimentar(self, dt):
        # Tempo atual
        current_time = pygame.time.get_ticks() / 1000

        # Mudar de direção a cada X segundos
        if current_time - self.tempo_ultima_mudanca >= self.tempo_mudanca_direcao:
            self.direcao = random.choice(['direita', 'esquerda', 'frente', 'tras'])
            self.tempo_ultima_mudanca = current_time

        # Movimentação baseada na direção
        if self.direcao == 'direita':
            self.rect.x += self.velocidade * dt
        elif self.direcao == 'esquerda':
            self.rect.x -= self.velocidade * dt
        elif self.direcao == 'frente':
            self.rect.y += self.velocidade * dt
        elif self.direcao == 'tras':
            self.rect.y -= self.velocidade * dt

        # Atualizar a imagem com base na direção
        self.image = self.imagens[self.direcao]
        self.rect = self.image.get_rect(center=self.rect.center)

        # Verificar colisão com blocos
        for bloco in self.mapa.blocos:
            if self.rect.colliderect(bloco.rect):
                if bloco.destrutivel:
                    bloco.destruir()  # Implementar método destruir em Bloco
                    self.mapa.blocos.remove(bloco)
                    if (bloco.rect.topleft in self.mapa.blocos_destrutiveis):
                        poder = self.mapa.blocos_destrutiveis.pop(bloco.rect.topleft)
                        self.mapa.poderes.add(poder)
                # Reverter o movimento se colidiu
                if self.direcao == 'direita':
                    self.rect.x -= self.velocidade * dt
                elif self.direcao == 'esquerda':
                    self.rect.x += self.velocidade * dt
                elif self.direcao == 'frente':
                    self.rect.y -= self.velocidade * dt
                elif self.direcao == 'tras':
                    self.rect.y += self.velocidade * dt
                break  # Interrompe o loop ao detectar a colisão

    def verificar_colisoes(self):
        # Verifica colisão com jogadores
        jogador_colidido = pygame.sprite.spritecollideany(self, self.mapa.jogadores)
        if jogador_colidido:
            self.explodir(jogador_colidido)

        # Verifica colisão com bombas
        for bomba in self.mapa.bombas:
            if self.rect.colliderect(bomba.rect):
                if bomba.explodindo:  # Verifica se a bomba está prestes a explodir
                    self.sofrer_dano(bomba)

    def explodir(self, jogador):
        from explosao import Explosao
        # Cria explosão
        explosao = Explosao(self.rect.center, (self.__raio_explosao * 2, self.__raio_explosao * 2), 0.05, self.mapa, dono=self)
        self.mapa.explosoes.add(explosao)

        # Se o jogador colidiu, matá-lo
        if jogador is not None:
            jogador.morte_instantanea()

        # Remover o inimigo do jogo após a explosão
        self.kill()  # Remove o inimigo do grupo

    def sofrer_dano(self, explosao):
        # Aqui você deve verificar a lógica interna da explosão para causar dano
        self.__vida -= 1
        if self.__vida <= 0:
            self.explodir(None)  # Explode ao morrer

    def update(self, dt):
        if self.vida > 0:  # Só movimentar e verificar colisões se o inimigo estiver vivo
            self.movimentar(dt)
            self.verificar_colisoes()

    def draw(self, tela):
        tela.blit(self.image, self.rect)
