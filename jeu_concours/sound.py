import pygame

class Sound:
    def __init__(self):
        self.compteur = 1
        self.sound = "background.mp3"
        self.sound2 = "win.mp3"
        self.sound3 = "instructions.mp3"
        self.sound_game = pygame.mixer.Sound(f"music/{self.sound}")
        self.sound_game2 = pygame.mixer.Sound(f"music/{self.sound2}")
        self.sound_game3 = pygame.mixer.Sound(f"music/{self.sound3}")

    def play(self):
        self.sound_game.play(100)
    def stop(self):
        self.sound_game.stop()

    def play2(self):

        self.sound_game.stop()

        self.sound_game2.play()
        
        
    def play3(self):

        self.sound_game.stop()

        self.sound_game3.play()
    def play1(self):

        self.sound_game2.stop()

        self.sound_game.play()



