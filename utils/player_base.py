import pygame


class PlayerBase:
    def initialize(self, x, y):
        self.state = "idle"
        self.facing_right = True
        self.is_run = False
        self.animator = self.animations[self.state]
        self.pos = pygame.Vector2(x, y)
        self.rect = self.animator.image.get_rect(center=(x, y))
        self.font = pygame.font.Font("assets/fonts/monogram.ttf", 60)

    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.animator = self.animations[state]
            self.animator.reset()

    def update_sprites(self, dt):
        self.animator.update(dt)

    def draw_sprites(self, screen, camera):
        image = self.animator.image

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        rect = camera.apply(self.rect)
        screen.blit(image, rect)

        text_surface = self.font.render(f"{self.stats['hp']}", True, (0, 0, 255))
        text_rect = text_surface.get_rect(center=(rect.x + 130, rect.y - 222))
        screen.blit(text_surface, text_rect)

    def check_run(self, keys, run_speed, walk_speed):
        if keys[pygame.K_LSHIFT]:
            self.stats["speed"] = run_speed
            self.is_run = True
        else:
            self.stats["speed"] = walk_speed
            self.is_run = False

    def move(self, direction, dt):
        if self.state == "attack":
            return

        if direction.length_squared() > 0:
            direction = direction.normalize()

            if direction[0] < 0:
                self.facing_right = False
            else:
                self.facing_right = True

            self.pos += direction * self.stats["speed"] * dt
            self.rect.center = self.pos
            self.set_state("run" if self.is_run else "walk")
        else:
            self.set_state("idle")
