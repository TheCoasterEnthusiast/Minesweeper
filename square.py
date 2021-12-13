import pygame

from square_textures import SquareTextures


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, length, row, column):
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.length = length
        self.row = row
        self.column = column
        self.texture_key = 'C'

        self.image = SquareTextures.SQUARE_TEXTURES[self.texture_key].convert()
        self.image = pygame.transform.smoothscale(self.image, (self.length, self.length))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def __repr__(self):
        return f'<Square sprite at row {self.row}, column {self.column}>'

    def update_image(self):
        self.image = SquareTextures.SQUARE_TEXTURES[self.texture_key].convert()
        self.image = pygame.transform.smoothscale(self.image, (self.length, self.length))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def check_if_clicked_on(self, pos):
        return self.rect.collidepoint(pos)

    def update(self):
        self.update_image()
