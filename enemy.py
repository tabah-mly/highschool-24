import pygame
from utils.enemy_base import EnemyBase


class Enemy(EnemyBase):
    def __init__(self, x, y, player):
        self.animations = {
            "idle": ("assets/imgs/enemy_idle.png", 4, 0.1),
            "walk": ("assets/imgs/enemy_walk.png", 4, 0.1),
            "attack": ("assets/imgs/enemy_attack.png", 4, 0.05, False),
        }

        self.stats = {
            "max_hp": 100,
            "hp": 100,
            "speed": 200,
            "damage": 25,
        }

        self.initialize(x, y, player)

    def update(self, dt):
        self.get_target_x()
        if not self.attack(dt):
            self.move(dt)
        self.update_sprites(dt)

    def draw(self, screen, camera):
        self.draw_sprites(screen, camera)
