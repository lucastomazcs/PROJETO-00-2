import pygame
import sys
from mapa import Mapa
from player import Player
from inimigo import Inimigo
from tkinter import Tk
from save import Salvar
from config import Configurações
from botao import Botao
import time
from poderes import Poder
from inimigoexplosivo import InimigoExplosivo


class Jogo:
    def __init__(self, dificuldade='', numero_jogadores=1):
        pygame.init()
        pygame.mixer.init()

        # Instanciando configurações
        self.configuracoes = Configurações()

        self.tempo_inicio = time.time()

        root = Tk()
        altura_monitor = root.winfo_screenheight()
        largura_monitor = root.winfo_screenwidth()

        self.num_blocos_x = 15
        self.num_blocos_y = 15
        self.tamanho_bloco = (altura_monitor // self.num_blocos_y) - 5

        self.largura = self.num_blocos_x * self.tamanho_bloco
        self.altura = self.num_blocos_y * self.tamanho_bloco

        self.tela = pygame.display.set_mode((self.largura, self.altura), pygame.RESIZABLE)
        pygame.display.set_caption("Bomberman")

        self.cor_preta = (0, 0, 0)
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.vitoria = False
        self.rodando = True

        # Valores padrão antes da configuração
        self.velocidade_jogador = 3  # Valor padrão
        self.velocidade_inimigo = 100  # Valor padrão
        self.vida_inimigo = 3  # Valor padrão
        self.vida_jogador = 3
      


        self.dificuldade = dificuldade
        self.numero_jogadores = numero_jogadores

        # Inicializa o mapa, jogador e inimigo
        self.mapa = Mapa(self.num_blocos_x, self.num_blocos_y, self.tamanho_bloco, self.tela, dificuldade)
        tamanho_imagem = (self.tamanho_bloco - 8, self.tamanho_bloco - 8)
        tamanho_imagem_inimigo = (self.tamanho_bloco - 9, self.tamanho_bloco - 9)
        
        # Criação do jogador
        self.jogador = Player((60, 60), self.vida_jogador, self.velocidade_jogador, 3, self.mapa,self.dificuldade, tamanho=tamanho_imagem, jogador_id=1)

        # Criação do inimigo
        self.inimigo = Inimigo((self.tamanho_bloco * 14, self.tamanho_bloco * 14), self.vida_inimigo, self.velocidade_inimigo, 'direcao', self.mapa, tamanho=tamanho_imagem_inimigo)
        
        # Exemplo: adicionar um inimigo explosivo ao mapa
        self.inimigo_explosivo = InimigoExplosivo(posicao=(60, 800), tamanho=(120, 120), velocidade=10, mapa=self.mapa,raio_explosao= 50)

        # Chama o método de ajustar dificuldade após criar os objetos
        self.ajustar_dificuldade(self.dificuldade)

        # Atualiza o jogador e o inimigo com as novas configurações
        self.jogador.set_velocidade(self.velocidade_jogador)
        self.inimigo.set_vida(self.vida_inimigo)
        self.inimigo.velocidade = self.velocidade_inimigo
        self.jogador.set_vida(self.vida_jogador)

        self.mapa.jogadores = [self.jogador]
        self.mapa.inimigos = [self.inimigo, self.inimigo_explosivo]
        

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.jogador)
        self.sprites.add(self.inimigo)
        self.sprites.add(self.inimigo_explosivo)

        # Verifica se o número de jogadores é igual a 2 para adicionar o segundo:
        if self.numero_jogadores == 2:
            controles_player2 = {
                'cima': pygame.K_UP,
                'baixo': pygame.K_DOWN,
                'esquerda': pygame.K_LEFT,
                'direita': pygame.K_RIGHT,
                'bomba': pygame.K_KP_ENTER
            }
            self.jogador2 = Player((700, 60), self.vida_jogador, self.velocidade_jogador, 3, self.mapa, self.dificuldade, tamanho=tamanho_imagem, controles=controles_player2,jogador_id=2)
            self.mapa.jogadores.append(self.jogador2)
            self.sprites.add(self.jogador2)

        # Criando botões:
        self.botao_start = pygame.Rect(300, 455, 150, 50)
        self.botao_sair = pygame.Rect(300, 530, 150, 50)

        self.salvar = Salvar()

        self.estado = "Inicial"  # Define Estado inicial do Jogo

        # Criando botões usando métodos estáticos da classe Botao
        self.botao_1player = Botao.criar_botao_1player(self.largura, self.altura)
        self.botao_2player = Botao.criar_botao_2player(self.largura, self.altura)
        self.botao_facil = Botao.criar_botao_facil(self.largura, self.altura)
        self.botao_medio = Botao.criar_botao_medio(self.largura, self.altura)
        self.botao_dificil = Botao.criar_botao_dificil(self.largura, self.altura)
        self.botao_som = Botao.criar_botao_som(self.largura, self.altura, self.configuracoes)

        self.botoes_jogadores = [self.botao_1player, self.botao_2player]
        self.botoes_dificuldade = [self.botao_facil, self.botao_medio, self.botao_dificil]

        self.selecao_dificuldade = None
        self.selecao_jogadores = None

    def ajustar_dificuldade(self, dificuldade):
        print(f"Ajustando dificuldade para: {dificuldade}")
        if dificuldade == 'Fácil':
            self.velocidade_jogador = 3
            self.velocidade_inimigo = 50
            self.vida_inimigo = 2
            self.vida_jogador = 4
        elif dificuldade == 'Médio':
            self.velocidade_jogador = 2
            self.velocidade_inimigo = 250
            self.vida_inimigo = 3
            self.vida_jogador = 3
        elif dificuldade == 'Difícil':
            self.velocidade_jogador = 1
            self.velocidade_inimigo = 400
            self.vida_inimigo = 4
            self.vida_jogador = 2

        # Atualizar o jogador e inimigo, se já foram inicializados
        if hasattr(self, 'jogador'):
            self.jogador.set_velocidade(self.velocidade_jogador)
            self.jogador.set_vida(self.vida_jogador)
        if hasattr(self, 'inimigo'):
            self.inimigo.set_vida(self.vida_inimigo)
            self.inimigo.velocidade = self.velocidade_inimigo

    def tela_escolha(self):
        imagem_configuracoes = pygame.image.load("telas/tela_estrelas.png")
        imagem_configuracoes = pygame.transform.scale(imagem_configuracoes, (self.largura, self.altura))
        self.tela.blit(imagem_configuracoes, (0, 0))

        for botao in self.botoes_dificuldade:
            botao.desenhar(self.tela)
        for botao in self.botoes_jogadores:
            botao.desenhar(self.tela)

        pygame.display.flip()

    def tela_inicial(self):
        imagem_inicio = pygame.image.load("telas/tela_inicial.png")
        imagem_inicio = pygame.transform.scale(imagem_inicio, (self.largura, self.altura))
        self.tela.blit(imagem_inicio, (0, 0))

        pygame.display.flip()

    def tela_game_over(self):
        imagem_game_over = pygame.image.load("telas/Tela_Game_Overr.png")
        imagem_game_over = pygame.transform.scale(imagem_game_over, (self.largura, self.altura))
        self.tela.blit(imagem_game_over, (0, 0))
        pygame.display.flip()

    def tela_vitoria(self):
        imagem_vitoria = pygame.image.load("telas/tela_Vitoriaa.png")
        imagem_vitoria = pygame.transform.scale(imagem_vitoria, (self.largura, self.altura))
        self.tela.blit(imagem_vitoria, (0, 0))
        pygame.display.flip()

    def tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if self.estado == "Inicial" and evento.key == pygame.K_SPACE:  # Pressione espaço para iniciar
                    self.estado = "Jogando"
                elif self.game_over and evento.key == pygame.K_r:
                    self.reiniciar_jogo()
                elif self.game_over and evento.key == pygame.K_q:
                    self.rodando = False
                elif self.vitoria and evento.key == pygame.K_r:
                    self.reiniciar_jogo()
                elif self.vitoria and evento.key == pygame.K_q:
                    self.rodando = False
                elif evento.key == pygame.K_t:
                    self.salvar.salvar_jogo(self.jogador, self.inimigo, self.mapa)
                elif evento.key == pygame.K_l:
                    self.salvar.carregar_jogo(self.jogador, self.inimigo, self.mapa)
                    self.estado = "Jogando"
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Clique com o botão esquerdo do mouse
                if self.estado == "Inicial":
                    if self.botao_start.collidepoint(evento.pos):  # Se clicar no botão Start invisível
                        self.estado = "Escolha"
                    elif self.botao_sair.collidepoint(evento.pos):  # Se clicar no botão Sair invisível
                        self.rodando = False
                elif self.estado == "Escolha":
                    if self.botao_facil.rect.collidepoint(evento.pos):
                        self.selecao_dificuldade = 'Fácil'
                        print('Dificuldade escolhida: Fácil')  # Debug
                    elif self.botao_medio.rect.collidepoint(evento.pos):
                        self.selecao_dificuldade = 'Médio'
                        print('Dificuldade escolhida: Médio')
                    elif self.botao_dificil.rect.collidepoint(evento.pos):
                        self.selecao_dificuldade = 'Difícil'
                        print('Dificuldade escolhida: Difícil')

                    # Verifica seleção de jogadores:
                    if self.botao_1player.rect.collidepoint(evento.pos):
                        self.selecao_jogadores = 1
                        print('Número de jogadores escolhidos: 1')
                    elif self.botao_2player.rect.collidepoint(evento.pos):
                        self.selecao_jogadores = 2
                        print('Número de jogadores escolhidos: 2')

                    # Se ambas as seleções forem feitas iniciar jogo:
                    if self.selecao_dificuldade and self.selecao_jogadores:
                        self.ajustar_dificuldade(self.selecao_dificuldade)
                        self.numero_jogadores = self.selecao_jogadores

                        # Reinicializa o jogo com os parâmetros definidos
                        self.reiniciar_jogo()
                        self.estado = 'Jogando'

                else:
                    # Checar clique no botão de som:
                    self.botao_som.checar_clique(evento.pos)

    def reiniciar_jogo(self):
        # Reiniciar o jogo com base na seleção de dificuldade e número de jogadores
        self.__init__(dificuldade=self.selecao_dificuldade, numero_jogadores=self.selecao_jogadores)
        self.ajustar_dificuldade(self.dificuldade)

    def atualizar_tempo(self):
        if self.estado == 'Jogando':
            tempo_atual = time.time()
            self.tempo_decorrido = tempo_atual - self.tempo_inicio

    def update(self, dt):
        self.atualizar_tempo()
        if self.estado == "Inicial":
            self.tela_inicial()
            pygame.display.flip()

        elif self.estado == "Escolha":
            self.tela_escolha()
            pygame.display.flip()

        elif self.estado == "Jogando":
            if not self.game_over and not self.vitoria:
                self.jogador.update(dt)

                # Se o número de jogadores for 2, atualize o segundo jogador:
                if self.numero_jogadores == 2 and hasattr(self, 'jogador2'):
                    self.jogador2.update(dt)

                self.inimigo.update(self.mapa.jogadores, dt)

                # Atualizar e desenhar o inimigo explosivo
                self.inimigo_explosivo.update(dt)
                self.inimigo_explosivo.draw(self.tela)


                # Verifica se o jogador colidiu com algum poder
                poder_coletado = pygame.sprite.spritecollideany(self.jogador, self.mapa.poderes)
                if poder_coletado:
                    poder_coletado.aplicar_poder(self.jogador)
                    poder_coletado.kill()

                if self.numero_jogadores == 2:
                    poder_coletado_jogador2 = pygame.sprite.spritecollideany(self.jogador2, self.mapa.poderes)
                    if poder_coletado_jogador2:
                        poder_coletado_jogador2.aplicar_poder(self.jogador2)
                        poder_coletado_jogador2.kill()

                self.tela.fill(self.cor_preta)
                self.mapa.desenhar(self.tela)
                self.mapa.bombas.draw(self.tela)
                self.sprites.draw(self.tela)

                # Atualiza e desenha as explosões
                self.mapa.explosoes.update(dt)
                self.mapa.explosoes.draw(self.tela)
                self.mapa.update(dt)

                # Desenha o botão de som
                # self.botao_som.desenhar(self.tela)

                pygame.display.flip()

                # Verifica se algum jogador perdeu todas as vidas
                if not self.jogador.alive() and (self.numero_jogadores == 1 or (self.numero_jogadores == 2 and not self.jogador2.alive())):
                    self.game_over = True

                # Verifica se o inimigo foi derrotado
                if not self.inimigo.alive() and not self.inimigo_explosivo.alive():
                    self.vitoria = True

            elif self.game_over:
                self.tela_game_over()
                self.clock.tick(60)
            elif self.vitoria:
                self.tela_vitoria()
                self.clock.tick(60)

    def run(self):
        while self.rodando:
            dt = self.clock.tick(60) / 1000
            self.tratar_eventos()
            self.update(dt)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Jogo()
    game.run()
