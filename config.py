import pygame


class Configurações:
    def __init__(self) :
        self.dificuldades = ['Fácil', 'Médio', 'Difícil']
        self.som_mutado = False
        self.nome_jogador = ""
        self.personagens = ['Bomberman 1', 'Bomberman 2']
        self.dificuldade_atual = ['Médio']
        self.jogo_iniciado = False
        self.jogo_pausado = False
        self.numero_jogadores = 1

    def escolher_dificuldade(self, dificuldade):
        if dificuldade in self.dificuldades:
            self.dificuldade_atual = dificuldade
            
    def mutar_desmutar_som(self):
        # Alterna o estado do som e controla o som usando pygame.mixer
        if self.som_mutado:
            pygame.mixer.music.set_volume(0)  # Desmuta o som
        else:
            pygame.mixer.music.set_volume(1)  # Muta o som

        self.som_mutado = not self.som_mutado  # Atualiza o estado do som
    
    def controlar_som_efeitos(self, efeito_som):
        if self.som_mutado:
            efeito_som.set_volume(0)  # Muta o efeito sonoro
        else:
            efeito_som.set_volume(1)  # Desmuta o efeito sonoro
    
    def digitar_nome(self, nome):
        self.nome_jogador = nome
    
    def iniciar_jogo(self):
        if self.nome_jogador:
            self.jogo_iniciado = True
    
    def pausar(self):
        self.jogo_pausado = not self.jogo_pausado
    
    def retomar_jogo(self):
        if self.jogo_pausado:
            self.jogo_pausado = False
    
    def escolher_numero_jogadores(self, numero):
        if numero in [1,2]:
            self.numero_jogadores = numero
    

    