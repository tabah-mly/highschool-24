import pygame, random
from enemy import Enemy
from utils.finish import Finish
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

        self.arena = 500

        self.is_finish = False
        self.finish_right = Finish(self.screen_height, self.arena)
        self.finish_left = Finish(self.screen_height, -self.arena)

        self.font = pygame.font.Font("assets/fonts/monogram.ttf", 40)

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

    def debug_text(self, text, pos):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, pos)

    def update_finish(self):
        self.finish_right.update()
        self.finish_left.update()

        is_finish_right = self.finish_right.is_finish(self.player)
        is_finish_left = self.finish_left.is_finish(self.player)

        self.is_finish = is_finish_right or is_finish_left

    def draw_finish(self):
        self.finish_right.draw(self.screen, self.camera)
        self.finish_left.draw(self.screen, self.camera)

    def debug_show(self):
        self.debug_text(f"Finish Right pos: {self.finish_right.finish_rect}", (20, 10))
        self.debug_text(f"Finish Left pos: {self.finish_left.finish_rect}", (20, 40))
        self.debug_text(f"Player pos: {self.player.pos}", (20, 70))

    def draw_player_hp(self):
        hp_x, hp_y = 20, 20
        hp_w, hp_h = (self.screen_width // 3) - (hp_x * 2), 20

        pygame.draw.rect(
            self.screen,
            (135, 0, 0),
            (hp_x, hp_y, hp_w * (self.player.stats["max_hp"] / 100), hp_h),
        )
        pygame.draw.rect(
            self.screen,
            (228, 13, 0),
            (hp_x, hp_y, hp_w * (self.player.stats["hp"] / 100), hp_h),
        )

    def draw_finish_screen(self):
        text_surface = self.font.render("Finish!", True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2)
        )
        self.screen.blit(text_surface, text_rect)

    def draw_ui(self):
        if self.is_finish:
            self.draw_finish_screen()
        else:
            self.draw_player_hp()
