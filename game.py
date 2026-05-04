import pygame, sys
from utils.game_base import GameBase
from player import Player


class Game(GameBase):
    def __init__(self, width, height, title):
        self.screen_width = width
        self.screen_height = height
        self.screen_title = title

        self.bg_path = "assets/imgs/bg.png"

        self.initialize()

        self.player = Player(0, 450)

    def event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.listen(event)

    def update(self):
        self.update_game()
        if self.game_finish:
            return
        self.player.update(self.dt)
        self.player.handle_attack(self.enemies)
        self.camera.follow(self.player.rect)
        self.update_enemies()

    def draw(self):
        self.background.draw(self.screen, self.camera.offset)
        self.player.draw(self.screen, self.camera)
        self.draw_enemies()
        self.draw_game()

    def start(self):
        while self.running:
            self.set_fps()
            self.event_listener()
            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()
