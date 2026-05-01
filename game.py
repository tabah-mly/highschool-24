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

    def event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.player.update(self.dt)
        self.player.handle_attack(self.enemies)
        self.camera.follow(self.player.rect)
        self.update_enemies()

    def draw(self):
        self.background.draw(self.screen, self.camera.offset)
        self.player.draw(self.screen, self.camera)
        self.draw_enemies()

    def start(self):
        while self.running:
            self.set_fps()
            self.event_listener()
            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()
