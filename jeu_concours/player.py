import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.ajout = ""
        self.photo = "player.png"
        self.sprite_sheet = pygame.image.load(self.photo)
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.max_health = 200
        self.first = self.position.copy()
        self.health = 200
        self.images = {
            "down" : self.get_image(0, 0),
            "left": self.get_image(0, 32),
            "right": self.get_image(0, 64),
            "up": self.get_image(0, 96),

        }
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.velocity = 7
    def save_location(self):
        self.old_position = self.position.copy()

    def change_animation(self, name):

        if self.ajout == "player_rage":
            self.photo = "Copie de player.png"
        self.image = self.images[name]
        self.image.set_colorkey((0, 0, 0))

    def update_health_bar(self, surface):
        pygame.draw.rect(surface, (60, 63, 60), [10, 10, self.max_health, 20])
        pygame.draw.rect(surface, (111, 210, 46), [10, 10, self.health, 20])


    def move_right(self): self.position[0] += self.velocity

    def move_left(self): self.position[0] -= self.velocity

    def move_up(self): self.position[1] -= self.velocity

    def move_down(self): self.position[1] += self.velocity
    def return_to_first(self):self.position = [0,0]
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image