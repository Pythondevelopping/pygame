import pygame
import pytmx
import pyscroll
from player import Player

from sound import Sound


class Game:
    def __init__(self):
        self.sound = Sound()
        self.end = False
        self.text1 = ""
        self.text2 = ""
        self.text3 = ""
        self.text4 = ""
        self.text5 = ""
        self.r_map = 1
        self.play = pygame.image.load('button.png')
        self.play = pygame.transform.scale(self.play, [300, 100])
        self.rect_play = self.play.get_rect()
        self.rect_play.y = 400
        self.rect_play.x = 450
        # cree la fenetre du jeu
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("aventure")
        # charger la carte
        self.tmx_data = pytmx.util_pygame.load_pygame("center.tmx")
        self.compteur = 1

        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 3
        self.under_score = 0
        self.score = 0
        self.current_animation = "idle"

        self.map = "world"
        # generer un joueur
        self.player_position = self.tmx_data.get_object_by_name("player")
        self.first_position = self.tmx_data.get_object_by_name("player")
        self.player = Player(self.player_position.x, self.player_position.y)

        self.font = pygame.font.SysFont("arial", 50, True, False)

        self.energie = 100
        # definir les rect de collision
        self.walls = []
        self.machine = []
        self.win = []
        self.instructions = []

        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "machine":
                self.machine.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "win":
                self.win.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "instructions":
                self.instructions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=8)

        self.group.add(self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
            self.current_animation = "idle"
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
            self.current_animation = "idle"
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
            self.current_animation = "idle"
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')
            self.current_animation = "idle"

    def update_score(self):
        font = pygame.font.SysFont("arial", 30, True, False)
        score_text = font.render(f"score : {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, [500, 20])
        font = pygame.font.SysFont("arial", 30, True, False)
        parole_text1 = font.render(self.text1, True, (255, 255, 255))
        parole_text2 = font.render(self.text2, True, (255, 255, 255))
        parole_text3 = font.render(self.text3, True, (255, 255, 255))
        parole_text4 = font.render(self.text4, True, (255, 255, 255))
        parole_text5 = font.render(self.text5, True, (255, 255, 255))
        self.screen.blit(parole_text1, [0, 400])
        self.screen.blit(parole_text2, [0, 425])
        self.screen.blit(parole_text3, [0, 450])
        self.screen.blit(parole_text4, [0, 475])
        self.screen.blit(parole_text5, [0, 500])

    def update(self):
        if self.end == False:
            self.group.update()
        else:
            self.end = True
            color = (0, 0, 0)
            color_blank = (255, 255, 255)
            self.screen.fill(color)
            font = pygame.font.SysFont("arial", 300, True, False)
            text = font.render("YOU HAVE WIN", True, color_blank)
            self.screen.blit(text, [150, 200])

            pygame.display.flip()

        for sprite in self.group.sprites():
            if type(sprite) == Player:
                if sprite.feet.collidelist(self.walls) > -1:
                    sprite.move_back()
                elif sprite.feet.collidelist(self.machine) > -1:
                    sprite.move_back()
                    sprite.position = sprite.first
                self.under_score += 1
                if self.under_score >= 15:
                    self.score += 1
                    self.under_score = 0
                if sprite.feet.collidelist(self.instructions) > -1:

                    self.text2 = "salut jeune explorateur"
                    self.text3 = " toi qui est entré dans le labyrinth je te met à l'epreuve"
                    self.text4 = "dans ta route tu trouvera soit des pierres soit des plantations "
                    self.text5 = "suis celui qui est le mieux adapté à ce milieu"
                else:
                    self.text1 = ""
                    self.text2 = ""
                    self.text3 = ""
                    self.text4 = ""
                    self.text5 = ""

                if self.player.rect.collidelist(self.win) > -1:
                    self.sound.play2()
                    self.end = True

    def run(self):
        clock = pygame.time.Clock()
        # boucle du jeu
        running = True
        while running:
            if self.end != True:
                self.player.save_location()
                self.handle_input()
                self.update()
                self.group.center(self.player.rect)
                self.group.draw(self.screen)
                self.update_score()

                self.sound.play()
            else:
                if self.player.rect.collidelist(self.win) > -1:
                    self.sound.play2()
                    self.end = True
                    color = (0, 0, 0)
                    color_blank = (255, 255, 255)
                    self.screen.fill(color)
                    font = pygame.font.SysFont("arial", 120,True, False)
                    font2 = pygame.font.SysFont("arial", 70,True, False)
                    text = font.render("TU AS GAGNE", True, color_blank)
                    text2 = font2.render(f"TEMPS PERDU : {self.score}s", True, color_blank)
                    self.screen.blit(text, [25, 100])
                    self.screen.blit(text2, [125, 230])

                    self.screen.blit(self.play, self.rect_play)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and self.end == True:
                    if self.rect_play.collidepoint(event.pos):
                        self.player.position = self.player.first
                        self.sound.play1()
                        self.under_score = 0
                        self.score = 0
                        self.end = False

            clock.tick(20)
        pygame.quit()


