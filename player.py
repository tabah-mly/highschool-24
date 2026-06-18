import pygame
from utils.player_base import PlayerBase
from utils.spritesheet import SpriteSheet


class Player(PlayerBase):
    def __init__(self, x, y):
        self.animations = {
            "idle": SpriteSheet("assets/imgs/player_idle.png", 2, 0.1),
            "walk": SpriteSheet("assets/imgs/player_walk.png", 2, 0.1),
            "run": SpriteSheet("assets/imgs/player_run.png", 2, 0.07),
            "attack": SpriteSheet("assets/imgs/player_attack.png", 2, 0.05, False),
        }

        self.stats = {
            "max_hp": 100,
            "hp": 100,
            "walk": 200,
            "run": 400,
            "damage": 100,
        }

        self.initialize(x, y)

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(keys[pygame.K_d] - keys[pygame.K_a], 0)
        self.move(keys, direction, dt)

    def update(self, dt):
        self.handle_input(dt)
        self.update_sprites(dt)

    def draw(self, screen, camera):
        self.draw_sprites(screen, camera)
