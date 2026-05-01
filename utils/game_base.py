import pygame, random
from enemy import Enemy
from utils.infinite_background import InfiniteBackground
from utils.camera import Camera


class GameBase:
    def initialize(self):
        pygame.init()
        pygame.display.set_caption(self.screen_title)
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height), display=1
        )
        self.clock = pygame.time.Clock()

        self.background = InfiniteBackground(
            self.bg_path, screen_height=self.screen_height
        )
        self.camera = Camera(self.screen_width, self.screen_height)

        self.running = True

        self.enemies = []
        self.max_enemies = 3
        self.spawn_interval = 2
        self.spawn_timer = 0

    def set_fps(self, frame=60):
        dt_raw = self.clock.tick(frame) / 1000
        self.dt = min(dt_raw, 0.05)

    def spawn_enemy(self):
        spawn_x = self.camera.offset.x + self.screen_width + random.randint(300, 600)
        enemy = Enemy(spawn_x, 420, self.player)
        self.enemies.append(enemy)

    def update_enemies(self):
        self.enemies = [e for e in self.enemies if not e.dead]
        
        if len(self.enemies) < self.max_enemies:
            self.spawn_timer -= self.dt
            if self.spawn_timer <= 0:
                self.spawn_timer = self.spawn_interval
                self.spawn_enemy()

        for enemy in self.enemies:
            enemy.update(self.dt)

    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera)
