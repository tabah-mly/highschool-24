import pygame
from utils.enemy_base import EnemyBase
from utils.spritesheet import SpriteSheet


class Enemy(EnemyBase):
    def __init__(self, x, y, player):
        self.animations = {
            "idle": SpriteSheet("assets/imgs/enemy_idle.png", 4, 0.1),
            "walk": SpriteSheet("assets/imgs/enemy_walk.png", 4, 0.1),
            "attack": SpriteSheet("assets/imgs/enemy_attack.png", 4, 0.07),
        }

        self.stats = {
            "max_hp": 100,
            "hp": 100,
            "speed": 200,
            "damage": 20,
        }

        self.initialize(x, y, player)

    def update(self, dt):
        self.move(dt)
        self.update_sprites(dt)

    def draw(self, screen, camera):
        self.draw_sprites(screen, camera)
