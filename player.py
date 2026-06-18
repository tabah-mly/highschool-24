import pygame
from utils.player_base import PlayerBase
from utils.spritesheet import SpriteSheet

class Player(PlayerBase):
    def __init__(self, x, y):
        self.animations = {
            "idle": ("assets/imgs/player_idle.png", 2, 0.1),
            "walk": ("assets/imgs/player_walk.png", 2, 0.1),
            "run": ("assets/imgs/player_run.png", 2, 0.07),
            "attack": ("assets/imgs/player_attack.png", 2, 0.5, False),
        }

        self.stats = {
            "max_hp": 100,
            "hp": 100,
            "walk": 200,
            "run": 400,
            "damage": 100,
        }

        self.initialize(x, y)