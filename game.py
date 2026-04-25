import pygame, sys
from utils.game_base import GameBase
from player import Player
from enemy import Enemy


class Game(GameBase):
    def __init__(self, width, height, title):
        self.screen_width = width
        self.screen_height = height
        self.screen_title = title

        self.bg_path = "assets/imgs/bg.png"

        self.initialize()

        self.player = Player(self.screen_width // 2, 450)
        self.enemy = Enemy((self.screen_width // 2) + 100, 420, self.player)

    def event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.player.update(self.dt)
        self.camera.follow(self.player.rect)
        self.enemy.update(self.dt)

    def draw(self):
        self.background.draw(self.screen, self.camera.offset)
        self.enemy.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)

    def start(self):
        while self.running:
            self.set_fps()
            self.event_listener()
            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()
