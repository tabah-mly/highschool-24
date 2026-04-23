import pygame


class PlayerBase:
    def initialize(self, x, y):
        self.state = "idle"
        self.facing_right = True
        self.animator = self.animations[self.state]
        self.pos = pygame.Vector2(x, y)
        self.rect = self.animator.image.get_rect(center=(x, y))

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

        player_rect = camera.apply(self.rect)
        screen.blit(image, player_rect)

    def move(self, direction, dt):
        if direction.length_squared() > 0:
            direction = direction.normalize()

            if direction[0] < 0:
                self.facing_right = False
            else:
                self.facing_right = True

            self.pos += direction * self.stats["speed"] * dt
            self.rect.center = self.pos
            self.set_state("run" if self.stats["speed"] > 200 else "walk")
        else:
            self.set_state("idle")
