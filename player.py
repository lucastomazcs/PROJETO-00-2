import pygame
from pygame.sprite import Sprite
from personagens import Personagem
from bomba import Bomba
from poderes import Poder
from mapa import Mapa

class Player(Personagem, Sprite):
    def __init__(self, posicao, vida, velocidade, range_bomba, mapa, dificuldade, tamanho, controles=None, jogador_id=1):
        # Inicializa a classe base Personagem
        Personagem.__init__(self, vida, posicao, velocidade, range_bomba)
        
        # Inicializa a classe Sprite
        Sprite.__init__(self)
        
        self.mapa = mapa
        self.dificuldade = dificuldade
        self.poder_pegos = set()
        self.__vida_maxima = 5

        # Inicializar variáveis de controle
        self.invulneravel = False
        self.tempo_invulnerabilidade = 1.0  # Tempo de invulnerabilidade em segundos
        self.ultimo_tempo_dano = 0

        # Define imagens específicas para cada jogador
        self.images = self.carregar_imagens(jogador_id, tamanho)
        
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()

        # Define a posição inicial do jogador
        self.rect.topleft = posicao

        # Tempo de troca de animação
        self.tempo_animacao = 0.01
        self.contador_tempo = 0

        # Variáveis de controle do tempo de plantar a bomba
        self.tempo_ultimo_plante = 0
        self.intervalo_bomba = 3

        # Define os controles, usa por padrão WASD
        self.controles = controles if controles else {
            'cima': pygame.K_w,
            'baixo': pygame.K_s,
            'esquerda': pygame.K_a,
            'direita': pygame.K_d,
            'bomba': pygame.K_SPACE
        }
        
        # Configura as vidas iniciais do jogador com base na dificuldade
        self.configurar_vidas_iniciais()

    def carregar_imagens(self, jogador_id, tamanho):
        try:
            if jogador_id == 1:
                return [
                    pygame.transform.scale(pygame.image.load('Bomberman/bomberman_frente.png').convert_alpha(), tamanho),
                    pygame.transform.scale(pygame.image.load('Bomberman/lado_direito_branco.png').convert_alpha(), tamanho),
                    pygame.transform.scale(pygame.image.load('Bomberman/bomberman_tras.png').convert_alpha(), tamanho),
                    pygame.transform.scale(pygame.image.load('Bomberman/lado_esquerdo_branco.png').convert_alpha(), tamanho)
                ]
            elif jogador_id == 2:
                return [
                    pygame.transform.scale(pygame.image.load('Bomberman/bomberman_preto_frente.png').convert_alpha(), tamanho),
                    pygame.transform.scale(pygame.image.load('Bomberman/bomberman_preto_lado_direito.png').convert_alpha(), tamanho),
                    pygame.transform.scale(pygame.image.load('Bomberman/bomberman_preto_tras.png').convert_alpha(), tamanho),
                    pygame.transform.scale(pygame.image.load('Bomberman/bomberman_preto_lado_esquerdo.png').convert_alpha(), tamanho)
                ]
            else:
                raise ValueError("ID do jogador inválido")
        except pygame.error as e:
            print(f'Erro ao carregar as imagens do jogador {jogador_id}: {e}')
            # Cria uma imagem genérica como fallback
            imagem_fallback = pygame.Surface(tamanho)
            imagem_fallback.fill((255, 0, 0))  # Cor vermelha indicando sinal de erro
            return [imagem_fallback] * 4

    @property
    def vida_maxima(self):
        return self.__vida_maxima

    def configurar_vidas_iniciais(self):
        if self.dificuldade == 'Fácil':
            self.vida = 3
        elif self.dificuldade == 'Médio':
            self.vida = 2
        elif self.dificuldade == 'Difícil':
            self.vida = 1

    def set_velocidade(self, velocidade):
        self.velocidade = velocidade

    def set_vida(self, vida):
        self.vida = vida

    def aumentar_velocidade(self):
        if self.velocidade < 8:
            self.velocidade += 4

    def aumentar_vida(self):
        if self.vida < self.__vida_maxima:
            self.vida += 1

    def pegar_poder(self, poder):
        if poder.tipo not in self.poder_pegos:
            self.poder_pegos.add(poder.tipo)
            if poder.tipo == 'vida':
                self.aumentar_vida()  # Apenas aumenta a vida
            elif poder.tipo == 'velocidade':
                self.aumentar_velocidade()  # Apenas aumenta a velocidade

            poder.aplicar_poder(self)  # Aplica o poder, se necessário

    def movimento(self):
        keys = pygame.key.get_pressed()
        movimento_x = 0
        movimento_y = 0

        # Movimentação do jogador
        if keys[self.controles['cima']]:
            movimento_y -= self.velocidade
            self.image = self.images[2]
        if keys[self.controles['baixo']]:
            movimento_y += self.velocidade
            self.image = self.images[0]
        if keys[self.controles['direita']]:
            movimento_x += self.velocidade
            self.image = self.images[1]
        if keys[self.controles['esquerda']]:
            movimento_x -= self.velocidade
            self.image = self.images[3]

        # Movimenta o jogador no eixo X e checa colisões
        self.rect.x += movimento_x
        bloco_colidido = pygame.sprite.spritecollideany(self, self.mapa.blocos)
        bomba_colidida = pygame.sprite.spritecollideany(self, self.mapa.bombas)

        if bloco_colidido or bomba_colidida:
            if bloco_colidido:
                self.colisao(bloco_colidido, eixo='x')
            if bomba_colidida:
                self.colisao(bomba_colidida, eixo='x')

        # Movimenta o jogador no eixo Y e checa colisões
        self.rect.y += movimento_y
        bloco_colidido = pygame.sprite.spritecollideany(self, self.mapa.blocos)
        bomba_colidida = pygame.sprite.spritecollideany(self, self.mapa.bombas)

        if bloco_colidido or bomba_colidida:
            if bloco_colidido:
                self.colisao(bloco_colidido, eixo='y')
            if bomba_colidida:
                self.colisao(bomba_colidida, eixo='y')

        self.__posicao = self.rect.topleft  # Atualiza a posição herdada de Personagem

    def verificar_colisoes_explosoes(self):
        explosao_colidida = pygame.sprite.spritecollideany(self, self.mapa.explosoes)
        if explosao_colidida:
            self.sofrer_dano(explosao_colidida)

    def verificar_colisoes_inimigo(self):
        inimigo_colidido = pygame.sprite.spritecollideany(self, self.mapa.inimigos)
        if inimigo_colidido:
            self.sofrer_dano(inimigo_colidido)

    def update(self, dt):
        super().update(dt)
        self.movimento()

        # Verifica se o jogador está invulnerável e se o tempo de invulnerabilidade expirou
        if self.invulneravel:
            current_time = pygame.time.get_ticks() / 1000
            if current_time - self.ultimo_tempo_dano > self.tempo_invulnerabilidade:
                self.invulneravel = False

        for poder in pygame.sprite.spritecollide(self, self.mapa.poderes, True):
            self.pegar_poder(poder)
        
        if self.vida <= 0:
            self.morrer()  # Chama o método morrer da classe Personagem

        # Adiciona a lógica de animação se necessário
        keys = pygame.key.get_pressed()
        if keys[self.controles['bomba']]:
            self.plantar_bomba(dt)
