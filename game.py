import pygame, sys
from utils.game_base import GameBase
from player import Player


class Game(GameBase):
    def __init__(self, width, height, title):
        self.screen_width = width
        self.screen_height = height
        self.screen_title = title

        self.bg_path = "assets/imgs/bg.png"

    def event_listener(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def start(self):
        pass