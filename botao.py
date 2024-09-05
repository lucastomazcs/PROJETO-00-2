import pygame
from config import Configurações

class Botao:
    
    def __init__(self, x, y, largura, altura, texto, cor_fundo, cor_texto, acao=None, imagens=None, configuracoes=None) -> None:
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_fundo = cor_fundo
        self.cor_texto = cor_texto
        self.acao = acao
        self.configuracoes = configuracoes

        # Gerenciamento de imagens
        self.imagens = imagens
        if self.imagens:
            if len(self.imagens) > 1:
                self.imagem_atual = pygame.transform.scale(pygame.image.load(self.imagens[0]), (largura, altura))
                self.imagem_mutada = pygame.transform.scale(pygame.image.load(self.imagens[1]), (largura, altura))
            else:
                # Se não houver imagem para o estado mutado, usar a mesma imagem para ambos os estados
                self.imagem_atual = pygame.transform.scale(pygame.image.load(self.imagens[0]), (largura, altura))
                self.imagem_mutada = self.imagem_atual
        else:
            # Caso não haja imagens, use o fundo e texto padrão
            self.imagem_atual = None
            self.imagem_mutada = None
        
    def desenhar(self, tela):
        if self.imagens:
            if self.configuracoes and self.configuracoes.som_mutado:
                tela.blit(self.imagem_mutada, self.rect)
            else:
                tela.blit(self.imagem_atual, self.rect)
        else:
            pygame.draw.rect(tela, self.cor_fundo, self.rect)
            # Adicionar texto, se necessário

    def checar_clique(self, posicao_mouse):
        if self.rect.collidepoint(posicao_mouse):
            if self.acao:
                self.acao()
            if self.imagens and self.configuracoes:
                self.configuracoes.mutar_desmutar_som()
    
     #Criando botão Facíl:
    @staticmethod
    def criar_botao_facil(largura_tela, altura_tela):
        return Botao(
            x = 70,
            y = (altura_tela // 2) - 100,
            largura = 200,
            altura = 120,
            texto = 'Fácil',
            cor_fundo = (0,0,0),
            cor_texto = (255,255,255),
            imagens = ['Botões/botao_easyy.png']
        )

    @staticmethod
    def criar_botao_medio(largura_tela, altura_tela):
        return Botao(
            x = 300,
            y = (altura_tela // 2) - 100,
            largura = 200,
            altura = 120,
            texto = 'Médio',
            cor_fundo = (0,0,0),
            cor_texto = (255,255,255),
            imagens = ['Botões/botao_normall.png']
        )

    @staticmethod
    def criar_botao_dificil(largura_tela, altura_tela):
        return Botao(
            x = 550,
            y = (altura_tela // 2) - 100,
            largura = 200,
            altura = 120,
            texto = 'Difícil',
            cor_fundo = (0,0,0),
            cor_texto = (255,255,255),
            imagens = ['Botões/botao_hardd.png']
        )

    @staticmethod
    def criar_botao_som(largura_tela, altura_tela, configuracoes):
        return Botao(
            x = 100,
            y = 100,
            largura = 50,
            altura = 50,
            texto = '',
            cor_fundo = (0,0,0),
            cor_texto = (255, 255, 255),
            imagens = ['Botões/botão__som.png', 'Botões/botao_ranking.png'], #Imagens para o botão de som
            configuracoes = configuracoes # Passa a instancia de configurações

        )
    
    
    @staticmethod
    def criar_botao_novo_jogo(largura_tela, altura_tela):
        return Botao(
            x = 350,
            y = 300,
            largura = 80,
            altura = 25,
            texto = 'Novo Jogo',
            cor_fundo = (0, 0, 0),
            cor_texto = (255, 255, 255),
            imagens = ['Botões/botão_novoJogo.png']
        )

    @staticmethod
    def criar_botao_continuar(largura_tela, altura_tela):
        return Botao(
            x = 350,
            y = 400,
            largura = 80,
            altura = 25,
            texto = 'Continuar',
            cor_fundo = (0, 0, 0),
            cor_texto = (255, 255, 255),
            imagens = ['Botões/botão_continuar.png']
        )
    
    @staticmethod
    def criar_botao_salvar(largura_tela, altura_tela, acao_salvar):
        return Botao(
            x = 350,
            y = 350,
            largura = 80,  
            altura = 25,   
            texto = 'Salvar',
            cor_fundo = (0, 0, 0),
            cor_texto = (255, 255, 255),
            acao = acao_salvar,
            imagens = ['Botões/botão_salvar.png']
        )

    @staticmethod
    def criar_botao_sair(largura_tela, altura_tela, acao_sair):
        return Botao(
            x = 350,
            y = 400,
            largura = 65,  
            altura = 25,   
            texto = 'Sair',
            cor_fundo = (0, 0, 0),
            cor_texto = (255, 255, 255),
            acao = acao_sair,
            imagens = ['Botões/botão_sair.png']
        )
    
