import pygame
from utils.infinite_background import InfiniteBackground
from utils.camera import Camera


class GameBase:
    def initialize(self):
        pygame.init()
        pygame.display.set_caption(self.screen_title)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.background = InfiniteBackground(self.bg_path, screen_height=self.screen_height)
        self.camera = Camera(self.screen_width, self.screen_height)

        self.running = True

    def set_fps(self, frame=60):
        dt_raw = self.clock.tick(frame) / 1000
        self.dt = min(dt_raw, 0.05)
