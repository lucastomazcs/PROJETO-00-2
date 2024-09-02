import pygame
from pygame.sprite import Sprite

class Bloco(Sprite):
    def __init__(self, imagem, x, y, tamanho_bloco, destrutivel=False):
        super().__init__()
        self._image_path = imagem
        self._image = pygame.image.load(imagem).convert_alpha()
        self._image = pygame.transform.scale(self._image, (tamanho_bloco, tamanho_bloco))
        self.rect = self._image.get_rect()
        self.rect.topleft = (x, y)
        self._destrutivel = destrutivel

    @property
    def image(self):
        return self._image
    
    @property
    def destrutivel(self):
        return self._destrutivel

    def aumentar_tamanho(self, tamanho_novo):
        center = self.rect.center
        self._image = pygame.transform.scale(self._image, (tamanho_novo, tamanho_novo))
        self.rect = self._image.get_rect()
        self.rect.center = center

    def redimensionar_imagem(self, novo_tamanho):
        self._image = pygame.transform.scale(self._image, (novo_tamanho, novo_tamanho))
        self.rect = self._image.get_rect(topleft=self.rect.topleft)
